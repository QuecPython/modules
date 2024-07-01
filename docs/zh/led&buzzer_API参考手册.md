# LED & Buzzer 功能模块 API 参考手册

中文 | [English](../en/led&buzzer_API_Reference.md)

## 简介

> `LED` 和 `Buzzer` 模块功能都继承于 `GPIOCtrl` 基类，用于控制 LED 灯亮灭于 Buzzer 蜂鸣器开关。

## API 说明

> 接口说明见 [common用户指导手册 GPIOCtrl](./common用户指导手册.md#GPIOCtrl)

## 使用示例

> 此处以 LED 灯为例，Buzzer 蜂鸣器以此类推

```python
from led import LED
from machine import Pin

# 实例化对象
yellow_led = LED()

# 添加控制 GPIO
red_gpio = Pin(Pin.GPIO1, Pin.OUT, Pin.PULL_DISABLE, 0)
green_gpio = Pin(Pin.GPIO2, Pin.OUT, Pin.PULL_DISABLE, 0)
yellow_led.add_gpio(red_gpio)
# True
yellow_led.add_gpio(green_gpio)
# True

# 查询获取控制 GPIO 列表
yellow_led.get_gpio()
# [<GPIO(1)>, <GPIO(2)>]

# LED 开启
yellow_led.on()
# True

# LED 关闭
yellow_led.off()
# True

# 启动 LED 闪烁, 亮 100ms, 灭 200ms, 亮灭重复 20 次
on_period = 100
off_period = 200
count = 20
yellow_led.start_flicker(on_period, off_period, count)
# True

# 关闭 LED 闪烁
yellow_led.stop_flicker()
# True
```
