# 温湿度传感器功能模块 用户指导手册

## 简介

> 该模块功能用于通过温湿度传感器获取设备温度与湿度信息

## 使用说明

### 1. 模块初始化

```python
from temp_humidity_sensor import TempHumiditySensor

temp_humidity_obj = TempHumiditySensor()
```

### 2. 开启(校准)传感器

```python
on_res = temp_humidity_obj.on()
print(on_res)
# True
```

### 3. 读取设备温度与湿度信息

```python
temperature, humidity = temp_humidity_obj.read()
print(temperature, humidity)
# 28.86, 41.36
```

### 4. 关闭(重置)传感器

```python
off_res = temp_humidity_obj.off()
print(off_res)
# True
```

## API说明

### LED

#### 导入初始化

示例:

```python
from temp_humidity_sensor import TempHumiditySensor

temp_humidity_obj = TempHumiditySensor()
```

#### on 开启(校准)传感器

示例:

```python
on_res = temp_humidity_obj.on()
print(on_res)
# True
```

参数:

无

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|

#### off 关闭(重置)传感器

示例:

```python
off_res = temp_humidity_obj.off()
print(off_res)
# True
```

参数:

无

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|

#### read 读取设备温度与湿度信息

示例:

```python
temperature, humidity = temp_humidity_obj.read()
print(temperature, humidity)
# 28.86, 41.36
```

参数:

无

返回值:

|数据类型|说明|
|:---|---|
|TUPLE|元素1为温度, 元素2为湿度, 两个数值都为浮点型, 获取失败时对应数值为None|
