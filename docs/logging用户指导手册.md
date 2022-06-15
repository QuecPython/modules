# 日志模块 用户指导手册

## 简介

> 该模块用于代码日志打印

## 使用说明

### 1. 模块初始化

```python
from logging import getLogger

log = getLogger("test_log")
```

### 2. 设置debug日志开关, 默认开

```python
debug = True
res = log.set_debug(debug)
```

### 3. 设置日志等级, 默认`debug`

```python
level = "debug"
res = log.set_level(level)
```

### 4. 打印不同等级日志

```python
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

## API说明

### getLogger 返回日志实例对象

示例:

```python
from logging import getLogger

log = getLogger("test_log")
```

参数:

|参数|类型|说明|
|:---|---|---|
|name|STRING|日志模块名|

返回值:

|数据类型|说明|
|:---|---|
|OBJECT|`Logger`实例对象|

### Logger 日志模块

#### 导入初始化

示例:

```python
from logging import Logger

log = Logger("test_log")
```

参数:

|参数|类型|说明|
|:---|---|---|
|name|STRING|日志模块名|

#### get_debug 获取debug日志开关

示例:

```python
level = log.get_debug()
```

参数:

无

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`开启, `False`关闭|

#### set_debug 设置debug日志开关

示例:

```python
res = log.set_debug(True)
```

参数:

|参数|类型|说明|
|:---|---|---|
|debug|BOOL|`True`开启, `False`关闭, 默认`True`|

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|

#### get_level 获取日志等级

示例:

```python
level = log.get_level()
```

参数:

无

返回值:

|数据类型|说明|
|:---|---|
|STRING|日志等级, `debug`, `info`, `warn`, `error`, `critical`|

#### set_level 设置日志等级

示例:

```python
res = log.set_level("debug")
```

参数:

|参数|类型|说明|
|:---|---|---|
|level|STRING|日志等级, `debug`, `info`, `warn`, `error`, `critical`|

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|

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
