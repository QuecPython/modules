# 日志模块 API 参考手册

中文 | [English](../en/logging_API_Reference.md)

## 简介

> 该模块用于代码日志打印。

## API 说明

### 日志等级枚举值

|枚举值|
|:---|
|`logging.CRITICAL`|
|`logging.FATAL`|
|`logging.ERROR`|
|`logging.WARNING`|
|`logging.WARN`|
|`logging.INFO`|
|`logging.DEBUG`|
|`logging.NOTSE`|

### Logger

> 不建议直接使用该类进行实例化对象, 建议直接通过 [`getLogger`](#getlogger) 接口获取 `Logger` 对象。

**示例：**

```python
from logging import Logger

logger = Logger("test_log")
```

**参数：**

|参数|类型|说明|
|:---|---|---|
|name|str|日志模块名|

#### debug

> 打印 DEBUG 级别日志。

**示例：**

```python
logger.debug("debug log")
# [2022-05-09 09:03:21][test_log][DEBUG] debug log
```

**参数：**

|参数|类型|说明|
|:---|---|---|
|message|str|日志信息|

#### info

> 打印 INFO 级别日志。

**示例：**

```python
logger.info("info log")
# [2022-05-09 09:03:21][test_log][INFO] info log
```

**参数：**

|参数|类型|说明|
|:---|---|---|
|message|str|日志信息|

#### warn

> 打印 WARNNING 级别日志。等价于 `warning` 方法。

**示例：**

```python
logger.warn("warn log")
# [2022-05-09 09:03:21][test_log][WARNING] warn log
```

**参数：**

|参数|类型|说明|
|:---|---|---|
|message|str|日志信息|

#### warning

> 打印 WARNNING 级别日志。

**示例：**

```python
logger.warn("warning log")
# [2022-05-09 09:03:21][test_log][WARNING] warning log
```

**参数：**

|参数|类型|说明|
|:---|---|---|
|message|str|日志信息|

#### error

> 打印 ERROR 级别日志。

**示例：**

```python
logger.error("error log")
# [2022-05-09 09:03:21][test_log][ERROR] error log
```

**参数：**

|参数|类型|说明|
|:---|---|---|
|message|str|日志信息|

#### fatal

> 打印 FATAL 级别日志。等价于 `critical` 方法。

**示例：**

```python
logger.fatal("fatal log")
# [2022-05-09 09:03:21][test_log][CRITICAL] fatal log
```

**参数：**

|参数|类型|说明|
|:---|---|---|
|message|str|日志信息|

#### critical

> 打印 critical 级别日志。

**示例：**

```python
logger.critical("critical log")
# [2022-05-09 09:03:21][test_log][CRITICAL] critical log
```

**参数：**

|参数|类型|说明|
|:---|---|---|
|message|str|日志信息|

### getLogger

> 获取指定名称的日志实例对象。该方法可以防止重复创建相同名称的 `Logger` 对象。

**示例：**

```python
from logging import getLogger

log = getLogger("test_log")
```

**参数：**

|参数|类型|说明|
|:---|---|---|
|name|str|日志模块名|

**返回值：**

|数据类型|说明|
|:---|---|
|object|`Logger` 对象|

### setSaveLog

> 设置日志存储相关参数，此处设置的存储信息是项目级别的日志属性。

**示例：**

```python
save = True
path = "/usr/log/"
name = "test.log"
size = 4096
backups = 5
setSaveLog(save, path, name, size, backups)
# True
```

**参数：**

|参数|类型|说明|
|:---|---|---|
|name|str|日志模块名|

**返回值：**

|数据类型|说明|
|:---|---|
|bool|`True` - 成功<br>`False` - 失败|

### getSaveLog

> 获取当前是否开启存储日志文件。

**示例：**

```python
getSaveLog()
# True
```

**参数：**

无

**返回值：**

|数据类型|说明|
|:---|---|
|bool|`True` - 开启<br>`False` - 关闭|

### setLogLevel

> 设置项目级日志等级。

**示例：**

```python
level = "debug"
setLogLevel(level)

level = "WARN"
setLogLevel(level)

setLogLevel(logging.ERROR)
```

**参数：**

|参数|类型|说明|
|:---|---|---|
|level|str/int|日志等级，可以使用字符串(不区分大小写)或[日志等级枚举值](#日志等级枚举值)|

**返回值：**

|数据类型|说明|
|:---|---|
|bool|`True` - 成功<br>`False` - 失败|

### getLogLevel

> 获取当前日志等级，返回对应日志等级的大写字符串。

**示例：**

```python
getLogLevel()
# True
```

**参数：**

无

**返回值：**

|数据类型|说明|
|:---|---|
|str|日志等级的大写字符串<br>`CRITICAL`，`ERROR`，`WARNING`，`INFO`，`DEBUG`，`NOTSET`|

### setLogDebug

> 设置项目级日志 DEBUG 日志开关。当设置了 DEBUG 开启，则会输出配置的日志等级的日志，包括 DEBUG 等级日志，如果设置了 DEBUG 关闭，则不会输出 DEBUG 等级日志，哪怕设置的日志等级时 DEBUG。

**示例：**

```python
debug = True
setLogDebug(debug)
# True
```

**参数：**

|参数|类型|说明|
|:---|---|---|
|debug|bool|DEBUG 日志开关|

**返回值：**

|数据类型|说明|
|:---|---|
|bool|`True`成功<br>`False`失败|

### getLogDebug

> 获取 DEBUG 设置状态。

**示例：**

```python
getLogDebug()
# True
```

**参数：**

无

**返回值：**

|数据类型|说明|
|:---|---|
|bool|`True` - 开启<br>`False` - 关闭|

## 使用示例

```python
from logging import getLogger, setLogLevel, setLogDebug, setSaveLog

# 设置debug日志开关, 默认开
debug = True
setLogDebug(debug)
# True

# 设置日志等级, 默认`debug`
level = "debug"
setLogLevel(level)
# True

# 设置日志存储
save = True
path = "/usr/log/"
name = "test.log"
size = 4096
backups = 5
setSaveLog(save, path, name, size, backups)
# True

# 模块初始化
logger = getLogger("test_log")

# 打印不同等级日志
logger.debug("debug log")
# [2022-05-09 09:03:21][test_log][DEBUG] debug log

logger.info("info log")
# [2022-05-09 09:03:21][test_log][INFO] info log

logger.warn("warn log")
# [2022-05-09 09:03:21][test_log][WARNING] warn log

logger.warning("warning log")
# [2022-05-09 09:03:21][test_log][WARNING] warn log

logger.error("error log")
# [2022-05-09 09:03:21][test_log][ERROR] error log

logger.fatal("fatal log")
# [2022-05-09 09:03:21][test_log][CRITICAL] fatal log

logger.critical("critical log")
# [2022-05-09 09:03:21][test_log][CRITICAL] critical log
```
