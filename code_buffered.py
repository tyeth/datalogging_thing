"""
Alternative implementation with buffered logging
This version uses an in-memory buffer to reduce SD write frequency
and improve sampling speed.

Note: INA260 does not have hardware FIFO, so we implement a software buffer.
For sensors with hardware FIFO, refer to sensor-specific documentation.
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

try:
    from adafruit_st7789 import ST7789
    display_available = True
except ImportError:
    display_available = False

# Configuration
SAMPLE_INTERVAL = 0.001  # 1ms target (actual rate depends on I2C/sensor speed)
BUFFER_SIZE = 100  # Number of samples to buffer before writing to SD
LOG_FILE = "/sd/datalog.csv"
DISPLAY_UPDATE_INTERVAL = 0.5

# Initialize I2C bus at maximum speed
i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)

# Initialize INA260 for maximum speed
ina260 = INA260(i2c)
ina260.averaging_count = 1  # No averaging
ina260.current_conversion_time = 0  # 140us (fastest)
ina260.voltage_conversion_time = 0  # 140us (fastest)

print("INA260 configured for high-speed sampling")

# Initialize SD card
try:
    spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
    cs = digitalio.DigitalInOut(board.D10)
    sdcard = sdcardio.SDCard(spi, cs)
    vfs = storage.VfsFat(sdcard)
    storage.mount(vfs, "/sd")
    sd_available = True
    print("SD card mounted")
    
    with open(LOG_FILE, "w") as f:
        f.write("timestamp,voltage_V,current_mA,power_mW\n")
    print(f"Log file created: {LOG_FILE}")
    
except Exception as e:
    print(f"SD card error: {e}")
    sd_available = False

# Initialize Display (same as main code)
if display_available:
    try:
        displayio.release_displays()
        display_spi = busio.SPI(board.SCK, board.MOSI)
        display_cs = digitalio.DigitalInOut(board.D5)
        display_dc = digitalio.DigitalInOut(board.D6)
        display_rst = digitalio.DigitalInOut(board.D9)
        
        display_bus = displayio.FourWire(
            display_spi, command=display_dc, chip_select=display_cs, reset=display_rst
        )
        
        display = ST7789(display_bus, width=240, height=135, rowstart=40, colstart=53, rotation=270)
        
        splash = displayio.Group()
        display.root_group = splash
        
        title_label = label.Label(terminalio.FONT, text="Buffered Logging", color=0xFFFFFF, x=10, y=10)
        voltage_label = label.Label(terminalio.FONT, text="V: ----.-V", color=0x00FF00, x=10, y=40)
        current_label = label.Label(terminalio.FONT, text="I: ----.-mA", color=0x00FFFF, x=10, y=70)
        rate_label = label.Label(terminalio.FONT, text="Rate: ---Hz", color=0xFFFF00, x=10, y=100)
        buffer_label = label.Label(terminalio.FONT, text="Buf: 0/100", color=0xFF00FF, x=10, y=130)
        
        splash.append(title_label)
        splash.append(voltage_label)
        splash.append(current_label)
        splash.append(rate_label)
        splash.append(buffer_label)
        
        display_initialized = True
        print("Display initialized")
    except Exception as e:
        print(f"Display error: {e}")
        display_initialized = False
else:
    display_initialized = False

# Data buffer
data_buffer = []
last_sample_time = time.monotonic()
last_display_update = time.monotonic()
last_rate_calc = time.monotonic()
sample_count = 0
rate_sample_count = 0
current_rate = 0

print("Starting buffered logging loop...")

while True:
    current_time = time.monotonic()
    
    # High-speed sampling
    try:
        # Read sensor
        voltage = ina260.voltage
        current = ina260.current
        power = ina260.power
        
        # Add to buffer
        data_buffer.append((current_time, voltage, current, power))
        sample_count += 1
        rate_sample_count += 1
        
        # Calculate actual sampling rate
        if current_time - last_rate_calc >= 1.0:
            current_rate = rate_sample_count / (current_time - last_rate_calc)
            rate_sample_count = 0
            last_rate_calc = current_time
        
        # Write buffer to SD when full
        if len(data_buffer) >= BUFFER_SIZE and sd_available:
            try:
                with open(LOG_FILE, "a") as f:
                    for timestamp, v, i, p in data_buffer:
                        f.write(f"{timestamp:.3f},{v:.3f},{i:.2f},{p:.2f}\n")
                data_buffer = []  # Clear buffer
            except Exception as e:
                print(f"SD write error: {e}")
                sd_available = False
        
        # Update display periodically
        if display_initialized and (current_time - last_display_update >= DISPLAY_UPDATE_INTERVAL):
            voltage_label.text = f"V: {voltage:.2f}V"
            current_label.text = f"I: {current:.1f}mA"
            rate_label.text = f"Rate: {current_rate:.0f}Hz"
            buffer_label.text = f"Buf: {len(data_buffer)}/{BUFFER_SIZE}"
            last_display_update = current_time
        
        last_sample_time = current_time
        
    except Exception as e:
        print(f"Sampling error: {e}")
        time.sleep(0.1)
    
    # Minimal delay for timing
    time.sleep(SAMPLE_INTERVAL)
