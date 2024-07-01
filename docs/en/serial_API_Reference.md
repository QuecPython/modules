# Serial Communication Module API Reference Manual

[中文](../zh/serial_API参考手册.md) | English

## Introduction

> This module is used for serial communication (blocking and non-blocking mode read).

## API Description

### Serial

> Initialization.

**Example:**

```python
from serial import Serial

# The following example parameters are consistent with the default parameters
serial = Serial(
    port=2,  # Quectel module UART number
    baudrate=115200,  # Baud rate
    bytesize=8,  # Data bits [5 ~ 8]
    parity=0,  # Parity (0 – NONE, 1 – EVEN, 2 – ODD)
    stopbits=1,   # Stop bits [1 ~ 2]
    flowctl=0  # Hardware flow control (0 – FC_NONE, 1 – FC_HW)
)
```

**Parameters:**

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| port      | int  | Serial port number |
| baudrate  | int  | Baud rate |
| bytesize  | int  | Data bits |
| stopbits  | int  | Stop bits |
| flowctl   | int  | Flow control |

### Serial.write

> Serial write.

**Example:**

```python
# Behavior is consistent with `machine.UART.write`.
serial.write(b'hello world!')
```

**Parameters:**

| Parameter | Type  | Description    |
| --------- | ----- | -------------- |
| data      | bytes | Data to be sent |

### Serial.read

> Serial read.

**Example:**

```python
# Non-blocking mode read, behavior is consistent with `machine.UART.read`
r_data = serial.read(1024)  # timeout keyword parameter defaults to 0

# Blocking read. Reads until 1024 bytes are read. (If the specified bytes are not read, it will block indefinitely.)
r_data = serial.read(1024, timeout=-1)

# Blocking read. Returns immediately after reading the specified bytes. (If the specified bytes are not read within the timeout (ms), it returns the actual read bytes.)
r_data = serial.read(1024, timeout=1000)
```

**Parameters:**

| Parameter | Type | Description       |
| --------- | ---- | ----------------- |
| size      | int  | Number of bytes to read |
| timeout   | int  | Timeout in ms     |