# Battery Function Module API Reference Manual

[中文](../zh/battery_API参考手册.md) | English

## Introduction

This module is used to query the current device's battery level and voltage, as well as the device's charging status.

## API Description

### Battery

**Example:**

```python
from battery import Battery

adc_args = (adc_num, adc_period, factor)
chrg_gpion = 0
stdby_gpion = 1

battery = Battery(adc_args=adc_args, chrg_gpion=chrg_gpion, stdby_gpion=stdby_gpion)
```

**Parameters:**

|Parameter|Type|Description|
|:---|---|---|
|adc_args|tuple|Element 1: [ADC Channel](https://python.quectel.com/doc/API_reference/zh/peripherals/misc.ADC.html#%E5%B8%B8%E9%87%8F)<br>Element 2: Number of ADC cyclic reads<br>Element 3: Calculation factor<br>Optional|
|chrg_gpion|int|CHRG (Pin 1): Open-drain output charging status indicator. Optional|
|stdby_gpion|int|STDBY (Pin 5): Battery charging completion indicator. Optional|

### set_charge_callback

> Charging event callback function.

**Example:**

```python
def charge_callback(charge_status):
    print(charge_status)

res = battery.set_charge_callback(charge_callback)
```

**Parameters:**

|Parameter|Type|Description|
|:---|---|---|
|charge_callback|function|Charging event callback function. The callback function parameter is the device charging status:<br>0 - Not charging<br>1 - Charging<br>2 - Charging complete|

**Return Value:**

|Data Type|Description|
|:---|---|
|bool|`True` - Success<br>`False` - Failure|

### set_temp

> Set the working environment temperature of the current device, used to calculate the device's battery level.

**Example:**

```python
res = battery.set_temp(20)
```

**Parameters:**

|Parameter|Type|Description|
|:---|---|---|
|temp|int/float|Temperature value, in degrees Celsius|

**Return Value:**

|Data Type|Description|
|:---|---|
|bool|`True` - Success<br>`False` - Failure|

### voltage

> Query battery voltage.

**Example:**

```python
battery.voltage
# 523
```

**Return Value:**

|Data Type|Description|
|:---|---|
|int|Battery voltage, in millivolts|

### energy

> Query battery level.

**Example:**

```python
res = battery.energy
# 100
```

**Return Value:**

|Data Type|Description|
|:---|---|
|int|Battery level percentage, 0 ~ 100|

### charge_status

> Query charging status.

**Example:**

```python
battery.charge_status
# 1
```

**Return Value:**

|Data Type|Description|
|:---|---|
|int|0 - Not charging<br>1 - Charging<br>2 - Charging complete|

## Usage Example

```python
from battery import Battery

# Instantiate object
adc_args = (adc_num, adc_period, factor)
chrg_gpion = 0
stdby_gpion = 1
battery = Battery(adc_args=adc_args, chrg_gpion=chrg_gpion, stdby_gpion=stdby_gpion)

def charge_callback(charge_status):
    print(charge_status)

# Set charging status callback function
battery.set_charge_callback(charge_callback)
# True

# Set the current device temperature
temp = 30
battery.set_temp(temp)
# True

# Get the current battery voltage
battery.voltage
# 3000

# Get the current battery level
battery.energy
# 100

# Get the current charging status
battery.charge_status
# 1

```