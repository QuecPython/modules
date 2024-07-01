# LED & Buzzer Function Module API Reference Manual

[中文](../zh/led&buzzer_API参考手册.md) | English

## Introduction

> The `LED` and `Buzzer` module functions both inherit from the `GPIOCtrl` base class, used to control the on/off state of the LED light and the Buzzer.

## API Description

> For interface descriptions, see [common_API_Reference](./common_API_Reference.md#GPIOCtrl).

## Usage Example

> Here we take the LED light as an example, and the Buzzer can be used similarly.

```python
from led import LED
from machine import Pin

# Instantiate object
yellow_led = LED()

# Add control GPIO
red_gpio = Pin(Pin.GPIO1, Pin.OUT, Pin.PULL_DISABLE, 0)
green_gpio = Pin(Pin.GPIO2, Pin.OUT, Pin.PULL_DISABLE, 0)
yellow_led.add_gpio(red_gpio)
# True
yellow_led.add_gpio(green_gpio)
# True

# Query the list of control GPIOs
yellow_led.get_gpio()
# [<GPIO(1)>, <GPIO(2)>]

# Turn on the LED
yellow_led.on()
# True

# Turn off the LED
yellow_led.off()
# True

# Start LED blinking, on for 100ms, off for 200ms, repeat 20 times
on_period = 100
off_period = 200
count = 20
yellow_led.start_flicker(on_period, off_period, count)
# True

# Stop LED blinking
yellow_led.stop_flicker()
# True
```