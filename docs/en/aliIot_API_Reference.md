# Ali IoT Platform Module API Reference Manual

[中文](../zh/aliIot_API参考手册.md) | English

## Introduction

This module is for the Ali IoT platform, using the MQTT protocol for communication, enabling data interaction between devices and the server.

Main supported features:

- Message publishing and subscription
- OTA upgrades

## API Description

### AliIot

> This module mainly provides connection to the Ali IoT platform, message sending, and message subscription.

**Example:**

```python
from aliIot import AliIot

server_cfg = {
    "product_key": "xxx",
    "product_secret": "xxx",
    "device_name": "xxx",
    "device_secret": "xxx",
    "server": "iot-as-mqtt.cn-shanghai.aliyuncs.com",
    "qos": 1,
}
server = AliIot(**server_cfg)
```

**Parameters:**

| Parameter       | Type | Description        |
|:----------------|------|--------------------|
| product_key     | str  | Product identifier |
| product_secret  | str  | Product secret     |
| device_name     | str  | Device name        |
| device_secret   | str  | Device secret      |
| server          | str  | Access domain      |
| qos             | int  | Message service quality (0 ~ 1) |

#### status

> Query the server connection status.

**Example:**

```python
conn_status = server.status
print(conn_status)
# True
```

**Return Value:**

| Data Type | Description               |
|:----------|---------------------------|
| bool      | `True` - Connected<br>`False` - Not connected |

#### auth_info

> Query authentication information.

**Example:**

```python
auth_info = server.auth_info
print(auth_info)
# {"product_key": "xxx", "product_secret": "xxx", "device_name": "xxx", "device_secret": "xxx"}
```

**Return Value:**

| Data Type | Description               |
|:----------|---------------------------|
| dict      | `product_key` - Product identifier<br>`product_secret` - Product secret<br>`device_name` - Device name<br>`device_secret` - Device secret<br> |

#### add_event

> Add an event identifier to subscribe to the event publish response topic.

**Example:**

```python
res = server.add_event("sos_alarm")
print(res)
# True
```

**Parameters:**

| Parameter | Type | Description    |
|:----------|------|----------------|
| event     | str  | Event identifier |

**Return Value:**

| Data Type | Description               |
|:----------|---------------------------|
| bool      | `True` - Success<br>`False` - Failure |

#### add_service

> Add a service identifier to subscribe to the service topic.

**Example:**

```python
res = server.add_service("report_location")
print(res)
# True
```

**Parameters:**

| Parameter | Type | Description    |
|:----------|------|----------------|
| service   | str  | Service identifier |

**Return Value:**

| Data Type | Description               |
|:----------|---------------------------|
| bool      | `True` - Success<br>`False` - Failure |

#### set_callback

> Set the callback function to receive data sent by the server.

**Example:**

```python
def server_callback(args):
    print("topic: %s, data: %s" % (args[0], args[1]))

server.set_callback(server_callback)
```

**Parameters:**

| Parameter | Type     | Description                                         |
|:----------|----------|-----------------------------------------------------|
| callback  | function | Function to receive data sent by the server<br>Function parameter `args`, data format `(topic, data)` |

**Callback Function Parameters:**

| Parameter | Type     | Description                  |
|:----------|----------|------------------------------|
| topic     | str      | Topic receiving the message  |
| data      | dict/str | Specific data sent by the server |

**Return Value:**

None

#### connect

> Connect and log in to the Ali IoT platform server.

**Example:**

```python
res = server.connect()
print(res)
# 0
```

**Parameters:**

None

#### disconnect

> Disconnect from the Ali IoT platform server.

**Example:**

```python
res = server.disconnect()
print(res)
# True
```

**Parameters:**

None

**Return Value:**

| Data Type | Description               |
|:----------|---------------------------|
| bool      | `True` - Success<br>`False` - Failure |

#### properties_report

> Report device model properties.

**Example:**

```python
data = {
    "phone_num": "123456789",
    "energy": 100,
    "GeoLocation": {
        "Longitude": 100.26,
        "Latitude": 26.86,
        "Altitude": 0.0,
        "CoordinateSystem": 1
    }
}
res = server.properties_report(data)
print(res)
# True
```

**Parameters:**

| Parameter | Type | Description      |
|:----------|------|------------------|
| data      | dict | Device model data |

**Return Value:**

| Data Type | Description               |
|:----------|---------------------------|
| bool      | `True` - Success<br>`False` - Failure |

#### event_report

> Report an event.

**Example:**

```python
event = "sos_alarm"
data = {
    "time": str(utime.mktime(utime.local_time()) * 1000),
}
res = server.event_report(event, data)
print(res)
# True
```

**Parameters:**

| Parameter | Type | Description      |
|:----------|------|------------------|
| event     | str  | Event identifier |
| data      | dict | Event-related information |

**Return Value:**

| Data Type | Description               |
|:----------|---------------------------|
| bool      | `True` - Success<br>`False` - Failure |

#### service_response

> Respond to service messages.

**Example:**

```python
service = "report_location"
code = 200
data = {
    "GeoLocation": {
        "Longitude": 100.26,
        "Latitude": 26.86,
        "Altitude": 0.0,
        "CoordinateSystem": 1
    }
}
msg_id = "102"
message = "success"
res = server.service_response(service, code, data, msg_id, message)
print(res)
# True
```

**Parameters:**

| Parameter | Type | Description                          |
|:----------|------|--------------------------------------|
| service   | str  | Service identifier                   |
| code      | int  | Success identifier, 200 - Success, others - Failure |
| data      | dict | Service-related information          |
| msg_id    | str  | Message ID                           |
| message   | str  | Remark information                   |

**Return Value:**

| Data Type | Description               |
|:----------|---------------------------|
| bool      | `True` - Success<br>`False` - Failure |

#### rrpc_response

> Respond to RRPC messages.

**Example:**

```python
msg_id = "103"
data = {
    "phone_num": "123456789",
}
res = server.rrpc_response(msg_id, data)
print(res)
# True
```

**Parameters:**

| Parameter | Type | Description               |
|:----------|------|---------------------------|
| msg_id    | str  | Message ID                |
| data      | dict | RRPC-related information  |

**Return Value:**

| Data Type | Description               |
|:----------|---------------------------|
| bool      | `True` - Success<br>`False` - Failure |

#### property_set_reply

> Respond to property setting messages.

**Example:**

```python
msg_id = "103"
code = 200
msg = "success"
res = server.property_set_reply(msg_id, code, msg)
print(res)
# True
```

**Parameters:**

| Parameter | Type | Description                          |
|:----------|------|--------------------------------------|
| msg_id    | str  | Message ID                           |
| code      | int  | Success identifier, 200 - Success, others - Failure |
| msg       | str  | Remark information                   |

**Return Value:**

| Data Type | Description               |
|:----------|---------------------------|
| bool      | `True` - Success<br>`False` - Failure |

#### ota_device_inform

> Report device module identifier and version.

**Example:**

```python
# Software module and version
module = "QuecPython-Tracker"
version = "2.2.0"
# Firmware module and version
# module = "EC600N-CNLC"
# version = "EC600NCNLCR03A11M16_OCPU_QPY_BETA0313"
res = server.ota_device_inform(version, module)
print(res)
# True
```

**Parameters:**

| Parameter | Type | Description       |
|:----------|------|-------------------|
| module    | str  | Module identifier |
| version   | str  | Version information |

**Return Value:**

| Data Type | Description               |
|:----------|---------------------------|
| bool      | `True` - Success<br>`False` - Failure |

#### ota_firmware_get

> Query the device module OTA upgrade plan.

**Example:**

```python
# Software module and version
module = "QuecPython-Tracker"
# Firmware module and version
# module = "EC600N-CNLC"
res = server.ota_firmware_get(module)
print(res)
# True
```

**Parameters:**

| Parameter | Type | Description       |
|:----------|------|-------------------|
| module    | str  | Module identifier |

**Return Value:**

| Data Type | Description               |
|:----------|---------------------------|
| bool      | `True` - Success<br>`False` - Failure |

#### ota_device_progress

> Report the OTA upgrade progress of the device module.

**Example:**

```python
step = 100
desc = "success."
# Software module and version
module = "QuecPython-Tracker"
# Firmware module and version
# module = "EC600N-CNLC"
res = server.ota_device_progress(step, desc, module)
print(res)
# True
```

**Parameters:**

| Parameter | Type | Description                  |
|:----------|------|------------------------------|
| step      | int  | -1 - Cancel upgrade<br>1 ~ 100 - Upgrade progress |
| desc      | str  | Remark information           |
| module    | str  | Module identifier            |

**Return Value:**

| Data Type | Description               |
|:----------|---------------------------|
| bool      | `True` - Success<br>`False` - Failure |

### AliIotOTA

> This module mainly provides connection to the Ali IoT platform, message sending, and message subscription.

**Example:**

```python
from aliIot import AliIotOTA

project_name = "QuecPython-Tracker"
firmware_name = "EC600N-CNLC"
server_ota = AliIotOTA(project_name, firmware_name)
```

**Parameters:**

| Parameter      | Type | Description               |
|:---------------|------|---------------------------|
| project_name   | str  | Software module identifier |
| firmware_name  | str  | Hardware module identifier |

#### set_server

> Set the `AliIot` instantiated object to report the upgrade progress.

**Example:**

```python
server_ota.set_server(server)
```

**Parameters:**

| Parameter | Type   | Description        |
|:----------|--------|--------------------|
| server    | object | `AliIot` object    |

**Return Value:**

None

#### set_ota_data

> Set the specific information of the OTA upgrade plan.

**Example:**

```python
server_ota.set_ota_data(data)
```

**Parameters:**

| Parameter | Type | Description                                                    |
|:----------|------|----------------------------------------------------------------|
| data      | dict | [Ali OTA upgrade package information](https://help.aliyun.com/document_detail/85700.html#section-nm2-m4c-r2b) |

**Return Value:**

None

#### get_ota_info

> Get the OTA upgrade module identifier and target version number.

**Example:**

```python
data = server_ota.get_ota_info()
```

**Parameters:**

None

**Return Value:**

| Data Type | Description                         |
|:----------|-------------------------------------|
| dict      | `ota_module` - Upgrade module identifier<br>`ota_version` - Upgrade target version number |

#### start

> Start the OTA upgrade.

**Example:**

```python
data = server_ota.start()
```

**Parameters:**

None

**Return Value:**

| Data Type | Description               |
|:----------|---------------------------|
| bool      | `True` - Success<br>`False` - Failure |

## Usage Example

```python
from misc import Power
from aliIot import AliIot, AliIotOTA


def server_callback(args):
    global server, server_ota
    topic, data = args
    if "/thing/service/" in topic:
        # Service information delivery response
        service = topic.split("/")[-1]
        code = 200
        data = {}
        msg_id = data["id"]
        message = "success"
        server.service_response(service, code, data, msg_id, message)
    elif "/rrpc/request/" in topic:
        # RRPC synchronous message delivery response
        msg_id = topic.split("/")[-1]
        data = {}
        server.rrpc_response(msg_id, data)
    elif "/thing/service/property/set" in topic:
        # Device model data delivery response
        msg_id = data["id"]
        code = 200
        msg = "success"
        server.property_set_reply(msg_id, code, msg)
    elif topic.startswith("/ota/device/inform/") or topic.endswith("/ota/firmware/get_reply"):
        # OTA upgrade plan delivery
        server_ota.set_ota_data(data)
        step = 1
        desc = "start ota."
        ota_module = server_ota.get_ota_info()["ota_module"]
        # OTA upgrade progress report
        server.ota_device_progress(step, desc, ota_module)
        if server_ota.start():
            server.ota_device_progress(100, "success", ota_module)
        else:
            server.ota_device_progress(100, "failed", ota_module)
        Power.powerRestart()


# Ali IoT platform module initialization
server_cfg = {
    "product_key": "xxx",
    "product_secret": "xxx",
    "device_name": "xxx",
    "device_secret": "xxx",
    "server": "iot-as-mqtt.cn-shanghai.aliyuncs.com",
    "qos": 1,
}
server = AliIot(**server_cfg)

# Ali IoT platform OTA module initialization
project_name = "QuecPython-Tracker"
firmware_name = "EC600N-CNLC"
server_ota = AliIotOTA(project_name, firmware_name)

# Register callback function for Ali IoT platform module
server.set_callback(server_callback)

# Add events
server.add_event("sos_alarm")
server.add_event("low_power_alarm")

# Add services
server.add_service("query_phone_num")
server.add_service("query_power_level")

# Connect to the service
server.connect()

# Report device model properties
data = {
    "phone_num": "123456789",
    "energy": 100,
    "GeoLocation": {
        "Longitude": 100.26,
        "Latitude": 26.86,
        "Altitude": 0.0,
        "CoordinateSystem": 1
    }
}
server.properties_report(data)

# Report an event
event = "low_power_alarm"
data = {"power_level": 20}
server.event_report(event, data)

# Report software module version information
PROJECT_NAME = "QuecPython-Tracker-Laike"
PROJECT_VERSION = "1.1.0"
server.ota_device_inform(PROJECT_VERSION, PROJECT_NAME)

# Query software module OTA upgrade plan
server.ota_firmware_get(PROJECT_NAME)

# Disconnect from the server
server.disconnect()
```