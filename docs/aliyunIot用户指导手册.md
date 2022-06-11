# 阿里云物联网模块 用户指导手册

## 简介

> 该模块为阿里云物联网功能模块, 主要有一下两个功能
>
> - 物模型导入转化类
> - MQTT协议的消息发布与订阅, OTA升级。

## 功能接口说明

### AliObjectModel

> 该模块是将阿里云导出的json格式的精简物模型数据转化成一个物模型类，方便使用

示例:

```python
from aliyunIot import AliObjectModel

object_model_file = "/usr/aliyun_object_model.json"
ali_object_model = AliObjectModel(om_file=object_model_file)

print(ali_object_model.properties.power_switch)
# {"power_switch": True}
print(ali_object_model.properties.GeoLocation)
# {"GeoLocation": {"Longitude": 0.0, "Latitude": 0.0, "Altitude": 0.0, "CoordinateSystem": 0}}
print(ali_object_model.events.sos_alert)
# {"sos_alert": {"local_time": 0, "GeoLocation": {"Longitude": 0.0, "Latitude": 0.0, "Altitude": 0.0, "CoordinateSystem": 0}}}
```

参数:

|参数|类型|说明|
|:---|---|---|
|om_file|STRING|物模型文件全路径地址，可选，默认`/usr/aliyun_object_model.json`|

### AliYunIot

> 还模块主要提供阿里云物联网模块的连接，消息的发送，消息订阅，OTA升级功能。
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

#### set_object_model 注册物模型对象(`AliObjectModel`实例)

示例:

```python
from aliyunIot import AliYunIot, AliObjectModel

ali_object_model = AliObjectModel()

ali = AliYunIot(pk, ps, dk, ds, server, client_id)
res = ali.set_object_model(ali_object_model)
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
res = ali.init(enforce=False)
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
res = ali.close()
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
res = ali.get_status()
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
res = ali.post_data(data)
```

参数:

|参数|类型|说明|
|:---|---|---|
|data|DICT|物模型key，value值|

```json
{
    "phone_num": "123456789",
    "energy": 100,
    "GeoLocation": {
        "Longtitude": 100.26,
        "Latitude": 26.86,
        "Altitude": 0.0,
        "CoordinateSystem": 1
    }
}
```

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`已连接, `False`未连接|

#### rrpc_response MQTT同步通信(RRPC)消息应答

示例:

```python
res = ali.rrpc_response(message_id, data)
```

参数:

|参数|类型|说明|
|:---|---|---|
|message_id|STRING|RRPC消息id|
|data|STRING/DICT|RRPC应答消息内容|

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|

#### device_report 设备固件版本与项目应用版本信息上报

示例:

```python
res = ali.device_report()
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
res = ali.ota_request()
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
res = ali.ota_action(action, module)
```

参数:

|参数|类型|说明|
|:---|---|---|
|action|INT| 0 取消升级, 1 确认升级|
|module|STRING|升级模块，固件名或项目名|

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|

#### ota_device_inform 设备模块版本信息上报

示例:

```python
res = ali.ota_device_inform(version, module)
```

参数:

|参数|类型|说明|
|:---|---|---|
|version|STRING| 模块版本信息 |
|module|STRING| 模块名称 |

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|

#### ota_device_progress 设备上报升级进度

示例:

```python
res = ali.ota_device_progress(step, desc, module)
```

参数:

|参数|类型|说明|
|:---|---|---|
|step|STRING| OTA升级进度。取值范围：1~100的整数：升级进度百分比。-1：升级失败。-2：下载失败。-3：校验失败。-4：烧写失败。 |
|desc|STRING| 当前步骤的描述信息，长度不超过128个字符。如果发生异常，此字段可承载错误信息。 |
|module|STRING| 升级包所属的模块名。 |

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|

#### ota_firmware_get 设备请求OTA升级包信息

示例:

```python
res = ali.ota_firmware_get(module)
```

参数:

|参数|类型|说明|
|:---|---|---|
|module|STRING| 升级包所属的模块名。 |

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|

#### ota_file_download 设备请求下载文件分片

示例:

```python
res = ali.ota_file_download(fileToken, streamId, fileId, size, offset)
```

参数:

|参数|类型|说明|
|:---|---|---|
|fileToken|STRING|文件的唯一标识Token |
|streamId|STRING|通过MQTT协议下载OTA升级包时的唯一标识。 |
|fileId|STRING|单个升级包文件的唯一标识。 |
|size|STRING|请求下载的文件分片大小，单位字节。取值范围为256 B~131072 B。若为最后一个文件分片，取值范围1 B~131072 B。 |
|offset|STRING|文件分片对应字节的起始地址。取值范围为0~16777216。 |

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|
