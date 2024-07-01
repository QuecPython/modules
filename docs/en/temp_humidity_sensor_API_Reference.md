# Temperature and Humidity Sensor Function Module API Reference Manual

[中文](../zh/temp_humidity_sensor_API参考手册.md) | English

## Introduction

> This module function is used to obtain device temperature and humidity information through the temperature and humidity sensor.

## API Description

### TempHumiditySensor

**Example:**

```python
from machine import I2C
from temp_humidity_sensor import TempHumiditySensor

i2cn = I2C.I2C1
mode = I2C.FAST_MODE
calibration = 0xE1
start_measurement = 0xAC
reset = 0xBA
i2c_addr = 0x38

temp_humidity_obj = TempHumiditySensor(
    i2cn=I2C.I2C1,
    mode=I2C.FAST_MODE,
    calibration=calibration,
    start_measurement=start_measurement,
    reset=reset,
    i2c_addr=i2c_addr
)
```

**Parameters:**

|Parameter|Type|Description|
|:---|---|---|
|i2cn|int|I2C channel index|
|mode|int|I2C operating mode<br>0 - Standard mode<br>1 - Fast mode|
|calibration|int|Calibration instruction, default: 0xE1|
|start_measurement|int|Start measurement instruction, default: 0xAC|
|reset|int|Reset instruction, default: 0xBA|
|i2c_addr|int|I2C address, default: 0x38|

### read

> Read device temperature and humidity information.

**Example:**

```python
temperature, humidity = temp_humidity_obj.read()
print(temperature, humidity)
# 28.86, 41.36
```

**Parameters:**

None

**Return Value:**

|Data Type|Description|
|:---|---|
|tuple|Element 1 is temperature, element 2 is humidity, both values are floating-point. If the retrieval fails, the corresponding value is None.|

## Usage Example

```python
from machine import I2C
from temp_humidity_sensor import TempHumiditySensor

i2cn = I2C.I2C1
mode = I2C.FAST_MODE
calibration = 0xE1
start_measurement = 0xAC
reset = 0xBA
i2c_addr = 0x38

# Initialize the function module
temp_humidity_obj = TempHumiditySensor(
    i2cn=I2C.I2C1, mode=I2C.FAST_MODE, calibration=calibration,
    start_measurement=start_measurement, reset=reset, i2c_addr=i2c_addr
)

# Read device temperature and humidity information
temperature, humidity = temp_humidity_obj.read()
print(temperature, humidity)
# 28.86 41.36
```