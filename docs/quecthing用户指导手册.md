# 移远云物联网模块 用户指导手册

## 简介

> 该模块为移远云物联网功能模块, 主要有一下两个功能
>
> - 物模型导入转化类
> - MQTT协议的消息发布与订阅, OTA升级。

## 使用说明

### 1. 物模型初始化

```python
from quecthing import QuecObjectModel

object_model_file = "/usr/quec_object_model.json"
quec_object_model = QuecObjectModel(om_file=object_model_file)
```

### 2. 移远云模块初始化

```python
from quecthing import QuecThing

pk = "ProductKey"
ps = "ProductSecret"
dk = "DeviceKey"
ds = "DeviceSecret"
server = "iot-south.quectel.com:1883"
life_time = 120
mcu_name = "QuecPython-quecthing"
mcu_version = "v2.0.1"
mode = 1
quec = QuecThing(pk, ps, dk, ds, server, life_time, mcu_name, mcu_version, mode)
```

### 3. 注册物模型对象

```python
from quecthing import QuecObjectModel

quec_object_model = QuecObjectModel()
res = quec.set_object_model(quec_object_model)
```

### 4. 添加监听者

```python
from remote import RemoteSubscribe

remote_sub = RemoteSubscribe()
quec.addObserver(remote_sub)
```

### 5. 连接初始化

```python
res = quec.init(enforce=False)
```

### 6. 发布消息(物模型)

```python
data = {
    "phone_num": "123456789",
    "energy": 100,
    "local_time": "1652067872000"
}
res = quec.post_data(data)
```

### 7. 设备固件版本与项目应用版本信息上报

```python
res = quec.device_report()
```

### 8. OTA升级计划查询

```python
res = quec.ota_request()
```

### 9. 确认是否OTA升级

```python
res = quec.ota_action(action, module)
```

### 10. 断开连接

```python
res = quec.close()
```

## API说明

### QuecObjectModel

> - 该模块是将移远云导出的json格式的模型数据转化成一个物模型类, 方便使用
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
|om_file|STRING|物模型文件全路径地址, 可选, 默认`/usr/quec_object_model.json`|

### QuecThing

> 还模块主要提供移远云物联网模块的连接, 消息的发送, 消息订阅, OTA升级功能。
> 
> 该功能以监听者模式进行设计, 本身既是监听者, 亦是被监听者
> 
> - 监听者: 可作为`remote`模块的`RemotePublish`类的监听者, 用于接收其消息的通知, 进行数据的发布.
> - 被监听者: 可作为`remote`模块的`RemoteSubscribe`类的被监听者, 用户通知监听者服务器下发的数据信息.
>
> 该模块继承`common`模块中的`CloudObservable`方法, 其方法见`common`模块文档, 在此不再赘述。

#### 导入初始化

示例:

```python
from quecthing import QuecThing

pk = "ProductKey"
ps = "ProductSecret"
dk = "DeviceKey"
ds = "DeviceSecret"
server = "iot-south.quectel.com:1883"
life_time = 120
mcu_name = "QuecPython-quecthing"
mcu_version = "v2.0.1"
mode = 1
quec = QuecThing(pk, ps, dk, ds, server, life_time, mcu_name, mcu_version, mode)
```

参数:

|参数|类型|说明|
|:---|---|---|
|pk|STRING|产品标识|
|ps|STRING|产品密钥|
|dk|STRING|设备名称|
|ds|STRING|device secret|
|server|STRING|设备密钥|
|life_time|INT|通信之间允许的最长时间段（以秒为单位）, 默认为300, 范围（60-1200）, 默认120|
|mcu_name|STRING|设备模块名称, 默认空字符串|
|mcu_version|STRING|设备模块版本号, 默认空字符串|
|mode|INT|协议类型, 0 - lwm2m, 1 - MQTT, 默认为1|

#### set_object_model 注册物模型对象(`QuecObjectModel`实例)

示例:

```python
from quecthing import QuecObjectModel

quec_object_model = QuecObjectModel()
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
|data|DICT|物模型key, value值|

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
|module|STRING|升级模块, 固件名或项目名, 可选|

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|
