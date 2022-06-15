# 低功耗唤醒模块 用户指导手册

## 简介

> 提供定时低功耗唤醒功能, 当设备不进行业务处理时, 可将设备调整为低功耗模式, 当设备唤醒时, 可通知用户进行业务处理。
> 该模块被设计为被监听者, 使用时需给其注册一个监听者, 当设备唤醒时, 通知监听者进行业务处理。
> 
> 支持定时器:
>
>   - RTC
>   - osTimer
>
> 支持低功耗模式:
> 
>   - PM(wake_lock)
>   - PSM
>   - PWOERDOWN
> 
> 功耗大小排序
> 
> PM > PSM > PWOERDOWN
> 
> **注意**
> 
> - 当设备只支持osTimer定时器, 不支持RTC定时器时, 设备只支持PM(wake_lock)低功耗模式
> - 当设备支持RTC模式时, 需确认设备是否支持PSM或POWERDOWN通过RTC唤醒, 支持才可使用该种低功耗模式, 设备支持休眠模式表见`common`模块中的`LOWENERGYMAP`

## 使用说明

### 1. 模块初始化

```python
from mpower import LowEnergyManage

low_energy = LowEnergyManage()
```

### 2. 设置低功耗唤醒周期

```python
period = 20
res = low_energy.set_period(period)
```

### 3. 设置低功耗模式

```python
method = "PM"
res = low_energy.set_low_energy_method(method)
```

### 4. 低功耗模式初始化

```python
res = low_energy.low_energy_init()
```

### 5. 开启低功耗唤醒

```python
res = low_energy.start()
```

### 5. 停止低功耗唤醒

```python
res = low_energy.stop()
```

## API说明

> 该模块继承`common`模块中的`Observable`方法, 其方法见`common`模块文档, 在此不再赘述。

### LowEnergyManage

#### 导入初始化

示例:

```python
from mpower import LowEnergyManage

low_energy = LowEnergyManage()
```

参数:

无

返回值:

无

#### get_period 获取低功耗唤醒周期

示例:

```python
period = low_energy.get_period()
```

参数:

无

返回值:

|数据类型|说明|
|:---|---|
|INT|唤醒周期, 单位s|

#### set_period 设置低功耗唤醒周期

示例:

```python
period = 20
res = low_energy.set_period(period)
```

参数:

|参数|类型|说明|
|:---|---|---|
|period|INT|休眠唤醒周期, 非0正整数, 单位s|

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|

#### get_low_energy_method 获取低功耗模式

示例:

```python
method = low_energy.get_low_energy_method()
```

参数:

无

返回值:

|数据类型|说明|
|:---|---|
|STRING|低功耗模式, `NULL`(不休眠), `PM`(wake_lock), `PSM`, `PWOERDOWN`|

#### set_low_energy_method 设置低功耗模式

示例:

```python
method = "PM"
res = low_energy.set_low_energy_method(method)
```

参数:

|参数|类型|说明|
|:---|---|---|
|method|STRING|低功耗模式, `NULL`(不休眠), `PM`(wake_lock), `PSM`, `PWOERDOWN`|

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|

#### get_lpm_fd 获取wake_lock锁

示例:

```python
lpm_fd = low_energy.get_lpm_fd()
```

参数:

无

返回值:

|数据类型|说明|
|:---|---|
|int|`PM`(wake_lock)对应标识id|

#### low_energy_init 低功耗模式初始化

> 初始化低功耗模式之前需设置好唤醒周期和低功耗模式, 如未设置, 则默认周期60s, 默认低功耗模式`PM`。

示例:

```python
res = low_energy.low_energy_init()
```

参数:

无

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|

#### start 开启低功耗唤醒

示例:

```python
res = low_energy.start()
```

参数:

无

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|

#### stop 停止低功耗唤醒

> 该方法只适用于PM(wake_lock)休眠方式

示例:

```python
res = low_energy.stop()
```

参数:

无

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|
