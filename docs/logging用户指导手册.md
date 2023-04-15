# 日志模块 用户指导手册

## 简介

> 该模块用于代码日志打印

## API说明

### getLogger

> 获取知道名称的日志实例对象

示例:

```python
from logging import getLogger

log = getLogger("test_log")
```

参数:

|参数|类型|说明|
|:---|---|---|
|name|str|日志模块名|

返回值:

|数据类型|说明|
|:---|---|
|object|`Logger`实例对象|

### setLogSave

> 设置日志存储相关参数, 此处设置的是整个项目中所有日志都进行存储。

示例:

```python
save = True
path = "/usr/log/"
name = "test.log"
size = 4096
backups = 5
setLogSave(save, path, name, size, backups)
# True
```

参数:

|参数|类型|说明|
|:---|---|---|
|name|str|日志模块名|

返回值:

|数据类型|说明|
|:---|---|
|bool|`True`成功<br>`False`失败|

### setLogLevel

> 设置日志等级。

示例:

```python
level = "debug"
setLogLevel(level)
# True
```

参数:

|参数|类型|说明|
|:---|---|---|
|level|str|日志等级, `debug`, `info`, `warn`, `error`, `critical`|

返回值:

|数据类型|说明|
|:---|---|
|bool|`True`成功<br>`False`失败|

### setLogDebug

> 设置日志等级。

示例:

```python
debug = True
setLogDebug(debug)
# True
```

参数:

|参数|类型|说明|
|:---|---|---|
|debug|bool|debug等级日志开关|

返回值:

|数据类型|说明|
|:---|---|
|bool|`True`成功<br>`False`失败|

### Logger 日志模块

#### 导入初始化

> 不建议直接使用该类进行实例化对象, 建议直接通过`getLogger`接口获取Logger对象。

示例:

```python
from logging import Logger

log = Logger("test_log")
```

参数:

|参数|类型|说明|
|:---|---|---|
|name|STRING|日志模块名|

#### debug 打印debug级别日志

示例:

```python
log.debug("debug log")
# [2022-05-09 09:03:21] [test_log] [debug] debug log
```

参数:

|参数|类型|说明|
|:---|---|---|
|message|STRING|日志信息|

返回值:

无

#### info 打印info级别日志

示例:

```python
log.info("info log")
# [2022-05-09 09:03:21] [test_log] [info] info log
```

参数:

|参数|类型|说明|
|:---|---|---|
|message|STRING|日志信息|

返回值:

无

#### warn 打印warn级别日志

示例:

```python
log.warn("warn log")
# [2022-05-09 09:03:21] [test_log] [warn] warn log
```

参数:

|参数|类型|说明|
|:---|---|---|
|message|STRING|日志信息|

返回值:

无

#### error 打印error级别日志

示例:

```python
log.error("error log")
# [2022-05-09 09:03:21] [test_log] [error] error log
```

参数:

|参数|类型|说明|
|:---|---|---|
|message|STRING|日志信息|

返回值:

无

#### critical 打印critical级别日志

示例:

```python
log.critical("critical log")
# [2022-05-09 09:03:21] [test_log] [critical] critical log
```

参数:

|参数|类型|说明|
|:---|---|---|
|message|STRING|日志信息|

返回值:

无

## 使用示例

```python
from logging import getLogger, setLogLevel, setLogDebug, setLogSave

# 模块初始化
log = getLogger("test_log")

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
setLogSave(save, path, name, size, backups)
# True

# 打印不同等级日志
log.debug("debug log")
# [2022-05-09 09:03:21] [test_log] [debug] debug log

log.info("info log")
# [2022-05-09 09:03:21] [test_log] [info] info log

log.warn("warn log")
# [2022-05-09 09:03:21] [test_log] [warn] warn log

log.error("error log")
# [2022-05-09 09:03:21] [test_log] [error] error log

log.critical("critical log")
# [2022-05-09 09:03:21] [test_log] [critical] critical log
```
