# LED功能模块 用户指导手册

## 简介

> 该模块功能用于控制模块LED灯的开关与周期性闪烁

## 使用说明

### 1. 模块初始化

```python
from machine import Pin
from led import LED

GPIOn = Pin.GPIO1
direction = Pin.OUT
pullMode = Pin.PULL_DISABLE
level = 0
led = LED(GPIOn, direction=direction, pullMode=pullMode, level=level)
```

### 2. 开启LED

```python
res = led.on()
```

### 3. 关闭LED

```python
res = led.off()
```

### 4. 开启LED闪烁

```python
on_period = 1000
off_period = 200
count = 10
res = led.start_flicker(on_period, off_period, count)
```

### 5. 停止LED闪烁

```python
res = led.stop_flicker()
```

### 6. 获取LED亮灭状态

```python
state = led.state
```

### 7. 获取LED闪烁状态

```python
flicker_state = led.flicker_state
```

## API说明

### LED

#### 导入初始化

示例:

```python
from machine import Pin
from led import LED

GPIOn = Pin.GPIO1
direction = Pin.OUT
pullMode = Pin.PULL_DISABLE
level = 0

led = LED(GPIOn, direction=direction, pullMode=pullMode, level=level)
```

参数:

|参数|类型|说明|
|:---|---|---|
|GPIOn|INT|引脚号|
|direction|INT|Pin.IN – 输入模式, Pin.OUT – 输出模式, 默认Pin.OUT|
|pullMode|INT|Pin.PULL_DISABLE – 浮空模式, Pin.PULL_PU – 上拉模式, Pin.PULL_PD – 下拉模式, 默认Pin.PULL_DISABLE|
|level|INT|0 - 设置引脚为低电平, 1- 设置引脚为高电平, 默认0|

#### on 开启LED

示例:

```python
res = led.on()
```

参数:

无

返回值:

无

#### off 关闭LED

示例:

```python
res = led.off()
```

参数:

无

返回值:

无

#### start_flicker 开启LED闪烁

示例:

```python
on_period = 1000
off_period = 200
count = 10
res = led.start_flicker(on_period, off_period, count)
```

参数:

|参数|类型|说明|
|:---|---|---|
|on_period|INT|LED周期闪烁亮持续时间, 单位: ms|
|off_period|INT|LED周期闪烁灭持续时间, 单位: ms|
|count|INT|闪烁次数, 当0时, 持续闪烁, 默认0|

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|

#### stop_flicker 停止LED闪烁

示例:

```python
res = led.stop_flicker()
```

参数:

无

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|

#### state 获取LED亮灭状态

示例:

```python
state = led.state
```


返回值:

|数据类型|说明|
|:---|---|
|INT|0 - 灭; 1 - 亮|

#### flicker_state 获取LED闪烁状态

示例:

```python
state = led.flicker_state
```


返回值:

|数据类型|说明|
|:---|---|
|INT|0 - 停止闪烁; 1 - 正在闪烁|
