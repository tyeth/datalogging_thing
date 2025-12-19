"""
CircuitPython Datalogging Project
Uses INA260 sensor for high-speed current/voltage monitoring
Logs to SD card via Adalogger FeatherWing
Displays values on screen using displayio
"""

import time
import board
import busio
import digitalio
import sdcardio
import storage
import displayio
import terminalio
from adafruit_display_text import label
from adafruit_ina260 import INA260

# Display setup (for 1.14" 240x135 screen or similar)
# This assumes ST7789 driver commonly used with these displays
try:
    from adafruit_st7789 import ST7789
    display_available = True
except ImportError:
    display_available = False
    print("Display driver not available")

# Configuration
SAMPLE_INTERVAL = 0.01  # 10ms between samples for high-speed logging
LOG_FILE = "/sd/datalog.csv"
DISPLAY_UPDATE_INTERVAL = 0.5  # Update display every 500ms

# Initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)

# Initialize INA260 sensor
ina260 = INA260(i2c)
# Configure for fastest conversion time (140us for both voltage and current)
ina260.averaging_count = 1  # No averaging for maximum speed
ina260.current_conversion_time = 0  # 140us
ina260.voltage_conversion_time = 0  # 140us

print("INA260 initialized")
print(f"Conversion time: {ina260.current_conversion_time}, {ina260.voltage_conversion_time}")

# Initialize SD card on SPI
try:
    spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
    cs = digitalio.DigitalInOut(board.D10)  # Common CS pin for Adalogger
    sdcard = sdcardio.SDCard(spi, cs)
    vfs = storage.VfsFat(sdcard)
    storage.mount(vfs, "/sd")
    sd_available = True
    print("SD card mounted successfully")
    
    # Create/open log file with headers
    try:
        with open(LOG_FILE, "w") as f:
            f.write("timestamp,voltage_V,current_mA,power_mW\n")
        print(f"Log file created: {LOG_FILE}")
    except Exception as e:
        print(f"Error creating log file: {e}")
        sd_available = False
        
except Exception as e:
    print(f"SD card initialization failed: {e}")
    sd_available = False

# Initialize Display
if display_available:
    try:
        displayio.release_displays()
        
        # SPI for display (may share with SD card or use separate pins)
        # Adjust pins based on your specific display connection
        display_spi = busio.SPI(board.SCK, board.MOSI)
        display_cs = digitalio.DigitalInOut(board.D5)
        display_dc = digitalio.DigitalInOut(board.D6)
        display_rst = digitalio.DigitalInOut(board.D9)
        
        display_bus = displayio.FourWire(
            display_spi, command=display_dc, chip_select=display_cs, reset=display_rst
        )
        
        display = ST7789(
            display_bus,
            width=240,
            height=135,
            rowstart=40,
            colstart=53,
            rotation=270
        )
        
        # Create display group
        splash = displayio.Group()
        display.root_group = splash
        
        # Create text labels
        title_label = label.Label(
            terminalio.FONT,
            text="INA260 Monitor",
            color=0xFFFFFF,
            x=10,
            y=10
        )
        
        voltage_label = label.Label(
            terminalio.FONT,
            text="Voltage: ----.-V",
            color=0x00FF00,
            x=10,
            y=40
        )
        
        current_label = label.Label(
            terminalio.FONT,
            text="Current: ----.-mA",
            color=0x00FFFF,
            x=10,
            y=70
        )
        
        power_label = label.Label(
            terminalio.FONT,
            text="Power: ----.-mW",
            color=0xFFFF00,
            x=10,
            y=100
        )
        
        status_label = label.Label(
            terminalio.FONT,
            text="Status: OK",
            color=0xFF00FF,
            x=10,
            y=130
        )
        
        splash.append(title_label)
        splash.append(voltage_label)
        splash.append(current_label)
        splash.append(power_label)
        splash.append(status_label)
        
        display_initialized = True
        print("Display initialized")
        
    except Exception as e:
        print(f"Display initialization failed: {e}")
        display_initialized = False
else:
    display_initialized = False

# Main loop variables
last_sample_time = time.monotonic()
last_display_update = time.monotonic()
sample_count = 0

print("Starting main loop...")

while True:
    current_time = time.monotonic()
    
    # High-speed sampling
    if current_time - last_sample_time >= SAMPLE_INTERVAL:
        try:
            # Read sensor values
            voltage = ina260.voltage
            current = ina260.current
            power = ina260.power
            
            # Log to SD card
            if sd_available:
                try:
                    with open(LOG_FILE, "a") as f:
                        f.write(f"{current_time:.3f},{voltage:.3f},{current:.2f},{power:.2f}\n")
                    sample_count += 1
                except Exception as e:
                    print(f"Error writing to SD card: {e}")
                    sd_available = False
            
            # Update display at slower rate
            if display_initialized and (current_time - last_display_update >= DISPLAY_UPDATE_INTERVAL):
                voltage_label.text = f"Voltage: {voltage:.2f}V"
                current_label.text = f"Current: {current:.1f}mA"
                power_label.text = f"Power: {power:.1f}mW"
                
                if sd_available:
                    status_label.text = f"Samples: {sample_count}"
                else:
                    status_label.text = "SD: Error"
                
                last_display_update = current_time
            
            last_sample_time = current_time
            
        except Exception as e:
            print(f"Error reading sensor: {e}")
            if display_initialized:
                status_label.text = "Sensor Error"
            time.sleep(1)
    
    # Small delay to prevent busy-waiting
    time.sleep(0.001)
