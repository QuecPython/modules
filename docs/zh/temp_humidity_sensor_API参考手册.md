# 温湿度传感器功能模块 API 参考手册

中文 | [English](../en/temp_humidity_sensor_API_Reference.md)

## 简介

> 该模块功能用于通过温湿度传感器获取设备温度与湿度信息。

## API 说明

### TempHumiditySensor

**示例：**

```python
from machine import I2C
from temp_humidity_sensor import TempHumiditySensor

i2cn = I2C.I2C1
mode = I2C.FAST_MODE
calibration = 0xE1
start_measurment = 0xAC
reset = 0xBA
i2c_addr = 0x38

temp_humidity_obj = TempHumiditySensor(
    i2cn=I2C.I2C1,
    mode=I2C.FAST_MODE,
    calibration=calibration,
    start_measurment=start_measurment,
    reset=reset,
    i2c_addr=i2c_addr
)
```

**参数：**

|参数|类型|说明|
|:---|---|---|
|i2cn|int|I2C 通路索引号|
|mode|int|I2C 的工作模式<br>0 - 标准模式<br>1 - 快速模式|
|calibration|int|校准指令，默认: 0xE1|
|start_measurment|int|开始测量指令，默认: 0xAC|
|reset|int|重置指令，默认: 0xBA|
|i2c_addr|int|I2C 地址，默认: 0x38|

### read

> 读取设备温度与湿度信息。

**示例：**

```python
temperature, humidity = temp_humidity_obj.read()
print(temperature, humidity)
# 28.86, 41.36
```

**参数：**

无

**返回值：**

|数据类型|说明|
|:---|---|
|tuple|元素 1 为温度，元素 2 为湿度，两个数值都为浮点型，获取失败时对应数值为 None|

## 使用示例

```python
from machine import I2C
from temp_humidity_sensor import TempHumiditySensor

i2cn = I2C.I2C1
mode = I2C.FAST_MODE
calibration = 0xE1
start_measurment = 0xAC
reset = 0xBA
i2c_addr = 0x38

# 功能模块初始化
temp_humidity_obj = TempHumiditySensor(
    i2cn=I2C.I2C1, mode=I2C.FAST_MODE, calibration=calibration,
    start_measurment=start_measurment,reset=reset, i2c_addr=i2c_addr
)

# 读取设备温度与湿度信息
temperature, humidity = temp_humidity_obj.read()
print(temperature, humidity)
# 28.86 41.36
```
