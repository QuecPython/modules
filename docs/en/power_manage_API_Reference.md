# Low Power Management Module API Reference Manual

[中文](../zh/power_manage_API参考手册.md) | English

## Introduction

This module is mainly used to control the low power mode of the device. QuecPython supports different low power modes depending on the device, primarily including the following two low power modes:

- Sleep mode
- PSM mode

## API Description

### PMLock

> This method implements the acquisition and release of sleep locks, making it convenient to use with Python's `with` statement.

**Example:**

```python
from power_manage import PMLock

def test():
    pm_lock = PMLock("pmlk")
    with pm_lock:
        # TODO: Do business process, when device is idle, device does not enter sleep.
        pass
```

**Parameters:**

| Parameter | Type | Description |
|:---|---|---|
| lock_name | str | Name of the sleep lock, must be unique, maximum length of 8 characters |

### PowerManage

#### Initialize Module

**Example:**

```python
from power_manage import PowerManage

power_manage = PowerManage()
```

### PowerManage.autosleep

> Enable or disable the device's sleep mode.

**Example:**

```python
net_manage.autosleep(1)
# True
```

**Parameters:**

| Parameter | Type | Description |
|:---|---|---|
| val | int | 0 - Disable sleep mode<br>1 - Enable sleep mode |

**Return Value:**

| Data Type | Description |
|:---|---|
| bool | `True` - Success<br>`False` - Failure |

### PowerManage.set_psm

> Set the device's PSM (Power Saving Mode).

**Example:**

```python
net_manage.set_psm(mode=1, tau=3600, act=5)
# True
```

**Parameters:**

| Parameter | Type | Description |
|:---|---|---|
| mode | int | 0 - Disable PSM<br>1 - Enable PSM<br>When this parameter is 0, `tau` and `act` can be omitted |
| tau | int | Duration of sleep, value of the T3412 timer in seconds |
| act | int | Time to enter sleep, value of the T3324 timer in seconds |

**Return Value:**

| Data Type | Description |
|:---|---|
| bool | `True` - Success<br>`False` - Failure |

### PowerManage.set_hibernatea

> Force the device into PSM sleep. This method is currently only applicable to EC800E R02 firmware version.

**Example:**

```python
net_manage.set_hibernatea()
# True
```

**Parameters:**

None

**Return Value:**

| Data Type | Description |
|:---|---|
| bool | `True` - Success<br>`False` - Failure |

## Usage Example

```python
from power_manage import PowerManage

# Initialize the module
power_manage = PowerManage()

# Enable sleep mode
power_manage.autosleep(1)
# True

# Disable sleep mode
power_manage.autosleep(0)
# True

# Enable PSM
net_manage.set_psm(mode=1, tau=3600, act=5)
# True

# Disable PSM
net_manage.set_psm(mode=0)
# True

# Force PSM sleep
net_manage.set_hibernatea()
# True
```