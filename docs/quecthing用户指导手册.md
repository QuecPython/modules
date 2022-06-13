# 移远云物联网模块 用户指导手册

## 简介

> 该模块为移远云物联网功能模块, 主要有一下两个功能
>
> - 物模型导入转化类
> - MQTT协议的消息发布与订阅, OTA升级。

## 功能接口说明

### QuecObjectModel

> - 该模块是将移远云导出的json格式的模型数据转化成一个物模型类，方便使用
> - 该类初始化完成后有三个属性, 为`properties`, `events`, `services`, 且每个属性为一个对象;
> - 物模型具体的key值为`properties`, `events`, `services`对象的属性, 属性值为默认的数据类型值;

示例:

```python
from quecthing import QuecObjectModel

object_model_file = "/usr/quec_object_model.json"
quec_object_model = QuecObjectModel(om_file=object_model_file)

print(quec_object_model.properties.power_switch)
# {"power_switch": True}
print(quec_object_model.properties.GeoLocation)
# {"GeoLocation": {"Longitude": 0.0, "Latitude": 0.0, "Altitude": 0.0, "CoordinateSystem": 0}}
print(quec_object_model.events.sos_alert)
# {"sos_alert": {"local_time": 0, "GeoLocation": {"Longitude": 0.0, "Latitude": 0.0, "Altitude": 0.0, "CoordinateSystem": 0}}}
print(ali_object_model.services.test_service)
# {"input": {"query_device_info": ""}, "output": {"local_time": 0}}
```

参数:

|参数|类型|说明|
|:---|---|---|
|om_file|STRING|物模型文件全路径地址，可选，默认`/usr/quec_object_model.json`|

### QuecThing

> 还模块主要提供移远云物联网模块的连接，消息的发送，消息订阅，OTA升级功能。
> 
> 该功能以监听者模式进行设计, 本身既是监听者, 亦是被监听者
> 
> - 监听者: 可作为`remote`模块的`RemotePublish`类的监听者, 用于接收其消息的通知, 进行数据的发布.
> - 被监听者: 可作为`remote`模块的`RemoteSubscribe`类的被监听者, 用户通知监听者服务器下发的数据信息.

#### addObserver 添加监听者

示例:

```python
from remote import RemoteSubscribe

remote_sub = RemoteSubscribe()

ali.addObserver(remote_sub)
```

参数:

|参数|类型|说明|
|:---|---|---|
|observer|OBJECT|监听者类实例对象|

返回值:

无

#### delObserver 删除监听者

示例:

```python
ali.delObserver(remote_sub)
```

参数:

|参数|类型|说明|
|:---|---|---|
|observer|OBJECT|监听者类实例对象|

返回值:

无

#### set_object_model 注册物模型对象(`QuecObjectModel`实例)

示例:

```python
from quecthing import QuecThing, QuecObjectModel

quec_object_model = QuecObjectModel()

quec = QuecThing(pk, ps, dk, ds, server)
res = quec.set_object_model(quec_object_model)
```

参数:

|参数|类型|说明|
|:---|---|---|
|object_model|OBJECT|物模型类实例对象|

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|

#### init 连接初始化

示例:

```python
res = quec.init(enforce=False)
```

参数:

|参数|类型|说明|
|:---|---|---|
|enforce|BOOL|是否重新连接, True 是, False 否, 默认否|

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|

#### close 断开连接

示例:

```python
res = quec.close()
```

参数:

无

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|

#### get_status 查询连接状态

示例:

```python
res = quec.get_status()
```

参数:

无

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`已连接, `False`未连接|

#### post_data 发布消息(物模型)

示例:

```python
res = quec.post_data(data)
```

参数:

|参数|类型|说明|
|:---|---|---|
|data|DICT|物模型key，value值|

```json
{
    "phone_num": "123456789",
    "energy": 100,
    "local_time": "1652067872000"
}
```

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|

#### device_report 设备固件版本与项目应用版本信息上报

示例:

```python
res = quec.device_report()
```

参数:

无

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|

#### ota_request OTA升级计划查询

示例:

```python
res = quec.ota_request()
```

参数:

无

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|

#### ota_action 确认是否OTA升级

示例:

```python
res = quec.ota_action(action, module)
```

参数:

|参数|类型|说明|
|:---|---|---|
|action|INT| 0 取消升级, 1 确认升级|
|module|STRING|升级模块，固件名或项目名, 可选|

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|
