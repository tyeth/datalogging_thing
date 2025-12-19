"""
Example: Using different INA sensors
This file shows how to adapt the code for various INA sensors.

IMPORTANT: This is a REFERENCE FILE with multiple code examples.
Each example shows a different sensor or technique. When using an example:
1. Copy the specific example you need
2. Add the required imports listed in comments
3. Paste into your code.py file

Common imports used throughout (add these to your code.py):
    import time
    import board
    import busio
    import digitalio
    from adafruit_ina260 import INA260

Note: Examples reuse variable names (i2c, sensor) for clarity.
When copying to your code, ensure you have the necessary imports.
"""

# ==============================================================================
# EXAMPLE 1: INA260 (Default - recommended)
# Range: 0-36V, ±15A
# Built-in shunt resistor
# ==============================================================================

# Required imports: board, busio
from adafruit_ina260 import INA260

i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)
sensor = INA260(i2c)
sensor.averaging_count = 1
sensor.current_conversion_time = 0  # 140us
sensor.voltage_conversion_time = 0  # 140us

# Read values
voltage = sensor.voltage  # Volts
current = sensor.current  # Milliamps
power = sensor.power      # Milliwatts


# ==============================================================================
# EXAMPLE 2: INA219 (High side, up to 26V)
# Range: 0-26V, ±3.2A (with 0.1Ω shunt)
# Requires external shunt resistor
# ==============================================================================

# Required imports: board, busio
from adafruit_ina219 import INA219

i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)
sensor = INA219(i2c)

# Read values
bus_voltage = sensor.bus_voltage        # Volts
shunt_voltage = sensor.shunt_voltage    # Volts
current = sensor.current                # Milliamps (may need scaling)
power = sensor.power                    # Milliwatts

# Calculate total voltage (for high-side sensing)
voltage = bus_voltage + shunt_voltage


# ==============================================================================
# EXAMPLE 3: INA3221 (Triple channel, up to 26V per channel)
# Range: 0-26V per channel, ±3.2A per channel
# Three independent channels
# ==============================================================================

# Required imports: board, busio
from adafruit_ina3221 import INA3221

i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)
sensor = INA3221(i2c)

# Enable channels (0, 1, 2)
sensor.enable_channel(0)
sensor.enable_channel(1)
sensor.enable_channel(2)

# Read from channel 0
voltage_ch0 = sensor.bus_voltage(0)   # Volts
current_ch0 = sensor.current(0)       # Milliamps

# Read from channel 1
voltage_ch1 = sensor.bus_voltage(1)
current_ch1 = sensor.current(1)

# Read from channel 2
voltage_ch2 = sensor.bus_voltage(2)
current_ch2 = sensor.current(2)

# For logging all channels, modify the data format:
# CSV header: "timestamp,ch0_V,ch0_mA,ch1_V,ch1_mA,ch2_V,ch2_mA\n"


# ==============================================================================
# EXAMPLE 4: INA260 with Alert Pin
# Use the alert pin to trigger sampling instead of polling
# ==============================================================================

# Required imports: board, busio, digitalio
from adafruit_ina260 import INA260, AlertLimit

i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)
sensor = INA260(i2c)

# Set up alert on conversion ready (data ready)
sensor.alert_limit = AlertLimit.CONVERSION_READY
sensor.alert_function_flag = True

# Connect INA260 ALERT pin to Feather digital input
alert_pin = digitalio.DigitalInOut(board.D11)
alert_pin.direction = digitalio.Direction.INPUT

# In main loop:
while True:
    if not alert_pin.value:  # Alert is active low
        voltage = sensor.voltage
        current = sensor.current
        power = sensor.power
        # Log data...


# ==============================================================================
# EXAMPLE 5: High-speed continuous mode with asyncio
# NOTE: asyncio is not available in standard CircuitPython!
# This requires a special build or CircuitPython 8.0+ with asyncio support.
# For most users, use timer-based approach in code_buffered.py instead.
# ==============================================================================

# Required imports: time, board, busio
# Optional (requires special build): asyncio
try:
    import asyncio
    ASYNCIO_AVAILABLE = True
except ImportError:
    ASYNCIO_AVAILABLE = False
    print("asyncio not available - use standard timer-based approach")

from adafruit_ina260 import INA260, Mode

i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)
sensor = INA260(i2c)
sensor.averaging_count = 1
sensor.mode = Mode.CONTINUOUS  # Continuous conversion

LOG_FILE = "/sd/datalog.csv"  # Define log file path
data_queue = []

if ASYNCIO_AVAILABLE:
    async def sample_sensor():
        while True:
            voltage = sensor.voltage
            current = sensor.current
            power = sensor.power
            data_queue.append((time.monotonic(), voltage, current, power))
            await asyncio.sleep(0.001)  # 1ms

    async def write_to_sd():
        while True:
            if len(data_queue) > 0:
                # Write batch to SD
                with open(LOG_FILE, "a") as f:
                    for timestamp, v, i, p in data_queue:
                        f.write(f"{timestamp:.3f},{v:.3f},{i:.2f},{p:.2f}\n")
                data_queue.clear()
            await asyncio.sleep(1.0)  # Write every second

    async def main():
        await asyncio.gather(
            sample_sensor(),
            write_to_sd()
        )

    # Only run if asyncio is available
    asyncio.run(main())


# ==============================================================================
# EXAMPLE 6: Different I2C addresses (for multiple sensors)
# INA260 default: 0x40
# Can be changed with A0/A1 solder jumpers to 0x41, 0x44, 0x45
# ==============================================================================

# Required imports: board, busio
from adafruit_ina260 import INA260

i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)

# Two sensors on same I2C bus
sensor1 = INA260(i2c, address=0x40)  # Default address
sensor2 = INA260(i2c, address=0x41)  # Modified address (A0 jumper)

# Read from both
voltage1 = sensor1.voltage
current1 = sensor1.current

voltage2 = sensor2.voltage
current2 = sensor2.current

# Log both to same file
# CSV header: "timestamp,v1_V,i1_mA,v2_V,i2_mA\n"


# ==============================================================================
# NOTES
# ==============================================================================

"""
Choosing the right sensor:

INA260:
+ Easy to use (built-in shunt)
+ Good accuracy
+ 0-36V range
- Limited to 15A

INA219:
+ Up to 26V
+ Configurable gain
- Requires external shunt
- Lower maximum current

INA3221:
+ Three channels
+ Useful for multi-rail monitoring
- Lower per-channel current
- More complex setup

For 60V+ applications, consider:
- INA226 (up to 36V on bus, but measures shunt voltage separately)
- Use voltage divider for bus voltage >36V
- External high-voltage isolation amplifier
"""
