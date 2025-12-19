"""
Hardware Diagnostic Script
Run this to verify your hardware is connected and working properly.
Copy this to code.py temporarily to test your setup.
"""

import time
import board
import busio
import digitalio

print("=" * 50)
print("CircuitPython Hardware Diagnostic")
print("=" * 50)
print()

# Test 1: I2C Bus
print("Test 1: I2C Bus Scan")
print("-" * 30)
try:
    i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)
    while not i2c.try_lock():
        pass
    
    devices = i2c.scan()
    print(f"I2C devices found: {[hex(x) for x in devices]}")
    
    if 0x40 in devices:
        print("✓ INA260 detected at 0x40")
    else:
        print("✗ INA260 not found (expected at 0x40)")
    
    i2c.unlock()
    print()
except Exception as e:
    print(f"✗ I2C Error: {e}")
    print()

# Test 2: INA260 Sensor
print("Test 2: INA260 Sensor")
print("-" * 30)
try:
    from adafruit_ina260 import INA260
    ina260 = INA260(i2c)
    
    # Read values
    voltage = ina260.voltage
    current = ina260.current
    power = ina260.power
    
    print(f"✓ Voltage: {voltage:.3f} V")
    print(f"✓ Current: {current:.2f} mA")
    print(f"✓ Power: {power:.2f} mW")
    
    # Test configuration
    print(f"  Averaging: {ina260.averaging_count}")
    print(f"  Current conversion time: {ina260.current_conversion_time}")
    print(f"  Voltage conversion time: {ina260.voltage_conversion_time}")
    print()
    
except ImportError:
    print("✗ adafruit_ina260 library not found")
    print("  Install from CircuitPython library bundle")
    print()
except Exception as e:
    print(f"✗ INA260 Error: {e}")
    print()

# Test 3: SD Card
print("Test 3: SD Card (SPI)")
print("-" * 30)
try:
    import sdcardio
    import storage
    
    spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
    cs = digitalio.DigitalInOut(board.D10)
    
    sdcard = sdcardio.SDCard(spi, cs)
    vfs = storage.VfsFat(sdcard)
    storage.mount(vfs, "/sd")
    
    print("✓ SD card mounted at /sd")
    
    # Test write
    test_file = "/sd/test.txt"
    with open(test_file, "w") as f:
        f.write("Hardware test OK\n")
    print(f"✓ Test write successful: {test_file}")
    
    # Test read
    with open(test_file, "r") as f:
        content = f.read()
    print(f"✓ Test read successful: {content.strip()}")
    
    storage.umount("/sd")
    print()
    
except ImportError:
    print("✗ sdcardio not available (check CircuitPython version)")
    print()
except Exception as e:
    print(f"✗ SD Card Error: {e}")
    print("  Check: SD card inserted, formatted as FAT32, CS pin D10")
    print()

# Test 4: Display
print("Test 4: Display")
print("-" * 30)
try:
    from adafruit_st7789 import ST7789
    import displayio
    import terminalio
    from adafruit_display_text import label
    
    displayio.release_displays()
    
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
    
    # Show test pattern
    splash = displayio.Group()
    display.root_group = splash
    
    test_label = label.Label(
        terminalio.FONT,
        text="Display OK!",
        color=0x00FF00,
        x=60,
        y=67
    )
    splash.append(test_label)
    
    print("✓ Display initialized")
    print("  Check display for 'Display OK!' message")
    print()
    
except ImportError as e:
    print(f"✗ Display library not found: {e}")
    print("  Install adafruit_st7789 and adafruit_display_text")
    print()
except Exception as e:
    print(f"✗ Display Error: {e}")
    print("  Check pins: CS=D5, DC=D6, RST=D9")
    print()

# Test 5: SPI Bus
print("Test 5: SPI Bus")
print("-" * 30)
try:
    spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
    while not spi.try_lock():
        pass
    
    print(f"✓ SPI bus locked successfully")
    print(f"  Frequency: 4 MHz (default)")
    
    spi.unlock()
    print()
except Exception as e:
    print(f"✗ SPI Error: {e}")
    print()

# Summary
print("=" * 50)
print("Diagnostic Complete")
print("=" * 50)
print()
print("Next steps:")
print("1. Fix any errors shown above")
print("2. Copy code.py to CIRCUITPY drive")
print("3. Reset board to start datalogging")
print()
print("For help, see README.md and HARDWARE.md")
print()

# Keep display on for viewing
print("Diagnostic running... Press CTRL+C to stop")
while True:
    time.sleep(1)
