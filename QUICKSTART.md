# Quick Start Guide

Get your INA260 datalogging system running in 5 minutes!

## What You Need

- [ ] Adafruit Feather M4 Express (or compatible)
- [ ] Adafruit INA260 sensor
- [ ] Adalogger FeatherWing
- [ ] Display (1.14" TFT or TFT FeatherWing)
- [ ] Formatted SD card (FAT32)
- [ ] USB cable

## 5-Minute Setup

### Step 1: Install CircuitPython (2 min)

1. Download CircuitPython 10.x from https://circuitpython.org/board/feather_m4_express/
2. Double-tap RESET button on Feather → appears as `FEATHERBOOT`
3. Drag the downloaded .UF2 file onto `FEATHERBOOT`
4. Board reboots as `CIRCUITPY` ✓

### Step 2: Install Libraries (1 min)

1. Download library bundle from https://circuitpython.org/libraries
2. Extract and copy these to `CIRCUITPY/lib/`:
   ```
   lib/
   ├── adafruit_ina260.mpy
   ├── adafruit_st7789.mpy
   ├── adafruit_display_text/
   ├── adafruit_bus_device/
   └── adafruit_register/
   ```

### Step 3: Deploy Code (1 min)

1. Copy `code.py` to root of `CIRCUITPY`
2. Insert SD card into Adalogger
3. Board auto-runs! ✓

### Step 4: Wire Hardware (1 min)

**INA260 to Feather:**
```
INA260    →    Feather
VIN       →    3.3V
GND       →    GND
SCL       →    SCL
SDA       →    SDA
```

**Display (if breakout):**
```
Display   →    Feather
VIN       →    3.3V
GND       →    GND
SCK       →    SCK
MOSI      →    MOSI
CS        →    D5
DC        →    D6
RST       →    D9
```

### Step 5: Test! (30 sec)

1. Open serial console (115200 baud)
2. Check for "INA260 initialized" ✓
3. Check for "SD card mounted successfully" ✓
4. Check display shows values ✓
5. Verify SD card has `datalog.csv` ✓

## Expected Output

**Serial Console:**
```
INA260 initialized
Conversion time: 0, 0
SD card mounted successfully
Log file created: /sd/datalog.csv
Display initialized
Starting main loop...
```

**Display:**
```
┌──────────────────────┐
│ INA260 Monitor       │
│                      │
│ Voltage: 5.12V       │
│ Current: 123.4mA     │
│ Power: 632.1mW       │
│ Samples: 1234        │
└──────────────────────┘
```

**SD Card (datalog.csv):**
```csv
timestamp,voltage_V,current_mA,power_mW
0.523,5.120,123.45,632.14
0.533,5.125,124.10,636.01
0.543,5.118,123.89,634.15
```

## Troubleshooting

### "No module named 'adafruit_ina260'"
→ Copy `adafruit_ina260.mpy` to `lib/` folder

### "SD card initialization failed"
→ Format SD card as FAT32 (not exFAT)

### "Display initialization failed"
→ Check pin wiring, verify display library installed

### "OSError: [Errno 30] Read-only filesystem"
→ Unmount SD from computer before inserting in Adalogger

### Serial console shows nothing
→ Press CTRL+C to stop, CTRL+D to reload

## Next Steps

- **Adjust sampling rate**: Edit `SAMPLE_INTERVAL` in `code.py`
- **Change pins**: Edit pin assignments in `code.py`
- **Buffer logging**: Use `code_buffered.py` for higher speeds
- **Customize display**: Modify display labels and layout

## Data Analysis

View your logged data:

**Python:**
```python
import pandas as pd
df = pd.read_csv('datalog.csv')
print(df.describe())
df.plot(x='timestamp', y=['voltage_V', 'current_mA'])
```

**Excel/LibreOffice:**
1. Open `datalog.csv`
2. Create charts from columns
3. Analyze power consumption patterns

## Support

- Read `README.md` for full documentation
- Check `HARDWARE.md` for wiring details
- Visit https://learn.adafruit.com for guides

## Pro Tips

💡 **Higher speed?** Use `code_buffered.py` for batch SD writes
💡 **Save power?** Reduce `DISPLAY_UPDATE_INTERVAL`
💡 **Multiple files?** Edit `LOG_FILE` to include date/time
💡 **Remote monitoring?** Add WiFi/BLE libraries for wireless logging

Happy logging! 📊
