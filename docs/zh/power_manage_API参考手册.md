# 低功耗管理模块 API 参考手册

中文 | [English](../en/power_manage_API_Reference.md)

## 简介

该模块主要用于控制设备的低功耗模式，QuecPython 根据不同设备支持的低功耗模式不同，主要有一下两种低功耗模式。

- sleep 模式
- psm 模式

## API 说明

### PMLock

> 该方法实现了休眠锁的获取与释放功能，方便使用 Python `with` 方法进行使用。

**示例：**

```python
from power_manage import PMLock

def test():
    pm_lock = PMLock("pmlk")
    with pm_lock:
        # TODO: Do business process, when device idel, device is not into sleep.
        pass
```

**参数：**

|参数|类型|说明|
|:---|---|---|
|lock_name|str|休眠锁名称, 不可重复, 字符长度最大8位|

### PowerManage

#### 初始化模块

**示例：**

```python
from power_manage import PowerManage

power_manage = PowerManage()
```

### PowerManage.autosleep

> 设置设备 sleep 休眠模式使能。

**示例：**

```python
net_manage.autosleep(1)
# True
```

**参数：**

|参数|类型|说明|
|:---|---|---|
|val|int|0 - 关闭 sleep 模式<br>1 - 开启 sleep 模式|

**返回值：**

|数据类型|说明|
|:---|---|
|bool|`True` - 成功<br>`False` - 失败|

### PowerManage.set_psm

> 设置设备 psm 休眠模式

**示例：**

```python
net_manage.set_psm(mode=1, tau=3600, act=5)
# True
```

**参数：**

|参数|类型|说明|
|:---|---|---|
|mode|int|0 - 关闭 psm<br>1 - 启动 psm<br>当该参数为 0 时，`tau` 与 `act` 可不传参|
|tau|int|休眠持续时间，（T3412）定时器时间周期值，单位：秒|
|act|int|进入休眠时间，（T3324）定时器时间周期值，单位：秒|

**返回值：**

|数据类型|说明|
|:---|---|
|bool|`True` - 成功<br>`False` - 失败|

### PowerManage.set_hibernatea

> 设置设备强制 psm 休眠, 该方法目前只适用于 EC800E R02 版本固件。

**示例：**

```python
net_manage.set_hibernatea()
# True
```

**参数：**

无

**返回值：**

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
