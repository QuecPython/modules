# 网络管理模块 API 参考手册

## 简介

> 该模块主要用于控制设备的网络断开与连接, 查询设备注网结果, 查询设备网络状态, 同步服务器时间, 通过回调函数接收设备网络状态变化情况。

## API说明

### 实例化对象

**示例:**

```python
from net_manage import NetManage

project_name = "QuecPython-Tracker"
project_version = "2.2.0"
net_manage = NetManage(project_name, project_version)
```

**参数:**

|参数|类型|说明|
|:---|---|---|
|project_name|str|软件项目名称|
|project_version|int|软件项目版本|

### status

> 设备网络状态

**示例:**

```python
net_manage.status
# True
```

**返回值:**

|数据类型|说明|
|:---|---|
|bool|`True` - 网络正常<br>`False` - 网络异常|

### sim_status

> 设备SIM卡状态

**示例:**

```python
net_manage.sim_status
# 1
```

**返回值:**

|数据类型|说明|
|:---|---|
|int|SIM卡状态枚举值|

**SIM卡状态枚举值:**

|枚举值|说明|
|:---|---|
|0|SIM卡不存在/被移除|
|1|SIM已经准备好|
|2|SIM卡已锁定, 等待CHV1密码|
|3|SIM卡已被阻拦, 需要CHV1密码解锁密码|
|4|由于SIM/USIM个性化检查失败, SIM卡被锁定|
|5|由于PCK错误导致SIM卡被阻拦, 需要MEP密码解除阻拦|
|6|需要隐藏电话簿条目的密钥|
|7|需要解锁隐藏密钥的编码|
|8|SIM卡已锁定, 等待CHV2密码|
|9|SIM卡被阻拦, 需要CHV2解锁密码|
|10|由于网络个性化检查失败, SIM卡被锁定|
|11|由于NCK不正确, SIM卡被阻栏, 需要MEP解锁密码|
|12|由于子网络锁个性化检查失败, SIM卡被锁定|
|13|由于错误的NSCK, SIM卡被阻拦, 需要MEP解锁密码|
|14|由于服务提供商个性化检查失败, SIM卡被锁定|
|15|由于SPCK错误, SIM卡被阻拦, 需要MEP解锁密码|
|16|由于企业个性化检查失败, SIM卡被锁定|
|17|由于CCK不正确, SIM卡被阻止, 需要MEP解锁密码|
|18|SIM正在初始化, 等待完成|
|19|使用CHV1/CHV2通用PIN码解锁CHV1码, 解锁CHV2码进而来解锁PIN被阻拦|
|20|SIM卡无效|
|21|未知状态|

### wait_connect

> 等待设备注网

**示例:**

```python
net_manage.wait_connect(timeout=60)
# (3, 1)
```

**参数:**

|参数|类型|说明|
|:---|---|---|
|timeout|int|等待注网超时时间, 单位: s|

**返回值:**

|数据类型|说明|
|:---|---|
|dict|返回一个元组, 格式为: `(stage, state)`|

|参数|类型|说明|
|:---|---|---|
|stage|int|表示当前正在检测什么状态:<br>1 - 正在检测SIM卡状态;<br>2 - 正在检测网络注册状态;<br>3 - 正在检测PDP Context激活状态.|
|state|int|根据stage值, 来表示不同的状态, 具体如下:<br>stage = 1时, state表示 SIM卡的状态, 范围0~21, 每个状态值的详细说明, 请参考sim.getStatus()方法的返回值说明;<br>stage = 2时, state表示网络注册状态, 范围0~11, 每个状态值的详细说明, 请参考net.getState()方法的返回值说明;<br>stage = 3时, state表示PDP Context激活状态, 0表示没有激活成功, 1表示激活成功。|

### connect

> 设备联网

**示例:**

```python
net_manage.connect()
# True
```

**参数:**

无

**返回值:**

|数据类型|说明|
|:---|---|
|bool|`True` - 成功<br>`False` - 失败|

### disconnect

> 设备联网

**示例:**

```python
net_manage.disconnect(4)
# True
```

**参数:**

|参数|类型|说明|
|:---|---|---|
|val|int|0 - 网络全功能关闭<br>4 - 飞行模式<br>默认: 4|

**返回值:**

|数据类型|说明|
|:---|---|
|bool|`True` - 成功<br>`False` - 失败|

### reconnect

> 设备重新注网, 该方法等价于先调用`disconnect`, 再调用`connect`。

**示例:**

```python
net_manage.reconnect()
# True
```

**参数:**

无

**返回值:**

|数据类型|说明|
|:---|---|
|bool|`True` - 成功<br>`False` - 失败|

### sync_time

> 设备同步网络时间

**示例:**

```python
net_manage.sync_time(timezon=8)
# True
```

**参数:**

|参数|类型|说明|
|:---|---|---|
|timezon|int|时区, -12~12, 默认: 8|

**返回值:**

|数据类型|说明|
|:---|---|
|bool|`True` - 成功<br>`False` - 失败|

### set_callback

> 设置网络状态变化回调函数

**示例:**

```python
def net_callback(args):
    print(args)

net_manage.set_callback(callabck=net_callback)
# True
```

**参数:**

|参数|类型|说明|
|:---|---|---|
|callabck|function|回调函数, <br>函数入参`args`, 数据格式`(pdp_id, state)`|

**回调函数参数:**

|参数|类型|说明|
|:---|---|---|
|pdp_id|int|PDP上下文ID, 表示当前是哪一路PDP网络状态发生变化|
|state|int|网络状态, 0表示网络断开, 1表示网络连接成功|

**返回值:**

|数据类型|说明|
|:---|---|
|bool|`True` - 成功<br>`False` - 失败|

## 使用示例

```python
from net_manage import NetManage

# 模块初始化
project_name = "QuecPython-Tracker"
project_version = "2.2.0"
net_manage = NetManage(project_name, project_version)

def net_callback(args):
    print(args)

# 设置网络状态变化回调函数
net_manage.set_callback(net_callback)
# True

# 查询sim卡状态
net_manage.sim_status
# 1

# 查询网络状态
net_manage.status
# False

# 设备重新注网
net_manage.disconnect()
# True
net_manage.connect()
# True
# net_manage.reconnect()
# True

# 等待注网成功
net_manage.wait_connect(timeout=60)
# (3, 1)

# 同步网络时间
net_manage.sync_time()
```
