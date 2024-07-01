# 公共模块 API 参考手册

中文 | [English](../en/common_API_Reference.md)

## 简介

该模块封装了一些公用组件与基类，方便其他模块使用。

- `option_lock` 函数锁装饰器
- `Singleton` 单例基类
- `GPIOCtrl` GPIO 控制基类

## API 说明

### option_lock

> 函数锁装饰器，用于需要上锁的函数功能。

**示例：**

```python
import _thread
from common import option_lock

_fun_lock = _thread.allocate_lock()

@option_lock(_fun_lock)
def test_lock_fun(args):
    print(args)

```

**参数：**

|参数|类型|说明|
|:---|---|---|
|thread_lock|object|线程锁实例对象|

### Singleton

> 单例基类，当需要控制一个类在整个项目中不被重复实例化，可继承该类实现类不被重复实例化的功能。

**示例：**

```python
from common import Singleton

class TestOne(Singleton):
    pass

class TestTwo(Singleton):
    pass

a = TestOne()
b = TestOne()
c = TestTwo()
d = TestTwo()

print(a)
# <TestOne object at 7e842d40>
print(b)
# <TestOne object at 7e842d40>
print(c)
# <TestTwo object at 7e842eb0>
print(d)
# <TestTwo object at 7e842eb0>
```

### <span id="GPIOCtrl">GPIOCtrl</span>

> GPIO 控制基类，该基类可用于控制 GPIO 高低电平，从而控制外设功能开关，重复开关等，如 LED 灯，Buzzer 蜂鸣器等。

#### 基类继承

**示例：**

```python
from common import GPIOCtrl

class LED(GPIOCtrl):

    def __init__(self):
        super().__init__()


class Buzzer(GPIOCtrl):

    def __init__(self):
        super().__init__()
```

#### 基类方法说明

> 以 LED 为例，对接口进行说明。

##### 实例化对象

**示例：**

```python
from led import LED

yellow_led = LED()
```

##### state

> GPIO 当前电平状态，1 高电平（LED 亮 / Buzzer 开），0 低电平（LED 灭 / Buzzer 关）。

**示例：**

```python
state = yellow_led.state
print(state)
# 1
```

**返回值：**

|数据类型|说明|
|:---|---|
|int|1 - 高电平<br>0 - 低电平|

##### add_gpio

> 添加控制当前 LED 的 GPIO，由于可能有多个 GPIO 控制一个颜色灯的情况，所以以该方式实现，如：黄色灯由红色和绿色同时点亮进行展示则需添加两个GPIO。

**示例：**

```python
from machine import Pin

red_gpio = Pin(Pin.GPIO1, Pin.OUT, Pin.PULL_DISABLE, 0)
green_gpio = Pin(Pin.GPIO2, Pin.OUT, Pin.PULL_DISABLE, 0)
yellow_led.add_gpio(red_gpio)
# True
yellow_led.add_gpio(green_gpio)
# True
```

**参数：**

|参数|类型|说明|
|:---|---|---|
|gpio|object|GPIO 对象|

**返回值：**

|数据类型|说明|
|:---|---|
|bool|`True` - 成功<br>`False` - 失败|

##### get_gpio

> 获取当前 GPIO 控制模块的所有 GPIO 对象列表。

**示例：**

```python
yellow_led.get_gpio()
# [<GPIO(1)>, <GPIO(2)>]
```

**返回值：**

|数据类型|说明|
|:---|---|
|list|GPIO 对象列表|

##### on

> 开启 GPIO 控制模块，设置所有控制 GPIO 引脚为高电平。

**示例：**

```python
yellow_led.on()
# True
```

**参数：**

无

**返回值：**

|数据类型|说明|
|:---|---|
|bool|`True` - 成功<br>`False` - 失败|

##### off

> 关闭 GPIO 控制模块，设置所有控制 GPIO 引脚为低电平。

**示例：**

```python
yellow_led.off()
# True
```

**参数：**

无

**返回值：**

|数据类型|说明|
|:---|---|
|bool|`True` - 成功<br>`False` - 失败|

##### start_flicker

> 启动 GPIO 控制模块周期性切换高低电平（LED 闪烁 / Buzzer 周期性开关）。

**示例：**

```python
on_period = 100
off_period = 200
count = 20
yellow_led.start_flicker(on_period, off_period, count)
# True
```

**参数：**

|参数|类型|说明|
|:---|---|---|
|on_period|int|高电平持续时间（LED 亮 / Buzzer 开）|
|off_period|int|低电平持续时间（LED 灭 / Buzzer 关）|
|count|int|开关次数，当设置0时，一直进行开关|

**返回值：**

|数据类型|说明|
|:---|---|
|bool|`True` - 成功<br>`False` - 失败|

##### stop_flicker

> 停止 GPIO 控制模块周期性切换高低电平（LED 闪烁 / Buzzer 周期性开关）。

**示例：**

```python
yellow_led.stop_flicker()
# True
```

**参数：**

无

**返回值：**

|数据类型|说明|
|:---|---|
|bool|`True` - 成功<br>`False` - 失败|
