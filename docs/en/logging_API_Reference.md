# Logging Module API Reference Manual

[中文](../zh/logging_API参考手册.md) | English

## Introduction

> This module is used for code log printing.

## API Description

### Log Level Enumerations

| Enumeration |
|:---|
| `logging.CRITICAL` |
| `logging.FATAL` |
| `logging.ERROR` |
| `logging.WARNING` |
| `logging.WARN` |
| `logging.INFO` |
| `logging.DEBUG` |
| `logging.NOTSE` |

### Logger

> It is not recommended to directly instantiate objects using this class. It is recommended to obtain `Logger` objects directly through the [`getLogger`](#getlogger) interface.

**Example:**

```python
from logging import Logger

logger = Logger("test_log")
```

**Parameters:**

| Parameter | Type | Description |
|:---|---|---|
| name | str | Log module name |

#### debug

> Print DEBUG level logs.

**Example:**

```python
logger.debug("debug log")
# [2022-05-09 09:03:21][test_log][DEBUG] debug log
```

**Parameters:**

| Parameter | Type | Description |
|:---|---|---|
| message | str | Log information |

#### info

> Print INFO level logs.

**Example:**

```python
logger.info("info log")
# [2022-05-09 09:03:21][test_log][INFO] info log
```

**Parameters:**

| Parameter | Type | Description |
|:---|---|---|
| message | str | Log information |

#### warn

> Print WARNING level logs. Equivalent to the `warning` method.

**Example:**

```python
logger.warn("warn log")
# [2022-05-09 09:03:21][test_log][WARNING] warn log
```

**Parameters:**

| Parameter | Type | Description |
|:---|---|---|
| message | str | Log information |

#### warning

> Print WARNING level logs.

**Example:**

```python
logger.warn("warning log")
# [2022-05-09 09:03:21][test_log][WARNING] warning log
```

**Parameters:**

| Parameter | Type | Description |
|:---|---|---|
| message | str | Log information |

#### error

> Print ERROR level logs.

**Example:**

```python
logger.error("error log")
# [2022-05-09 09:03:21][test_log][ERROR] error log
```

**Parameters:**

| Parameter | Type | Description |
|:---|---|---|
| message | str | Log information |

#### fatal

> Print FATAL level logs. Equivalent to the `critical` method.

**Example:**

```python
logger.fatal("fatal log")
# [2022-05-09 09:03:21][test_log][CRITICAL] fatal log
```

**Parameters:**

| Parameter | Type | Description |
|:---|---|---|
| message | str | Log information |

#### critical

> Print critical level logs.

**Example:**

```python
logger.critical("critical log")
# [2022-05-09 09:03:21][test_log][CRITICAL] critical log
```

**Parameters:**

| Parameter | Type | Description |
|:---|---|---|
| message | str | Log information |

### getLogger

> Get the log instance object with the specified name. This method can prevent the repeated creation of `Logger` objects with the same name.

**Example:**

```python
from logging import getLogger

log = getLogger("test_log")
```

**Parameters:**

| Parameter | Type | Description |
|:---|---|---|
| name | str | Log module name |

**Return Value:**

| Data Type | Description |
|:---|---|
| object | `Logger` object |

### setSaveLog

> Set log storage related parameters. The storage information set here is the project-level log attribute.

**Example:**

```python
save = True
path = "/usr/log/"
name = "test.log"
size = 4096
backups = 5
setSaveLog(save, path, name, size, backups)
# True
```

**Parameters:**

| Parameter | Type | Description |
|:---|---|---|
| name | str | Log module name |

**Return Value:**

| Data Type | Description |
|:---|---|
| bool | `True` - Success<br>`False` - Failure |

### getSaveLog

> Get whether the current log file storage is enabled.

**Example:**

```python
getSaveLog()
# True
```

**Parameters:**

None

**Return Value:**

| Data Type | Description |
|:---|---|
| bool | `True` - Enabled<br>`False` - Disabled |

### setLogLevel

> Set the project-level log level.

**Example:**

```python
level = "debug"
setLogLevel(level)

level = "WARN"
setLogLevel(level)

setLogLevel(logging.ERROR)
```

**Parameters:**

| Parameter | Type | Description |
|:---|---|---|
| level | str/int | Log level, can use string (case insensitive) or [log level enumerations](#log-level-enumerations) |

**Return Value:**

| Data Type | Description |
|:---|---|
| bool | `True` - Success<br>`False` - Failure |

### getLogLevel

> Get the current log level, returning the corresponding uppercase string of the log level.

**Example:**

```python
getLogLevel()
# True
```

**Parameters:**

None

**Return Value:**

| Data Type | Description |
|:---|---|
| str | Uppercase string of the log level<br>`CRITICAL`, `ERROR`, `WARNING`, `INFO`, `DEBUG`, `NOTSET` |

### setLogDebug

> Set the project-level DEBUG log switch. When DEBUG is enabled, logs of the configured log level, including DEBUG level logs, will be output. If DEBUG is disabled, DEBUG level logs will not be output even if the log level is set to DEBUG.

**Example:**

```python
debug = True
setLogDebug(debug)
# True
```

**Parameters:**

| Parameter | Type | Description |
|:---|---|---|
| debug | bool | DEBUG log switch |

**Return Value:**

| Data Type | Description |
|:---|---|
| bool | `True` - Success<br>`False` - Failure |

### getLogDebug

> Get the DEBUG setting status.

**Example:**

```python
getLogDebug()
# True
```

**Parameters:**

None

**Return Value:**

| Data Type | Description |
|:---|---|
| bool | `True` - Enabled<br>`False` - Disabled |

## Usage Example

```python
from logging import getLogger, setLogLevel, setLogDebug, setSaveLog

# Set the DEBUG log switch, default is on
debug = True
setLogDebug(debug)
# True

# Set the log level, default is `debug`
level = "debug"
setLogLevel(level)
# True

# Set log storage
save = True
path = "/usr/log/"
name = "test.log"
size = 4096
backups = 5
setSaveLog(save, path, name, size, backups)
# True

# Module initialization
logger = getLogger("test_log")

# Print logs of different levels
logger.debug("debug log")
# [2022-05-09 09:03:21][test_log][DEBUG] debug log

logger.info("info log")
# [2022-05-09 09:03:21][test_log][INFO] info log

logger.warn("warn log")
# [2022-05-09 09:03:21][test_log][WARNING] warn log

logger.warning("warning log")
# [2022-05-09 09:03:21][test_log][WARNING] warning log

logger.error("error log")
# [2022-05-09 09:03:21][test_log][ERROR] error log

logger.fatal("fatal log")
# [2022-05-09 09:03:21][test_log][CRITICAL] fatal log

logger.critical("critical log")
# [2022-05-09 09:03:21][test_log][CRITICAL] critical log
```