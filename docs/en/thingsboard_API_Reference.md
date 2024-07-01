# ThingsBoard Platform Client Module API Reference Manual

[中文](../zh/thingsboard_API参考手册.md) | English

## Introduction

- This module is a client function module for the ThingsBoard platform, using the MQTT protocol for communication, enabling data interaction between devices and the server.
- Main supported functions: message publishing and subscription.

## API Description

### TBDeviceMQTTClient

> This module mainly provides the connection, message sending, and message subscription for the ThingsBoard platform client module.

#### Instantiate Object

**Example:**

```python
from thingsboard import TBDeviceMQTTClient

server_cfg = {
    "host": "xxx",
    "port": 0,
    "username": "xxx",
    "qos": 1,
    "client_id": "xxx",
}
server = TBDeviceMQTTClient(**server_cfg)
```

**Parameters:**

| Parameter | Type | Description |
|:---|---|---|
| host | str | Server IP |
| port | int | Server port |
| username | str | Username |
| qos | int | Message Quality of Service (0 ~ 1) |
| client_id | str | Client ID, can use device IMEI |

#### status

> Query the server connection status.

**Example:**

```python
conn_status = server.status
print(conn_status)
# True
```

**Return Value:**

| Data Type | Description |
|:---|---|
| bool | `True` - Connected<br>`False` - Not connected |

#### set_callback

> Set to receive data information sent by the server.

**Example:**

```python
def server_callback(topic, data):
    print("topic: %s, data: %s" % (topic, data))

server.set_callback(server_callback)
```

**Parameters:**

| Parameter | Type | Description |
|:---|---|---|
| callback | function | Used to receive data information sent by the server<br>Function parameters `(topic, data)` |

**Callback Function Parameters:**

| Parameter | Type | Description |
|:---|---|---|
| topic | str | Topic of the received message |
| data | str | Specific data sent by the server |

**Return Value:**

| Data Type | Description |
|:---|---|
| bool | `True` - Success<br>`False` - Failure |

#### connect

> Connect and log in to the server.

**Example:**

```python
res = server.connect()
print(res)
# True
```

**Parameters:**

None

**Return Value:**

| Data Type | Description |
|:---|---|
| bool | `True` - Success<br>`False` - Failure |

#### disconnect

> Disconnect from the server.

**Example:**

```python
res = server.disconnect()
print(res)
# True
```

**Parameters:**

None

**Return Value:**

| Data Type | Description |
|:---|---|
| bool | `True` - Success<br>`False` - Failure |

#### send_telemetry

> Report telemetry data.

**Example:**

```python
data = {
    "Longitude": 100.26,
    "Latitude": 26.86,
    "Altitude": 0.0,
    "Speed": 10.0
}
res = server.send_telemetry(data)
print(res)
# True
```

**Parameters:**

| Parameter | Type | Description |
|:---|---|---|
| data | dict | Telemetry data |

**Return Value:**

| Data Type | Description |
|:---|---|
| bool | `True` - Success<br>`False` - Failure |

#### send_rpc_reply

> RPC message reply.

**Example:**

```python
data = {
    "Longitude": 100.26,
    "Latitude": 26.86,
    "Altitude": 0.0,
    "Speed": 10.0
}
request_id = "102"
res = server.send_rpc_reply(data, request_id)
print(res)
# True
```

**Parameters:**

| Parameter | Type | Description |
|:---|---|---|
| data | dict | Service related information |
| request_id | str | Message ID |

**Return Value:**

| Data Type | Description |
|:---|---|
| bool | `True` - Success<br>`False` - Failure |

## Usage Example

```python
from usr.thingsboard import TBDeviceMQTTClient

def server_callback(topic, data):
    print("topic: %s, data: %s" % (topic, data))
    # RPC message reply
    if "rpc" in topic:
        request_id = data["id"]
        data = {}
        server.send_rpc_reply(data, request_id)


# Initialize function module
server_cfg = {
    "host": "xxx",
    "port": 0,
    "username": "xxx",
    "qos": 1,
    "client_id": "xxx",
}
server = TBDeviceMQTTClient(**server_cfg)

# Set callback function
server.set_callback(server_callback)

# Connect and log in to the server
res = server.connect()
print(res)
# True

# Report telemetry data
data = {
    "Longitude": 100.26,
    "Latitude": 26.86,
    "Altitude": 0.0,
    "Speed": 10.0
}
res = server.send_telemetry(data)
print(res)
# True

# Disconnect from the server
res = server.disconnect()
print(res)
# True
```