# 低功耗管理模块 用户指导手册

## 简介

> 该模块主要用于控制设备的低功耗模式, QuecPython根据不同设备支持的低功耗模式不同, 主要有一下两种低功耗模式
> 
> - sleep 模式
> - psm 模式

## API说明

### PMLock

> 该方法实现了休眠锁的获取与释放功能, 方便使用python `with`方法进行使用

**示例:**

```python
from power_manage import PMLock

def test():
    pm_lock = PMLock("pmlk")
    with pm_lock:
        # TODO: Do business process, when device idel, device is not into sleep.
        pass
```

**参数:**

|参数|类型|说明|
|:---|---|---|
|lock_name|str|休眠锁名称, 不可重复, 字符长度最大8位|

### PowerManage

#### 实例化对象

**示例:**

```python
from power_manage import PowerManage

power_manage = PowerManage()
```

### autosleep

> 设置设备sleep休眠模式开关

**示例:**

```python
net_manage.autosleep(1)
# True
```

**参数:**

|参数|类型|说明|
|:---|---|---|
|val|int|0 - 关闭sleep模式<br>1 - 启动sleep模式|

**返回值:**

|数据类型|说明|
|:---|---|
|bool|`True` - 成功<br>`False` - 失败|

### set_psm

> 设置设备psm休眠模式

**示例:**

```python
net_manage.set_psm(mode=1, tau=3600, act=5)
# True
```

**参数:**

|参数|类型|说明|
|:---|---|---|
|mode|int|0 - 关闭psm<br>1 - 启动psm, 当该参数为0时, `tau`与`act`可不传参.|
|tau|int|休眠持续时间, (T3412)定时器时间周期值, 单位: s|
|act|int|进入休眠时间, (T3324)定时器时间周期值, 单位: s|

**返回值:**

|数据类型|说明|
|:---|---|
|bool|`True` - 成功<br>`False` - 失败|

### set_hibernatea

> 设置设备强制psm休眠, 该方法目前只适用于EC800E R02版本固件

**示例:**

```python
net_manage.set_hibernatea()
# True
```

**参数:**

无

**返回值:**

|数据类型|说明|
|:---|---|
|bool|`True` - 成功<br>`False` - 失败|

## 使用示例

```python
from power_manage import PowerManage

# 功能模块初始化
power_manage = PowerManage()

# 设置sleep休眠
power_manage.autosleep(1)
# True

# 禁用sleep休眠
power_manage.autosleep(0)
# True

# 设置PSM休眠
net_manage.set_psm(mode=1, tau=3600, act=5)
# True

# 禁用PSM休眠
net_manage.set_psm(mode=0)
# True

# 设置强制PSM休眠
net_manage.set_hibernatea()
# True
```
