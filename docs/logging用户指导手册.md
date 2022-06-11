# 日志模块 用户指导手册

## 简介

> 该模块用于代码日志打印

## 功能接口说明

### Logger 日志模块

#### 模块导入

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
res = log.set_debug(debug=True)
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
res = log.set_level()
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
