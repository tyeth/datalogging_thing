# Project Summary

## CircuitPython High-Speed Datalogging System

This repository contains a complete CircuitPython implementation for high-speed voltage and current monitoring with data logging and real-time display.

## Project Files

### Core Implementation
- **`code.py`** - Main application code (100Hz sampling, SD logging, display)
- **`code_buffered.py`** - Alternative with buffered logging for higher speeds

### Documentation
- **`README.md`** - Complete project documentation
- **`QUICKSTART.md`** - 5-minute setup guide
- **`HARDWARE.md`** - Detailed wiring diagrams and assembly instructions

### Utilities
- **`diagnostic.py`** - Hardware testing and verification script
- **`examples_sensors.py`** - Examples for different INA sensors (260, 219, 3221)

### Configuration
- **`settings.toml`** - CircuitPython configuration file
- **`requirements.txt`** - Required library list
- **`.gitignore`** - Git ignore rules for CircuitPython projects

## Key Features

✅ **High-speed sampling**: Up to 100 samples/second  
✅ **INA260 sensor**: Voltage (0-36V), current (±15A), power monitoring  
✅ **SD card logging**: CSV format with timestamps  
✅ **Real-time display**: Shows voltage, current, power, and status  
✅ **CircuitPython v10**: Uses displayio for graphics  
✅ **Configurable**: Easy pin and parameter customization  
✅ **Error handling**: Graceful degradation if components unavailable  
✅ **Multiple modes**: Standard and buffered logging options  

## Hardware Components

1. **Microcontroller**: Adafruit Feather M4 Express (or compatible)
2. **Sensor**: Adafruit INA260 High/Low Side Power Monitor
3. **Logger**: Adalogger FeatherWing (SD card + RTC)
4. **Display**: 1.14" 240x135 TFT (ST7789) or TFT FeatherWing

## Quick Start

```bash
# 1. Install CircuitPython 10.x on your Feather
# 2. Copy libraries to /lib folder:
#    - adafruit_ina260.mpy
#    - adafruit_st7789.mpy
#    - adafruit_display_text/
#    - adafruit_bus_device/
#    - adafruit_register/
# 3. Copy code.py to CIRCUITPY drive
# 4. Wire hardware and insert SD card
# 5. Reset board - it starts automatically!
```

## Code Structure

### Main Loop (code.py)
```
Initialization:
  - I2C bus (400kHz)
  - INA260 sensor (fastest conversion)
  - SD card mount
  - Display setup

Main Loop:
  - Read sensor @ 100Hz
  - Log to CSV immediately
  - Update display @ 2Hz
  - Handle errors gracefully
```

### Buffered Mode (code_buffered.py)
```
  - Buffer 100 samples in memory
  - Batch write to SD card
  - Higher sampling rates possible
  - Shows actual sampling rate on display
```

## Data Format

CSV output with columns:
- `timestamp` - Seconds since boot (float)
- `voltage_V` - Bus voltage in volts
- `current_mA` - Current in milliamps
- `power_mW` - Power in milliwatts

Example:
```csv
timestamp,voltage_V,current_mA,power_mW
0.523,5.120,123.45,632.14
0.533,5.125,124.10,636.01
```

## Configuration Options

### Sampling Rate
```python
SAMPLE_INTERVAL = 0.01  # 100Hz (10ms)
```

### Display Update Rate
```python
DISPLAY_UPDATE_INTERVAL = 0.5  # 2Hz (500ms)
```

### Pin Assignments
```python
# SD Card
cs = board.D10

# Display
display_cs = board.D5
display_dc = board.D6
display_rst = board.D9
```

## Performance Characteristics

| Metric | Value |
|--------|-------|
| Sampling Rate | 100 Hz (configurable) |
| Sensor Conversion | 280 μs (140μs × 2) |
| I2C Speed | 400 kHz |
| Display Update | 2 Hz |
| Buffer Size | 100 samples (buffered mode) |
| Voltage Range | 0-36V |
| Current Range | ±15A |
| Resolution | 1.25mV, 1.25mA |

## Testing

Run diagnostics:
```bash
# Copy diagnostic.py to code.py temporarily
# Connect to serial console (115200 baud)
# View test results for each component
```

Tests verify:
- ✓ I2C bus scan
- ✓ INA260 sensor readings
- ✓ SD card mount and write
- ✓ Display initialization
- ✓ SPI bus operation

## Future Enhancements

Possible additions (not implemented):
- [ ] Button controls (start/stop logging)
- [ ] RTC timestamping
- [ ] WiFi/Bluetooth transmission
- [ ] Data compression
- [ ] Multiple log files
- [ ] Power analysis features
- [ ] Battery monitoring
- [ ] Trigger-based capture

## Support

- **Documentation**: See README.md and HARDWARE.md
- **Examples**: Check examples_sensors.py
- **Troubleshooting**: Run diagnostic.py
- **Adafruit Learning System**: https://learn.adafruit.com

## License

MIT License - Free to use and modify

## Version

Initial Release - December 2025

---

**Ready to use!** Copy `code.py` to your CircuitPython device and start logging. 📊
