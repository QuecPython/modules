# Common Module API Reference Manual

[中文](../zh/common_API参考手册.md) | English

## Introduction

This module encapsulates some common components and base classes for use by other modules.

- `option_lock` function lock decorator
- `Singleton` singleton base class
- `GPIOCtrl` GPIO control base class

## API Description

### option_lock

> Function lock decorator, used for functions that require locking.

**Example:**

```python
import _thread
from common import option_lock

_fun_lock = _thread.allocate_lock()

@option_lock(_fun_lock)
def test_lock_fun(args):
    print(args)
```

**Parameters:**

| Parameter   | Type   | Description                |
|:------------|--------|----------------------------|
| thread_lock | object | Thread lock instance object |

### Singleton

> Singleton base class. When you need to control a class so that it is not instantiated multiple times throughout the project, you can inherit this class to achieve the function of not being instantiated multiple times.

**Example:**

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

> GPIO control base class. This base class can be used to control the high and low levels of GPIO, thereby controlling peripheral functions such as switches, repetitive switches, etc., such as LED lights, Buzzer buzzers, etc.

#### Base Class Inheritance

**Example:**

```python
from common import GPIOCtrl

class LED(GPIOCtrl):

    def __init__(self):
        super().__init__()


class Buzzer(GPIOCtrl):

    def __init__(self):
        super().__init__()
```

#### Base Class Method Description

> Taking the LED as an example, the interface is explained.

##### Instantiate Object

**Example:**

```python
from led import LED

yellow_led = LED()
```

##### state

> Current GPIO level status, 1 high level (LED on / Buzzer on), 0 low level (LED off / Buzzer off).

**Example:**

```python
state = yellow_led.state
print(state)
# 1
```

**Return Value:**

| Data Type | Description            |
|:----------|------------------------|
| int       | 1 - High level<br>0 - Low level |

##### add_gpio

> Add the GPIO that controls the current LED. Since multiple GPIOs may control one color light, this method is used to achieve this. For example, a yellow light is displayed by simultaneously lighting up red and green, so two GPIOs need to be added.

**Example:**

```python
from machine import Pin

red_gpio = Pin(Pin.GPIO1, Pin.OUT, Pin.PULL_DISABLE, 0)
green_gpio = Pin(Pin.GPIO2, Pin.OUT, Pin.PULL_DISABLE, 0)
yellow_led.add_gpio(red_gpio)
# True
yellow_led.add_gpio(green_gpio)
# True
```

**Parameters:**

| Parameter | Type   | Description |
|:----------|--------|-------------|
| gpio      | object | GPIO object |

**Return Value:**

| Data Type | Description            |
|:----------|------------------------|
| bool      | `True` - Success<br>`False` - Failure |

##### get_gpio

> Get the list of all GPIO objects controlling the current GPIO module.

**Example:**

```python
yellow_led.get_gpio()
# [<GPIO(1)>, <GPIO(2)>]
```

**Return Value:**

| Data Type | Description         |
|:----------|---------------------|
| list      | List of GPIO objects |

##### on

> Turn on the GPIO control module, setting all control GPIO pins to high level.

**Example:**

```python
yellow_led.on()
# True
```

**Parameters:**

None

**Return Value:**

| Data Type | Description            |
|:----------|------------------------|
| bool      | `True` - Success<br>`False` - Failure |

##### off

> Turn off the GPIO control module, setting all control GPIO pins to low level.

**Example:**

```python
yellow_led.off()
# True
```

**Parameters:**

None

**Return Value:**

| Data Type | Description            |
|:----------|------------------------|
| bool      | `True` - Success<br>`False` - Failure |

##### start_flicker

> Start the GPIO control module to periodically switch high and low levels (LED flickering / Buzzer periodic switching).

**Example:**

```python
on_period = 100
off_period = 200
count = 20
yellow_led.start_flicker(on_period, off_period, count)
# True
```

**Parameters:**

| Parameter  | Type | Description                                     |
|:-----------|------|-------------------------------------------------|
| on_period  | int  | High level duration (LED on / Buzzer on)        |
| off_period | int  | Low level duration (LED off / Buzzer off)       |
| count      | int  | Number of switches, set to 0 for continuous switching |

**Return Value:**

| Data Type | Description            |
|:----------|------------------------|
| bool      | `True` - Success<br>`False` - Failure |

##### stop_flicker

> Stop the GPIO control module from periodically switching high and low levels (LED flickering / Buzzer periodic switching).

**Example:**

```python
yellow_led.stop_flicker()
# True
```

**Parameters:**

None

**Return Value:**

| Data Type | Description            |
|:----------|------------------------|
| bool      | `True` - Success<br>`False` - Failure |