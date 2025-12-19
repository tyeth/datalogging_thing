# Hardware Setup Guide

## Bill of Materials

### Core Components
| Item | Part Number | Description | Link |
|------|-------------|-------------|------|
| Microcontroller | Feather M4 Express | ATSAMD51 Cortex M4, 120MHz, 512KB Flash | [Adafruit #3857](https://www.adafruit.com/product/3857) |
| Sensor | INA260 | High/Low Side Current/Voltage/Power Monitor | [Adafruit #4226](https://www.adafruit.com/product/4226) |
| SD Logger | Adalogger FeatherWing | RTC + SD Card for Feather | [Adafruit #2922](https://www.adafruit.com/product/2922) |
| Display Option 1 | 1.14" TFT | 240x135 Color TFT Breakout | [Adafruit #4383](https://www.adafruit.com/product/4383) |
| Display Option 2 | TFT FeatherWing | 2.4" or 3.5" TFT FeatherWing | [Adafruit #3315](https://www.adafruit.com/product/3315) |

### Alternative INA Sensors (60V+ range)
- **INA260**: ±15A, 0-36V (most common, built-in 2mΩ shunt)
- **INA219**: High side DC current sensor, 0-26V
- **INA3221**: Triple-channel, 0-26V per channel

*Note: INA260 is recommended for this project due to integrated shunt resistor and ease of use*

## Wiring Diagrams

### Stack Configuration (Recommended)
```
┌─────────────────────┐
│   Display           │  (If using TFT FeatherWing)
│   FeatherWing       │
├─────────────────────┤
│   Adalogger         │
│   FeatherWing       │
├─────────────────────┤
│   Feather M4        │
│   Express           │
└─────────────────────┘
```

### I2C Connections for INA260
```
INA260 Breakout          Feather M4
┌───────────┐           ┌──────────┐
│ VIN       │─────────→ │ 3.3V     │
│ GND       │─────────→ │ GND      │
│ SCL       │─────────→ │ SCL      │
│ SDA       │─────────→ │ SDA      │
└───────────┘           └──────────┘
```

### Display Connections (if using 1.14" Breakout)
```
Display Breakout         Feather M4
┌───────────┐           ┌──────────┐
│ VIN       │─────────→ │ 3.3V     │
│ GND       │─────────→ │ GND      │
│ SCK       │─────────→ │ SCK      │
│ MOSI      │─────────→ │ MOSI     │
│ CS        │─────────→ │ D5       │
│ DC        │─────────→ │ D6       │
│ RST       │─────────→ │ D9       │
│ LITE      │─────────→ │ 3.3V     │
└───────────┘           └──────────┘
```

## Power Considerations

### Current Monitoring Setup
The INA260 can be wired in two configurations:

#### High-Side Sensing (Recommended)
```
[Power Source] → [INA260 IN+] → [INA260 IN-] → [Load]
                      ↑
                   [Device GND] ← [INA260 GND]
```

#### Low-Side Sensing
```
[Power Source] → [Load] → [INA260 IN+] → [INA260 IN-] → [GND]
                                              ↑
                                         [INA260 GND]
```

### Power Budget
- Feather M4: ~50mA (active) + ~0.1mA (deep sleep)
- INA260: ~1mA
- Display: ~20-50mA (depending on brightness)
- SD Card: ~100mA (write) / ~20mA (idle)
- **Total**: ~150-200mA typical

## Pin Usage Reference

### Feather M4 Express Default Pins

| Pin | Function | Used By |
|-----|----------|---------|
| SCL | I2C Clock | INA260 |
| SDA | I2C Data | INA260 |
| SCK | SPI Clock | SD Card, Display |
| MOSI | SPI MOSI | SD Card, Display |
| MISO | SPI MISO | SD Card |
| D5 | GPIO | Display CS |
| D6 | GPIO | Display DC |
| D9 | GPIO | Display RST |
| D10 | GPIO | SD Card CS |

*Note: Adalogger FeatherWing typically uses D10 for SD CS*

## Assembly Instructions

1. **Stack FeatherWings**: 
   - Place Adalogger FeatherWing on top of Feather M4
   - Ensure all pins are aligned and seated properly
   - If using TFT FeatherWing, stack it on top

2. **Connect INA260**:
   - Use STEMMA QT cable (if available) or solder headers
   - Connect to I2C port on Feather or Adalogger

3. **Connect Display** (if using breakout):
   - Solder headers to display breakout
   - Wire according to diagram above
   - Use breadboard or proto area for connections

4. **Insert SD Card**:
   - Format as FAT32
   - Insert into Adalogger slot

5. **Power**:
   - USB cable for development
   - LiPo battery (3.7V) via JST connector for portable use

## Firmware Upload

1. Enter bootloader mode:
   - Double-tap RESET button on Feather
   - Board appears as `FEATHERBOOT` drive

2. Install CircuitPython:
   - Drag and drop CircuitPython UF2 file
   - Board reboots as `CIRCUITPY`

3. Install libraries:
   - Copy required .mpy files to `/lib` folder

4. Deploy code:
   - Copy `code.py` to root directory
   - Board automatically resets and runs

## Testing

### Step-by-step Verification

1. **Test I2C**:
   ```python
   import board
   import busio
   i2c = busio.I2C(board.SCL, board.SDA)
   while not i2c.try_lock():
       pass
   print([hex(x) for x in i2c.scan()])
   i2c.unlock()
   ```
   Should show: `['0x40']` (INA260 address)

2. **Test INA260**:
   ```python
   from adafruit_ina260 import INA260
   ina = INA260(i2c)
   print(f"Voltage: {ina.voltage}V")
   print(f"Current: {ina.current}mA")
   ```

3. **Test SD Card**:
   - Check for log file creation
   - Verify data is being written

4. **Test Display**:
   - Verify text appears
   - Check values update

## Troubleshooting

### Common Issues

**"No I2C device found"**
- Check wiring
- Verify power to INA260
- Try I2C scan code

**"SD card mount failed"**
- Ensure card is FAT32
- Check CS pin (D10)
- Try different SD card

**Display shows nothing**
- Check backlight connection
- Verify pin assignments
- Test with simpler displayio example

**High current consumption**
- Disable display backlight when not needed
- Use deep sleep between samples
- Check for shorts

## Safety Notes

⚠️ **Important Safety Information**

- Maximum voltage: 36V for INA260
- Maximum current: ±15A for INA260
- Do not exceed sensor ratings
- Use appropriate wire gauge for high current (>1A)
- Ensure proper heatsinking for high power measurements
- Double-check polarity before connecting power
- Use isolated power supplies when necessary

## Further Reading

- [INA260 Datasheet](https://www.ti.com/lit/ds/symlink/ina260.pdf)
- [ATSAMD51 Datasheet](https://www.microchip.com/wwwproducts/en/ATSAMD51J19A)
- [CircuitPython Core Modules](https://docs.circuitpython.org/en/latest/shared-bindings/index.html)
