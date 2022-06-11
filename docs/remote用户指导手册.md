# 云端中间件模块 用户指导手册

## 简介

> 该模块作用于云服务与设备直接消息交互的中间件

## 功能接口说明

### RemoteSubscribe 云端消息下发

> 该模块采用监听者设计模式，该模块继承`CloudObserver`
> 
> - 相对云端接口，该模块为监听者，接收云端下发的消息
> - 相对业务处理模块，该模块为被监听者，当收到云端下发的消息后，通知业务模块

#### 模块导入

示例:

```python
from remote import RemoteSubscribe
remote_sub = RemoteSubscribe()
```

#### add_executor 添加业务处理模块对象

> 业务处理模块需包含一下几个方法，作为监听者接收消息函数，当不包含这些方法时，则不会将云端下发的对应功能的消息通知到业务模块。
> 
> - `event_option` 透传模式数据接收
> - `event_done` 物模型设置数据接收
> - `event_query` 物模型查询数据接收
> - `event_ota_plain` OTA升级计划数据接收
> - `event_ota_file_download` OTA文件分片下载数据接收
> - `rrpc_request` RRPC请求消息数据接收

示例:

```python

class cloudExecutor(object):
    pass

cloud_executor = cloudExecutor()
res = remote_sub.add_executor(cloud_executor)
```

参数:

|参数|类型|说明|
|:---|---|---|
|executor|OBJECT|业务处理模块对象|

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|

#### execute 添加业务处理模块对象

示例:

```python
from aliyunIot import AliYunIot
ali = AliYunIot(pk, ps, dk, ds, server, client_id)
ali.addObserver(remote_sub)
remote_sub.execute(ali, *args, **kwargs)
```

参数:

|参数|类型|说明|
|:---|---|---|
|observable|OBJECT|被监听者实例对象|
|args|TUPLE|元组数据, 元素1即observable|
|kwargs|DICT|字典数据|

返回值:

无

### RemotePublish 云端消息发布

> 该模块采用监听者设计模式，该模块继承`Observable`
> 
> - 相对于业务模块，该模块作为监听者，接收业务模块的消息发送信息
> - 相对于云功能模块，该模块作为被监听者，当有数据需要进行发送时，通知云功能模块
> - 同时该模块也作为`History`模块的被监听者，当消息发送失败时，发送失败的数据通知给`History`模块进行存储

#### 模块导入

示例:

```python
from remote import RemotePublish
remote_pub = RemotePublish()
```

#### add_cloud 添加云功能模块对象

示例:

```python
from aliyunIot import AliYunIot
ali = AliYunIot(pk, ps, dk, ds, server, client_id)
res = remote_pub.add_cloud(ali)
```

参数:

|参数|类型|说明|
|:---|---|---|
|cloud|OBJECT|云功能实例对象|

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|

#### cloud_ota_check OTA升级计划查询

示例:

```python
res = remote_pub.cloud_ota_check()
```

参数:

无

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|

#### cloud_ota_action OTA升级确认

示例:

```python
res = remote_pub.cloud_ota_action(action, module)
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

#### cloud_device_report 设备模块版本信息上报

示例:

```python
res = remote_pub.cloud_device_report()
```

参数:

无

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|

#### cloud_rrpc_response MQTT同步通信消息应答

示例:

```python
res = remote_pub.cloud_rrpc_response(message_id, data)
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

#### post_data 物模型消息发布

> 当消息发送失败时，会通知已注册的监听者`History`进行消息存储

示例:

```python
data = {
    "switch": True,
    "energy": 100,
}
res = remote_pub.post_data(data)
```

参数:

|参数|类型|说明|
|:---|---|---|
|data|DICT|物模型消息数据|

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|
