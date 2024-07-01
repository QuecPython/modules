# Network Management Module API Reference Manual

[中文](../zh/net_manage_API参考手册.md) | English

## Introduction

> This module is mainly used to control the device's network disconnection and connection, query the device's network registration result, check the device's network status, synchronize server time, and receive device network status changes through callback functions.

## API Description

### Instantiate Object

**Example:**

```python
from net_manage import NetManage

project_name = "QuecPython-Tracker"
project_version = "2.2.0"
net_manage = NetManage(project_name, project_version)
```

**Parameters:**

| Parameter       | Type | Description           |
|:----------------|------|-----------------------|
| project_name    | str  | Software project name |
| project_version | int  | Software project version |

### status

> Device network status

**Example:**

```python
net_manage.status
# True
```

**Return Value:**

| Data Type | Description                                 |
|:----------|---------------------------------------------|
| bool      | `True` - Network is normal<br>`False` - Network is abnormal |

### sim_status

> Device SIM card status

**Example:**

```python
net_manage.sim_status
# 1
```

**Return Value:**

| Data Type | Description                   |
|:----------|-------------------------------|
| int       | SIM card status enumeration value |

**SIM Card Status Enumeration Values:**

| Enumeration Value | Description                                                                 |
|:------------------|-----------------------------------------------------------------------------|
| 0                 | SIM card does not exist/removed                                             |
| 1                 | SIM is ready                                                                |
| 2                 | SIM card is locked, waiting for CHV1 password                               |
| 3                 | SIM card is blocked, needs CHV1 password unlock                             |
| 4                 | SIM card is locked due to failed SIM/USIM personalization check             |
| 5                 | SIM card is blocked due to PCK error, needs MEP password to unblock         |
| 6                 | Needs key for hidden phone book entries                                     |
| 7                 | Needs code to unlock hidden key                                             |
| 8                 | SIM card is locked, waiting for CHV2 password                               |
| 9                 | SIM card is blocked, needs CHV2 unlock password                             |
| 10                | SIM card is locked due to failed network personalization check              |
| 11                | SIM card is blocked due to incorrect NCK, needs MEP unlock password         |
| 12                | SIM card is locked due to failed sub-network personalization check          |
| 13                | SIM card is blocked due to incorrect NSCK, needs MEP unlock password        |
| 14                | SIM card is locked due to failed service provider personalization check     |
| 15                | SIM card is blocked due to incorrect SPCK, needs MEP unlock password        |
| 16                | SIM card is locked due to failed corporate personalization check            |
| 17                | SIM card is blocked due to incorrect CCK, needs MEP unlock password         |
| 18                | SIM is initializing, waiting to complete                                    |
| 19                | Using CHV1/CHV2 universal PIN code to unlock CHV1 code, then unlock CHV2 code to unblock PIN |
| 20                | SIM card is invalid                                                         |
| 21                | Unknown status                                                              |

### wait_connect

> Wait for device network registration

**Example:**

```python
net_manage.wait_connect(timeout=60)
# (3, 1)
```

**Parameters:**

| Parameter | Type | Description                          |
|:----------|------|--------------------------------------|
| timeout   | int  | Wait for network registration timeout, unit: s |

**Return Value:**

| Data Type | Description                  |
|:----------|------------------------------|
| dict      | Returns a tuple in the format: `(stage, state)` |

| Parameter | Type | Description                                                                                                           |
|:----------|------|-----------------------------------------------------------------------------------------------------------------------|
| stage     | int  | Indicates the current status being checked:<br>1 - Checking SIM card status;<br>2 - Checking network registration status;<br>3 - Checking PDP Context activation status. |
| state     | int  | Based on the stage value, it indicates different statuses, as follows:<br>stage = 1, state indicates SIM card status, range 0~21, for detailed description of each status value, please refer to the return value description of the sim.getStatus() method;<br>stage = 2, state indicates network registration status, range 0~11, for detailed description of each status value, please refer to the return value description of the net.getState() method;<br>stage = 3, state indicates PDP Context activation status, 0 means activation failed, 1 means activation succeeded. |

### connect

> Device network connection

**Example:**

```python
net_manage.connect()
# True
```

**Parameters:**

None

**Return Value:**

| Data Type | Description            |
|:----------|------------------------|
| bool      | `True` - Success<br>`False` - Failure |

### disconnect

> Device network disconnection

**Example:**

```python
net_manage.disconnect(4)
# True
```

**Parameters:**

| Parameter | Type | Description                                      |
|:----------|------|--------------------------------------------------|
| val       | int  | 0 - Full network functionality off<br>4 - Airplane mode<br>Default: 4 |

**Return Value:**

| Data Type | Description            |
|:----------|------------------------|
| bool      | `True` - Success<br>`False` - Failure |

### reconnect

> Device re-network registration, this method is equivalent to calling `disconnect` first, then calling `connect`.

**Example:**

```python
net_manage.reconnect()
# True
```

**Parameters:**

None

**Return Value:**

| Data Type | Description            |
|:----------|------------------------|
| bool      | `True` - Success<br>`False` - Failure |

### sync_time

> Device synchronize network time

**Example:**

```python
net_manage.sync_time(timezon=8)
# True
```

**Parameters:**

| Parameter | Type | Description              |
|:----------|------|--------------------------|
| timezon   | int  | Time zone, -12~12, Default: 8 |

**Return Value:**

| Data Type | Description            |
|:----------|------------------------|
| bool      | `True` - Success<br>`False` - Failure |

### set_callback

> Set network status change callback function

**Example:**

```python
def net_callback(args):
    print(args)

net_manage.set_callback(callabck=net_callback)
# True
```

**Parameters:**

| Parameter | Type     | Description                                               |
|:----------|----------|-----------------------------------------------------------|
| callabck  | function | Callback function, <br>Function parameter `args`, data format `(pdp_id, state)` |

**Callback Function Parameters:**

| Parameter | Type | Description                                                            |
|:----------|------|------------------------------------------------------------------------|
| pdp_id    | int  | PDP context ID, indicating which PDP network status has changed        |
| state     | int  | Network status, 0 means network disconnected, 1 means network connected successfully |

**Return Value:**

| Data Type | Description            |
|:----------|------------------------|
| bool      | `True` - Success<br>`False` - Failure |

## Example Usage

```python
from net_manage import NetManage

# Module initialization
project_name = "QuecPython-Tracker"
project_version = "2.2.0"
net_manage = NetManage(project_name, project_version)

def net_callback(args):
    print(args)

# Set network status change callback function
net_manage.set_callback(net_callback)
# True

# Query SIM card status
net_manage.sim_status
# 1

# Query network status
net_manage.status
# False

# Device re-network registration
net_manage.disconnect()
# True
net_manage.connect()
# True
# net_manage.reconnect()
# True

# Wait for network registration success
net_manage.wait_connect(timeout=60)
# (3, 1)

# Synchronize network time
net_manage.sync_time()
```