# led&Buzzer 功能模块 用户指导手册

## 简介

> `LED`和`Buzzer`模块功能都继承于`GPIOCtrl`基类, 用于控制LED灯亮灭于Buzzer蜂鸣器开关。

## API说明

> 接口说明见[`common.py`用户指导手册 GPIOCtrl](./common用户指导手册.md#gpioctrl-gpio控制基类)

## 使用示例

> 此处以LED灯为例, Buzzer蜂鸣器以此类推

```python
from led import LED
from machine import Pin

# 实例化对象
yellow_led = LED()

# 添加控制GPIO
red_gpio = Pin(Pin.GPIO1, Pin.OUT, Pin.PULL_DISABLE, 0)
green_gpio = Pin(Pin.GPIO2, Pin.OUT, Pin.PULL_DISABLE, 0)
yellow_led.add_gpio(red_gpio)
# True
yellow_led.add_gpio(green_gpio)
# True

# 查询获取控制GPIO列表
yellow_led.get_gpio()
# [<GPIO(1)>, <GPIO(2)>]

# LED开启
yellow_led.on()
# True

# LED关闭
yellow_led.off()
# True

# 启动LED闪烁, 亮100ms, 灭200ms, 亮灭重复20次
on_period = 100
off_period = 200
count = 20
yellow_led.start_flicker(on_period, off_period, count)
# True

# 关闭LED闪烁
yellow_led.stop_flicker()
# True
```
