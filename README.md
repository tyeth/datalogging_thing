# CircuitPython High-Speed Datalogging System

A CircuitPython project for high-speed voltage and current monitoring using the Adafruit INA260 sensor, with SD card logging and real-time display.

## Features

- **High-speed sampling** from INA260 sensor (up to 100 samples/second)
- **SD card logging** via Adalogger FeatherWing
- **Real-time display** using displayio (CircuitPython v10 compatible)
- **Voltage range**: Up to 36V (INA260)
- **Current range**: ±15A (INA260)

## Hardware Requirements

### Required Components:
1. **Microcontroller**: Adafruit Feather M4 Express or similar CircuitPython-compatible board
2. **Sensor**: Adafruit INA260 High or Low Side Voltage, Current, Power Sensor
   - I2C address: 0x40 (default)
   - Measures voltage, current, and power
   - Supports fast conversion times (140μs minimum)
3. **SD Card Logger**: Adafruit Adalogger FeatherWing
   - Provides SD card slot via SPI
   - Stacks on top of Feather
4. **Display**: One of the following:
   - Adafruit 1.14" 240x135 Color TFT Display (ST7789)
   - Adafruit TFT FeatherWing (ILI9341 or ST7735)
   - Any displayio-compatible display

### Hardware Connections:

#### INA260 Sensor (I2C):
- **VIN** → 3.3V
- **GND** → GND
- **SCL** → SCL (I2C clock)
- **SDA** → SDA (I2C data)

#### Adalogger FeatherWing:
- Stacks directly onto Feather board
- Uses SPI pins (SCK, MOSI, MISO)
- CS on pin D10 (default)

#### Display (if using 1.14" TFT breakout):
- **VIN** → 3.3V or 5V
- **GND** → GND
- **SCK** → SCK (SPI clock, shared with SD card)
- **MOSI** → MOSI (SPI data, shared with SD card)
- **CS** → D5
- **DC** → D6
- **RST** → D9
- **Backlight** → 3.3V (optional: connect to a PWM pin for dimming)

*Note: Pin assignments can be adjusted in code.py based on your specific setup*

## Software Setup

### 1. Install CircuitPython

1. Download CircuitPython v10.x from [circuitpython.org](https://circuitpython.org/downloads)
2. Install it on your Feather board following the installation guide
3. The board will appear as a USB drive named `CIRCUITPY`

### 2. Install Required Libraries

1. Download the CircuitPython Library Bundle (matching your CircuitPython version) from [circuitpython.org/libraries](https://circuitpython.org/libraries)
2. Extract the bundle and copy these libraries to the `lib` folder on your `CIRCUITPY` drive:
   - `adafruit_ina260.mpy`
   - `adafruit_st7789.mpy`
   - `adafruit_display_text/` (entire folder)
   - `adafruit_bus_device/` (entire folder)
   - `adafruit_register/` (entire folder)

### 3. Install Project Code

1. Copy `code.py` to the root of your `CIRCUITPY` drive
2. Insert a formatted SD card into the Adalogger FeatherWing

### 4. Run the Project

- The code starts automatically when the board powers on
- Serial console (connect at 115200 baud) shows initialization messages
- Data is logged to `/sd/datalog.csv` on the SD card
- Display shows real-time voltage, current, and power readings

## Configuration

Edit `code.py` to customize settings:

```python
SAMPLE_INTERVAL = 0.01  # Sample every 10ms (100 Hz)
LOG_FILE = "/sd/datalog.csv"  # SD card log file path
DISPLAY_UPDATE_INTERVAL = 0.5  # Update display every 500ms
```

### Pin Configuration

If your display uses different pins, update these lines in `code.py`:

```python
display_cs = digitalio.DigitalInOut(board.D5)   # Chip select
display_dc = digitalio.DigitalInOut(board.D6)   # Data/command
display_rst = digitalio.DigitalInOut(board.D9)  # Reset
```

For Adalogger FeatherWing SD card CS pin:
```python
cs = digitalio.DigitalInOut(board.D10)  # SD card chip select
```

## Data Format

CSV log file includes:
- `timestamp`: Time in seconds since boot
- `voltage_V`: Voltage in volts
- `current_mA`: Current in milliamps
- `power_mW`: Power in milliwatts

Example:
```csv
timestamp,voltage_V,current_mA,power_mW
0.523,5.120,123.45,632.14
0.533,5.125,124.10,636.01
```

## Performance

- **Maximum sampling rate**: ~100 Hz (limited by I2C communication and SD write speed)
- **Sensor conversion time**: 140μs (voltage) + 140μs (current) = 280μs
- **Actual throughput**: Limited by I2C speed (400 kHz) and SD card write operations

## Troubleshooting

### SD Card Issues:
- Ensure SD card is formatted as FAT32
- Check CS pin assignment matches your board
- Verify SPI connections

### Display Not Working:
- Check pin assignments in code
- Verify correct display driver (ST7789 vs ILI9341 vs ST7735)
- Ensure display library is installed

### Sensor Not Found:
- Verify I2C connections (SDA, SCL)
- Check sensor I2C address (default 0x40)
- Run I2C scan to detect devices

### Serial Console Access:
```bash
# Linux/Mac
screen /dev/ttyACM0 115200

# Windows - use PuTTY or Tera Term
```

## Future Enhancements

Potential additions (not yet implemented):
- Button controls for start/stop logging
- Multiple log files with timestamps
- FIFO buffering for higher speed capture
- Data compression
- WiFi/Bluetooth data transmission
- Battery monitoring
- Power analysis features

## License

MIT License - Feel free to use and modify for your projects.

## Resources

- [Adafruit INA260 Guide](https://learn.adafruit.com/adafruit-ina260-current-voltage-power-sensor-breakout)
- [CircuitPython Documentation](https://docs.circuitpython.org/)
- [Adalogger FeatherWing Guide](https://learn.adafruit.com/adafruit-adalogger-featherwing)
- [DisplayIO Guide](https://learn.adafruit.com/circuitpython-display-support-using-displayio)