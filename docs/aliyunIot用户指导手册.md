# 阿里云物联网模块 用户指导手册

## 简介

> 该模块为阿里云物联网功能模块, 使用MQTT协议进行通信, 实现设备与服务器数据交互
> 
> 主要支持功能
>
> - 消息发布与订阅
> - OTA升级


## API说明

### AliYunIot

> 该模块主要提供阿里云物联网模块的连接, 消息的发送, 消息订阅。

#### 实例化对象

##### 示例

```python
from aliyunIot import AliYunIot

cloud_cfg = {
    "product_key": "xxx",
    "product_secret": "xxx",
    "device_name": "xxx",
    "device_secret": "xxx",
    "server": "iot-as-mqtt.cn-shanghai.aliyuncs.com",
    "qos": 1,
}
cloud = AliYunIot(**cloud_cfg)
```

##### 参数

|参数|类型|说明|
|:---|---|---|
|product_key|str|产品标识|
|product_secret|str|产品密钥|
|device_name|str|设备名称|
|device_secret|str|设备密钥|
|server|str|访问域名|
|qos|int|消息服务质量(0~1)|

#### status

> 查询服务器连接状态.

##### 示例

```python
conn_status = cloud.status
print(conn_status)
# True
```

##### 返回值

|数据类型|说明|
|:---|---|
|bool|`True` - 已连接<br>`False` - 未连接|

#### auth_info

> 查询认证信息.

##### 示例

```python
auth_info = cloud.auth_info
print(auth_info)
# {"product_key": "xxx", "product_secret": "xxx", "device_name": "xxx", "device_secret": "xxx"}
```

##### 返回值

|数据类型|说明|
|:---|---|
|dict|`product_key` - 产品标识<br>`product_secret` - 产品密钥<br>`device_name` - 设备名称<br>`device_secret` - 设备密钥<br>|

#### add_event

> 添加需要订阅的事件标识, 用于订阅事件发布应答topic.

##### 示例

```python
res = cloud.add_event("sos_alarm")
print(res)
# True
```

##### 参数

|参数|类型|说明|
|:---|---|---|
|event|str|事件标识|

##### 返回值

|数据类型|说明|
|:---|---|
|bool|`True` - 成功<br>`False` - 失败|

#### add_service

> 添加需要订阅的服务标识, 用于订阅服务topic.

##### 示例

```python
res = cloud.add_service("report_location")
print(res)
# True
```

##### 参数

|参数|类型|说明|
|:---|---|---|
|service|str|服务标识|

##### 返回值

|数据类型|说明|
|:---|---|
|bool|`True` - 成功<br>`False` - 失败|

#### set_callback

> 设置接收服务端下发的数据信息.

##### 示例

```python
def cloud_callback(args):
    print("topic: %s, data: %s" % (args[0], args[1]))

cloud.set_callback(cloud_callback)
```

##### 参数

|参数|类型|说明|
|:---|---|---|
|callback|function|用于接收服务端下发的数据信息,<br>函数入参`args`, 数据格式`(topic, data)`|

##### 返回值

无

#### connect

> 连接登录阿里云服务器.

##### 示例

```python
res = cloud.connect()
print(res)
# 0
```

##### 参数

无

#### disconnect

> 断开阿里云服务器连接.

##### 示例

```python
res = cloud.disconnect()
print(res)
# True
```

##### 参数

无

##### 返回值

|数据类型|说明|
|:---|---|
|bool|`True` - 成功<br>`False` - 失败|

#### properties_report

> 物模型属性上报.

##### 示例

```python
data = {
    "phone_num": "123456789",
    "energy": 100,
    "GeoLocation": {
        "Longitude": 100.26,
        "Latitude": 26.86,
        "Altitude": 0.0,
        "CoordinateSystem": 1
    }
}
res = cloud.properties_report(data)
print(res)
# True
```

##### 参数

|参数|类型|说明|
|:---|---|---|
|data|dict|物模型数据|

##### 返回值

|数据类型|说明|
|:---|---|
|bool|`True` - 成功<br>`False` - 失败|

#### event_report

> 事件上报.

##### 示例

```python
event = "sos_alarm"
data = {
    "time": str(utime.mktime(utime.local_time()) * 1000),
}
res = cloud.event_report(event, data)
print(res)
# True
```

##### 参数

|参数|类型|说明|
|:---|---|---|
|event|str|事件标识|
|data|dict|事件相关信息|

##### 返回值

|数据类型|说明|
|:---|---|
|bool|`True` - 成功<br>`False` - 失败|

#### service_response

> 服务消息应答.

##### 示例

```python
service = "report_location"
code = 200
data = {
    "GeoLocation": {
        "Longitude": 100.26,
        "Latitude": 26.86,
        "Altitude": 0.0,
        "CoordinateSystem": 1
    }
}
msg_id = "102"
message = "success"
res = cloud.service_response(service, code, data, msg_id, message)
print(res)
# True
```

##### 参数

|参数|类型|说明|
|:---|---|---|
|service|str|服务标识|
|code|int|成功标识, 200 - 成功, 其他 - 失败|
|data|dict|服务相关信息|
|msg_id|str|消息id|
|message|str|备注信息|

##### 返回值

|数据类型|说明|
|:---|---|
|bool|`True` - 成功<br>`False` - 失败|

#### rrpc_response

> RRPC下发消息应答.

##### 示例

```python
msg_id = "103"
data = {
    "phone_num": "123456789",
}
res = cloud.rrpc_response(msg_id, data)
print(res)
# True
```

##### 参数

|参数|类型|说明|
|:---|---|---|
|msg_id|str|消息id|
|data|dict|RRPC相关信息|

##### 返回值

|数据类型|说明|
|:---|---|
|bool|`True` - 成功<br>`False` - 失败|

#### property_set_reply

> 属性设置消息应答.

##### 示例

```python
msg_id = "103"
code = 200
msg = "success"
res = cloud.property_set_reply(msg_id, code, msg)
print(res)
# True
```

##### 参数

|参数|类型|说明|
|:---|---|---|
|msg_id|str|消息id|
|code|int|成功标识, 200 - 成功, 其他 - 失败|
|msg|str|备注信息|

##### 返回值

|数据类型|说明|
|:---|---|
|bool|`True` - 成功<br>`False` - 失败|

#### ota_device_inform

> 设备模块标识与版本上报.

##### 示例

```python
# Software module and version
module = "QuecPython-Tracker"
version = "2.2.0"
# Firmware module and version
# module = "EC600N-CNLC"
# version = "EC600NCNLCR03A11M16_OCPU_QPY_BETA0313"
res = cloud.ota_device_inform(version, module)
print(res)
# True
```

##### 参数

|参数|类型|说明|
|:---|---|---|
|module|str|模块标识|
|version|str|版本信息|

##### 返回值

|数据类型|说明|
|:---|---|
|bool|`True` - 成功<br>`False` - 失败|

#### ota_firmware_get

> 设备模块OTA升级计划查询.

##### 示例

```python
# Software module and version
module = "QuecPython-Tracker"
# Firmware module and version
# module = "EC600N-CNLC"
res = cloud.ota_firmware_get(module)
print(res)
# True
```

##### 参数

|参数|类型|说明|
|:---|---|---|
|module|str|模块标识|

##### 返回值

|数据类型|说明|
|:---|---|
|bool|`True` - 成功<br>`False` - 失败|

#### ota_device_progress

> 设备模块OTA升级进度上报.

##### 示例

```python
step = 100
desc = "success."
# Software module and version
module = "QuecPython-Tracker"
# Firmware module and version
# module = "EC600N-CNLC"
res = cloud.ota_device_progress(step, desc, module)
print(res)
# True
```

##### 参数

|参数|类型|说明|
|:---|---|---|
|step|int|-1 - 取消升级<br> 1~100 - 升级进度|
|desc|str|备注信息|
|module|str|模块标识|

##### 返回值

|数据类型|说明|
|:---|---|
|bool|`True` - 成功<br>`False` - 失败|

### AliYunOTA

> 该模块主要提供阿里云物联网模块的连接, 消息的发送, 消息订阅。

#### 实例化对象

##### 示例

```python
from aliyunIot import AliYunOTA

project_name = "QuecPython-Tracker"
firmware_name = "EC600N-CNLC"
cloud_ota = AliYunOTA(project_name, firmware_name)
```

##### 参数

|参数|类型|说明|
|:---|---|---|
|project_name|str|软件模块标识|
|firmware_name|str|硬件模块标识|

#### set_cloud

> 设置`AliYunIot`实例化对象, 用于上报升级进度.

##### 示例

```python
cloud_ota.set_cloud(cloud)
```

##### 参数

|参数|类型|说明|
|:---|---|---|
|cloud|object|`AliYunIot`对象|

##### 返回值

无

#### set_ota_data

> 设置OTA升级计划具体信息.

##### 示例

```python
cloud_ota.set_ota_data(data)
```

##### 参数

|参数|类型|说明|
|:---|---|---|
|data|dict|[阿里云OTA升级包信息](https://help.aliyun.com/document_detail/85700.html#section-nm2-m4c-r2b)|

##### 返回值

无

#### get_ota_info

> 获取OTA升级模块标识与目标版本号.

##### 示例

```python
data = cloud_ota.get_ota_info()
```

##### 参数

无

##### 返回值

|数据类型|说明|
|:---|---|
|dict|`ota_module` - 升级模块标识<br>`ota_version` - 升级目标版本号|

#### start

> 开始OTA升级.

##### 示例

```python
data = cloud_ota.start()
```

##### 参数

无

##### 返回值

|数据类型|说明|
|:---|---|
|bool|`True` - 成功<br>`False` - 失败|

## 使用示例

```python
from misc import Power
from aliyunIot import AliYunIot, AliYunOTA


def cloud_callback(args):
    global cloud, cloud_ota
    topic, data = args
    if "/thing/service/" in topic:
        # 服务信息下发处理应答
        service = topic.split("/")[-1]
        code = 200
        data = {}
        msg_id = data["id"]
        message = "success"
        cloud.service_response(service, code, data, msg_id, message)
    elif "/rrpc/request/" in topic:
        # RRPC同步消息下发处理应答
        msg_id = topic.split("/")[-1]
        data = {}
        cloud.rrpc_response(msg_id, data)
    elif "/thing/service/property/set" in topic:
        # 物模型数据下发处理应答
        msg_id = data["id"]
        code = 200
        msg = "success"
        cloud.property_set_reply(msg_id, code, msg)
    elif topic.startswith("/ota/device/inform/") or topic.endswith("/ota/firmware/get_reply"):
        # OTA升级计划下发
        cloud_ota.set_ota_data(data)
        step = 1
        desc = "start ota."
        ota_module = cloud_ota.get_ota_info()["ota_module"]
        # OTA升级进度上报
        cloud.ota_device_progress(step, desc, ota_module)
        if cloud_ota.start():
            cloud.ota_device_progress(100, "success", ota_module)
        else:
            cloud.ota_device_progress(100, "failed", ota_module)
        Power.powerRestart()


# 阿里云模块初始化
cloud_cfg = {
    "product_key": "xxx",
    "product_secret": "xxx",
    "device_name": "xxx",
    "device_secret": "xxx",
    "server": "iot-as-mqtt.cn-shanghai.aliyuncs.com",
    "qos": 1,
}
cloud = AliYunIot(**cloud_cfg)

# 阿里云OTA模块初始化
project_name = "QuecPython-Tracker"
firmware_name = "EC600N-CNLC"
cloud_ota = AliYunOTA(project_name, firmware_name)

# 阿里云模块注册回调函数
cloud.set_callback(cloud_callback)

# 添加事件
cloud.add_event("sos_alarm")
cloud.add_event("low_power_alarm")

# 添加服务
cloud.add_service("query_phone_num")
cloud.add_service("query_power_level")

# 连接服务
cloud.connect()

# 物模型属性上报
data = {
    "phone_num": "123456789",
    "energy": 100,
    "GeoLocation": {
        "Longitude": 100.26,
        "Latitude": 26.86,
        "Altitude": 0.0,
        "CoordinateSystem": 1
    }
}
cloud.properties_report(data)

# 事件上报
event = "low_power_alarm"
data = {"power_level": 20}
cloud.event_report(event, data)

# 软件模块版本信息上报
PROJECT_NAME = "QuecPython-Tracker-Laike"
PROJECT_VERSION = "1.1.0"
cloud.ota_device_inform(PROJECT_VERSION, PROJECT_NAME)

# 软件模块OTA升级计划查询
cloud.ota_firmware_get(PROJECT_NAME)

# 断开服务器连接
cloud.disconnect()
```
