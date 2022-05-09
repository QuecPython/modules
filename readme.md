# 独立功能模块 API v2.1.0

## 简介

- 该项目将不同的功能进行了独立的封装，每个文件都是一个单独的模块，可以进行独立使用
- 所有模块都采用了观察者模式的设计方式
- 模块之间的组合使用可使用注册观察者和被观察者的方式进行组合使用，将模块之间的耦合性降到最低

## aliyunIot 阿里云物联网模块

> 该模块用于提供阿里云物联网模块相关功能，MQTT协议的消息发布与订阅, OTA升级。

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
    },
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

## battery 设备电池模块

### Battery

> 该模块用于查询当前设备的电池电量与电压，设备的充电状态。

#### 导入

示例:

```python
from battery import Battery

adc_args = (adc_num, adc_period, factor)
chrg_gpion = 0
stdby_gpion = 1

battery = Battery(adc_args=adc_args, chrg_gpion=chrg_gpion, stdby_gpion=stdby_gpion)
```

参数:

|参数|类型|说明|
|:---|---|---|
|adc_args|TUPLE|元素1: [ADC通道](https://python.quectel.com/wiki/#/zh-cn/api/QuecPythonClasslib?id=%e8%af%bb%e5%8f%96%e9%80%9a%e9%81%93%e7%94%b5%e5%8e%8b%e5%80%bc), 元素2: ADC循环读取次数, 元素3: 计算系数，可选|
|chrg_gpion|INT|CHRG （引脚 1）：漏极开路输出的充电状态指示端。可选|
|stdby_gpion|INT|STDBY （引脚 5）：电池充电完成指示端。可选|

#### set_temp 设置温度

> 设置当前设备所处工作环境温度，用于计算设备电池电量

示例:

```python
res = battery.set_temp(20)
```

参数:

|参数|类型|说明|
|:---|---|---|
|temp|INT/FLOAT|温度值, 单位:摄氏度 |

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|

#### get_voltage 获取电池电压

示例:

```python
res = battery.get_voltage()
```

参数:

无

返回值:

|数据类型|说明|
|:---|---|
|INT|电池电压，单位mV。|

#### get_energy 获取电池电量

示例:

```python
res = battery.get_energy()
```

参数:

无

返回值:

|数据类型|说明|
|:---|---|
|INT|电池电量百分比，0~100。|

#### set_charge_callback 充电事件回调函数

示例:

```python
def charge_callback(charge_status):
    print(charge_status)

res = battery.set_charge_callback(charge_callback)
```

参数:

|参数|类型|说明|
|:---|---|---|
|charge_callback|FUNCTION|充电事件回调函数，回调函数参数为设备充电状态: 0-未充电；1-充电中；2-充电完成|

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|

#### get_charge_status 充电状态查询

示例:

```python
res = battery.get_charge_status()
```

参数:

无

返回值:

|数据类型|说明|
|:---|---|
|INT|0-未充电；1-充电中；2-充电完成|

## common 公用模块

> 该模块封装了一些公用组件与基类，方便其他模块使用

### LOWENERGYMAP 不同设备支持的低功耗模式表

| 设备型号 | 支持低功耗模式 |
|---|---|
| EC200U | POWERDOWN,PM |
| EC600N | PM |
| EC800G | PM |

### numiter 数字迭代器

> 返回一个指定整形数值范围的数字迭代器, 默认数值范围0~99999

示例:

```python
from common import numiter

num_iter = numiter(num=10)
print(next(num_iter))
# 0
print(next(num_iter))
# 1
print(next(num_iter))
# 2
```

参数:

|参数|类型|说明|
|:---|---|---|
|num|INT|迭代数值范围，默认99999|

返回值:

|数据类型|说明|
|:---|---|
|OBJECT|迭代器对象, 可使用`next`方法获取数值|

### option_lock 函数锁装饰器

> 用于需要上锁的函数功能

示例:

```python
import _thread
from common import option_lock

_fun_lock = _thread.allocate_lock()

@option_lock(_fun_lock)
def test_lock_fun(args):
    print(args)

```

参数:

|参数|类型|说明|
|:---|---|---|
|thread_lock|OBJECT|线程锁实例对象|

### BaseError 异常提示基类

示例:

```python
from common import BaseError

class TestError(BaseError):
    pass

def test_error():
    raise TestError("test error.")

# Traceback (most recent call last):
#   File "<stdin>", line 55, in <module>
#   File "<stdin>", line 6, in test_error
# TestError: test error.
```

### Singleton 单例基类

> 当需要控制一个类在整个项目中不被重复实例化, 可继承该类实现类不被重复实例化的功能

示例:

```python
from common import Singleton

class TestOne(Singleton):
    pass

class TestTwo(Singleton):
    pass

a = TestOne()
b = TestOne()
c = TestTwo()
d = TestTwo()

print(a)
# <TestOne object at 7e842d40>
print(b)
# <TestOne object at 7e842d40>
print(c)
# <TestTwo object at 7e842eb0>
print(d)
# <TestTwo object at 7e842eb0>
```

### Observer 监听者基类

> 监听模式中的监听者基类, 当被监听者发生变化时, 通知监听者消息进行处理

#### update 监听者消息接收接口

参数:

|参数|类型|说明|
|:---|---|---|
|observable|OBJECT|被监听者实例对象|
|args|TUPLE|元组数据, 元素1即observable|
|kwargs|DICT|字典数据|

返回值:

无

### Observable 被监听者基类

> 监听模式中的被监听者基类，动态注册与移除监听者，通知监听者信息

#### addObserver 添加监听者

参数:

|参数|类型|说明|
|:---|---|---|
|observer|OBJECT|监听者实例对象|

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|

#### delObserver 移除监听者

参数:

|参数|类型|说明|
|:---|---|---|
|observer|OBJECT|监听者实例对象|

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|

#### notifyObservers 通知监听者消息

参数:

|参数|类型|说明|
|:---|---|---|
|args|TUPLE|元组数据|
|kwargs|DICT|字典数据|

返回值:

无

示例:

```python
from common import Observer, Observable

class Boss(Observer):

    def __init__(self, name):
        self.name = name

    def update(self, observable, *args, *kwargs):
        print("%s recive %s work report: %s" % (self.name, args[1], args[2]))

class Employee(Observable):

    def __init__(self, name):
        self.name = name

    def submit_work_report(self, report):
        self.notifyObservers(self, self.name, report)

Henry = Boss("Henry")
Tony = Employee("Tony")
Jimmy = Employee("Jimmy")
Tony.addObserver(Henry)
Jimmy.addObserver(Henry)
Tony.submit_work_report("2000-01-01 work over")
# Henry recive Tony work report: 2000-01-01 work over
Jimmy.submit_work_report("2000-01-01 work deferral")
# Henry recive Jimmy work report: 2000-01-01 work deferral

Jimmy.delObserver(Henry)
Leaf = Boss("Leaf")
Jimmy.addObserver(Leaf)
Jimmy.submit_work_report("2001-01-01 work over")
# Leaf recive Jimmy work report: 2001-01-01 work over
```

### CloudObserver 云服务监听者基类

> 针对云服务中间件封装的监听者基类，当云端下发指令到设备时，通过监听者进行消息的分类转发

#### execute 监听者消息接收接口

参数:

|参数|类型|说明|
|:---|---|---|
|observable|OBJECT|被监听者实例对象|
|args|TUPLE|元组数据, 元素1即observable|
|kwargs|DICT|字典数据|

返回值:

无

### CloudObservable 云服务被监听者基类

> 云服务被监听者基类，用于定义封装的不同云服务方法的基本功能，方便统一不同云的兼容使用，用户可根据不同的云服务编写`init`, `close`, `post_data`, `ota_request`, `ota_action`方法

#### addObserver 添加监听者

参数:

|参数|类型|说明|
|:---|---|---|
|observer|OBJECT|监听者实例对象|

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|

#### delObserver 移除监听者

参数:

|参数|类型|说明|
|:---|---|---|
|observer|OBJECT|监听者实例对象|

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|

#### notifyObservers 通知监听者消息

参数:

|参数|类型|说明|
|:---|---|---|
|args|TUPLE|元组数据|
|kwargs|DICT|字典数据|

返回值:

无

#### init 云服务连接初始化

参数:

|参数|类型|说明|
|:---|---|---|
|enforce|BOOL|是否强制重连|

返回值:

无

#### close 云服务断开连接

参数:

无

返回值:

无

#### post_data 发送消息

参数:

|参数|类型|说明|
|:---|---|---|
|data|DICT|发送消息体|

返回值:

无

#### ota_request OTA升级计划查询

参数:

|参数|类型|说明|
|:---|---|---|
|args|TUPLE|元组数据|
|kwargs|DICT|字典数据|

返回值:

无

#### ota_action OTA升级确认

参数:

|参数|类型|说明|
|:---|---|---|
|action|INT|0-取消升级;1-确认升级|
|module|STRING|升级模块，非必填|

返回值:

无

### CloudObjectModel 云服务物模型基类

> 将物模型转换成抽象类的方法，方便项目使用，用户可根据不同的云服务的物模型重写`init`方法

#### init 物模型json文件解析

参数:

无

返回值:

无

## history 历史文件模块

> 该模块主要用于读取记录与清理历史数据文件，该模块设计成监听者模式，可以和`remote`模块结合使用，当`remote`发送消息失败时，将消息通知给`history`模块，存入历史文件中

### History

#### 模块导入

示例:

```python
from history import History

hist = History(history_file="/usr/tracker_data.hist", max_hist_num=100)
```

参数:

|参数|类型|说明|
|:---|---|---|
|history_file|STRING|全路径历史文件名称，默认`/usr/tracker_data.hist`|
|max_hist_num|INT|最大存储历史数据条数，默认100|

#### read 读取历史文件

> 将历史文件中的数据读取出来，并将历史文件清空，防止重复读取

示例:

```python
data = hist.read()
print(data)
# {"data": [{"local_time": 1651136994000}]}
```

参数:

无

返回值:

|数据类型|说明|
|:---|---|
|DICT|key值为`data`, value值为列表，列表元素为存入的历史数据|

#### write 写入历史文件

> 将数据写入历史文件中，当文件中有数据时，则在文件中追加写入，并保证总写入的数据不大于设置的最大保存数据条数

示例:

```python
data = [{"local_time": 1651136994000}, {"local_time": 1651136995000}]
res = hist.write(data)
```

参数:

|参数|类型|说明|
|:---|---|---|
|data|LIST|列表数据，元素根据具体业务具体定义即可|

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|

#### clean 清除历史文件

> 将历史数据文件清除

示例:

```python
res = hist.clean()
```

参数:

无

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|

#### update 监听者消息接收接口

> 被监听者将需要存储的数据传递给监听者`History`进行数据存储

示例:

```python
hist.update(observable, *args, **kwargs)
```

参数:

|参数|类型|说明|
|:---|---|---|
|observable|OBJECT|被监听者实例对象|
|args|TUPLE|元组数据, 元素1即observable, 元素1之后的所有元素即为需要存储的数据列表即`args[1:]`|
|kwargs|DICT|字典数据, 扩展数据暂无用处|

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|

## led LED模块(开发中)

### LED

> 该模块功能用于控制模块LED灯的开关与周期性闪烁

#### 模块导入

示例:

```python
from machine import Pin
from led import LED

GPIOn = Pin.GPIO1
direction = Pin.OUT
pullMode = Pin.PULL_DISABLE
level = 0

led = LED(GPIOn, direction=direction, pullMode=pullMode, level=level)
```

参数:

|参数|类型|说明|
|:---|---|---|
|GPIOn|INT|引脚号|
|direction|INT|Pin.IN – 输入模式，Pin.OUT – 输出模式，默认Pin.OUT|
|pullMode|INT|Pin.PULL_DISABLE – 浮空模式, Pin.PULL_PU – 上拉模式, Pin.PULL_PD – 下拉模式, 默认Pin.PULL_DISABLE|
|level|INT|0 - 设置引脚为低电平, 1- 设置引脚为高电平，默认0|

#### get_period 获取LED闪烁周期

示例:

```python
period = led.get_period()
```

参数:

无

返回值:

|数据类型|说明|
|:---|---|
|INT|闪烁周期, 单位ms|

#### set_period 设置LED闪烁周期

示例:

```python
period = 1000
res = led.set_period(period)
```

参数:

|参数|类型|说明|
|:---|---|---|
|period|INT|闪烁周期, 单位ms|

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|

#### start_flicker 开启LED闪烁

示例:

```python
res = led.start_flicker()
```

参数:

无

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|

#### stop_flicker 停止LED闪烁

示例:

```python
res = led.stop_flicker()
```

参数:

无

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|

#### get_led_status 获取LED当前开关状态

示例:

```python
status = led.get_led_status()
```

参数:

无

返回值:

|数据类型|说明|
|:---|---|
|INT|0 - 关, 1 - 开|

#### set_led_status 设置LED当前开关状态

示例:

```python
onoff = 1
res = led.set_led_status(onoff)
```

参数:

|参数|类型|说明|
|:---|---|---|
|onoff|INT|0 - 关, 1 - 开|

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|

#### switch 反转当前LED开关状态

> 根据当前LED开关状态自动转换，当前LED状态为关时，则开，当前状态为开时，则关

示例:

```python
res = led.switch()
```

参数:

无

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|

## location 位置信息模块

> 本模块使用的定位坐标系为WGS-84, 如需转换GCJ-02坐标系，本模块提供了`WGS84ToGCJ02`方法进行经纬度坐标系的转换

### WGS84ToGCJ02

> 经纬度坐标系转换

示例:

```python
from location import WGS84ToGCJ02

wgs84_longtitude = 117.1154593833333
wgs84_latitude = 31.82221683333333

gcj02_longtitude, gcj02_latitude = WGS84ToGCJ02(wgs84_longtitude, wgs84_latitude)
print(gcj02_longtitude, gcj02_latitude)
# 117.121085101472 31.82038457486135
```

参数:

|参数|类型|说明|
|:---|---|---|
|lon|FLOAT|WGS84经度|
|lat|FLOAT|WGS84纬度|

返回值:

|数据类型|说明|
|:---|---|
|TUPLE|元素1: GCJ02经度, 元素2: GCJ02纬度|

### GPSMatch

> GPS NMEA明码语句匹配

#### GxRMC RMC(推荐的最小具体 GNSS 数据)

参数:

|参数|类型|说明|
|:---|---|---|
|gps_data|STRING|GPS明码语句|

返回值:

|数据类型|说明|
|:---|---|
|STRING|RMC语句|

#### GxGGA GGA(全球定位系统定位数据，如时间、定位等)

参数:

|参数|类型|说明|
|:---|---|---|
|gps_data|STRING|GPS明码语句|

返回值:

|数据类型|说明|
|:---|---|
|STRING|GGA语句|

#### GxVTG VTG(矢量跟踪与对地速度)

参数:

|参数|类型|说明|
|:---|---|---|
|gps_data|STRING|GPS明码语句|

返回值:

|数据类型|说明|
|:---|---|
|STRING|VTG语句|

#### GxGSV GSV(可见的 GNSS 卫星，例如可见的卫星数、卫星 ID 号等)

参数:

|参数|类型|说明|
|:---|---|---|
|gps_data|STRING|GPS明码语句|

返回值:

|数据类型|说明|
|:---|---|
|STRING|GSV语句|

示例:

```python
from loction import GPSMatch

gps_match = GPSMatch()

gps_data = """
$GNGLL,3149.333010,N,11706.927563,E,064758.000,A,A*4F
$BDGSV,5,5,17,11,04,276,,1*44
$BDGSV,5,4,17,19,24,059,,05,18,251,,21,16,172,,25,15,312,21,1*7A
$BDGSV,5,3,17,22,39,120,,02,38,230,,04,32,119,,26,25,199,,1*7A
$BDGSV,5,2,17,13,49,228,,12,44,307,27,01,43,135,,24,40,254,,1*71
$BDGSV,5,1,17,07,84,161,,10,78,301,23,08,64,233,,03,53,193,,1*71
$GPGSV,4,4,13,24,03,306,15,1*52
$GPGSV,4,3,13,02,06,249,,04,04,109,,30,04,193,,09,03,140,,1*61
$GPGSV,4,2,13,06,47,264,,194,44,165,,03,43,061,15,01,17,049,18,1*5F
$GPGSV,4,1,13,195,67,060,30,14,63,177,17,17,61,359,19,19,48,325,17,1*5D
$GNGSA,A,3,10,12,25,,,,,,,,,,1.56,1.30,0.86,4*0F
$GNGSA,A,3,14,17,195,19,01,03,,,,,,,1.56,1.30,0.86,1*3B
$GNGGA,064758.000,3149.333010,N,11706.927563,E,1,9,1.30,98.483,M,-0.336,M,,*64
$GNVTG,19.23,T,,M,1.19,N,2.20,K,A*13
$GNRMC,064758.000,A,3149.333010,N,11706.927563,E,1.19,19.23,060522,,,A,V*31
$GPTXT,01,01,02,ANTSTATUS=OPEN*2B
"""
rmc_data = gps_match.GxRMC(gps_data)
print(rmc_data)
# $GNRMC,064758.000,A,3149.333010,N,11706.927563,E,1.19,19.23,060522,,,A,V*31

gga_data = gps_match.GxGGA(gps_data)
print(gga_data)
# $GNGGA,064758.000,3149.333010,N,11706.927563,E,1,9,1.30,98.483,M,-0.336,M,,*64

vtg_data = gps_match.GxVTG(gps_data)
print(vtg_data)
# $GNVTG,19.23,T,,M,1.19,N,2.20,K,A*13

gsv_data = gps_match.GxGSV(gps_data)
print(gsv_data)
# $GPGSV,4,4,13,24,03,306,15,1*52
```

### GPSParse

> GPS 参数解析

#### GxGGA_satellite_num 正在使用解算位置的卫星数量

参数:

|参数|类型|说明|
|:---|---|---|
|gga_data|STRING|GGA明码语句|

返回值:

|数据类型|说明|
|:---|---|
|STRING|卫星数，无返回空字符串|

#### GxGGA_latitude 纬度

参数:

|参数|类型|说明|
|:---|---|---|
|gga_data|STRING|GGA明码语句|

返回值:

|数据类型|说明|
|:---|---|
|STRING|纬度|

#### GxGGA_longtitude 经度

参数:

|参数|类型|说明|
|:---|---|---|
|gga_data|STRING|GGA明码语句|

返回值:

|数据类型|说明|
|:---|---|
|STRING|经度|

#### GxGGA_altitude 海拔高度

参数:

|参数|类型|说明|
|:---|---|---|
|gga_data|STRING|GGA明码语句|

返回值:

|数据类型|说明|
|:---|---|
|STRING|海拔高度|

#### GxVTG_speed 地面速率

参数:

|参数|类型|说明|
|:---|---|---|
|vtg_data|STRING|VTG明码语句|

返回值:

|数据类型|说明|
|:---|---|
|STRING|地面速率, 单位:公里/小时|

#### GxGSV_satellite_num 可见卫星的总数

参数:

|参数|类型|说明|
|:---|---|---|
|gsv_data|STRING|GSV明码语句|

返回值:

|数据类型|说明|
|:---|---|
|STRING|卫星数，无返回空字符串|

示例:

```python
from loction import GPSParse

gps_parse = GPSParse()
gga_data = "$GNGGA,064758.000,3149.333010,N,11706.927563,E,1,9,1.30,98.483,M,-0.336,M,,*64"
vtg_data = "$GNVTG,19.23,T,,M,1.19,N,2.20,K,A*13"
gsv_data = "$GPGSV,4,4,13,24,03,306,15,1*52"

gga_satellite_num = gps_parse.GxGGA_satellite_num(gga_data)
print(gga_satellite_num)
# "9"

gga_latitude = gps_parse.GxGGA_latitude(gga_data)
print(gga_latitude)
# "31.82221683333333"

gga_longtitude = gps_parse.GxGGA_longtitude(gga_data)
print(gga_longtitude)
# "117.1154593833333"

gga_altitude = gps_parse.GxGGA_altitude(gga_data)
print(gga_altitude)
# "98.483"

vtg_speed = gps_parse.GxVTG_speed(vtg_data)
print(vtg_speed)
# "2.20"

gsv_satellite_num = gps_parse.GxGSV_satellite_num(gsv_data)
print(gsv_satellite_num)
# "13"
```

### GPS

> GPS 定位模块，用于开启关闭GPS模块，读取GPS数据

#### 模块导入

示例:

```python
from location import GPS

gps_cfg = {
    "UARTn": UART.UART1,
    "buadrate": 115200,
    "databits": 8,
    "parity": 0,
    "stopbits": 1,
    "flowctl": 0,
    "PowerPin": None,
    "StandbyPin": None,
    "BackupPin": None
}
gps_mode = 2

gps = GPS(gps_cfg, gps_mode)
```

参数:

|参数|类型|说明|
|:---|---|---|
|gps_cfg|DICT|外置GPS读取uart配置信息|
|gps_mode|INT|1 - 内置GPS, 2 - 外置GPS|

#### read 读取GPS数据

示例:

```python
retry = 10
gps_data = gps.read(retry=retry)
print(gps_data)
# $GNGLL,3149.333010,N,11706.927563,E,064758.000,A,A*4F
# $BDGSV,5,5,17,11,04,276,,1*44
# $BDGSV,5,4,17,19,24,059,,05,18,251,,21,16,172,,25,15,312,21,1*7A
# $BDGSV,5,3,17,22,39,120,,02,38,230,,04,32,119,,26,25,199,,1*7A
# $BDGSV,5,2,17,13,49,228,,12,44,307,27,01,43,135,,24,40,254,,1*71
# $BDGSV,5,1,17,07,84,161,,10,78,301,23,08,64,233,,03,53,193,,1*71
# $GPGSV,4,4,13,24,03,306,15,1*52
# $GPGSV,4,3,13,02,06,249,,04,04,109,,30,04,193,,09,03,140,,1*61
# $GPGSV,4,2,13,06,47,264,,194,44,165,,03,43,061,15,01,17,049,18,1*5F
# $GPGSV,4,1,13,195,67,060,30,14,63,177,17,17,61,359,19,19,48,325,17,1*5D
# $GNGSA,A,3,10,12,25,,,,,,,,,,1.56,1.30,0.86,4*0F
# $GNGSA,A,3,14,17,195,19,01,03,,,,,,,1.56,1.30,0.86,1*3B
# $GNGGA,064758.000,3149.333010,N,11706.927563,E,1,9,1.30,98.483,M,-0.336,M,,*64
# $GNVTG,19.23,T,,M,1.19,N,2.20,K,A*13
# $GNRMC,064758.000,A,3149.333010,N,11706.927563,E,1.19,19.23,060522,,,A,V*31
# $GPTXT,01,01,02,ANTSTATUS=OPEN*2B
```

参数:

|参数|类型|说明|
|:---|---|---|
|retry|INT|GPS位置信息读取重试次数, 默认100|

返回值:

|数据类型|说明|
|:---|---|
|STRING|GPS NMEA明码语句|

#### read_coordinates 获取GPS定位信息(经纬度，海拔)

示例:

```python

coordinates = gps.read_coordinates(gps_data)
print(coordinates)
# (117.1154593833333, 31.82221683333333, 98.483)
```

参数:

|参数|类型|说明|
|:---|---|---|
|gps_data|STRING|GPS NMEA明码语句|

返回值:

|数据类型|说明|
|:---|---|
|TUPLE|元素1经度，元素2纬度，元素3海拔|

#### power_switch GPS模块电源开关

示例:

```python

onoff = 1
res = gps.power_switch(onoff)
```

参数:

|参数|类型|说明|
|:---|---|---|
|onoff|INT|0 - 关, 1 - 开|

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|

#### backup BACKUP低功耗模式(支持模块L76K)

示例:

```python

onoff = 1
res = gps.backup(onoff)
```

参数:

|参数|类型|说明|
|:---|---|---|
|onoff|INT|0 - 关, 1 - 开|

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|

#### standby STANDBY低功耗模式(支持模块L76K)

示例:

```python

onoff = 1
res = gps.standby(onoff)
```

参数:

|参数|类型|说明|
|:---|---|---|
|onoff|INT|0 - 关, 1 - 开|

返回值:

|数据类型|说明|
|:---|---|
|BOOL|`True`成功, `False`失败|

### CellLocator

> 基站定位模块，获取基站定位信息与小区信息

#### 模块导入

示例:

```python
from location import CellLocator

cell_cfg = {
    "serverAddr": "www.queclocator.com",
    "port": 80,
    "token": "XXXX",
    "timeout": 3,
    "profileIdx": 1,
}

cell = CellLocator(cell_cfg)
```

参数:

|参数|类型|说明|
|:---|---|---|
|cell_cfg|DICT|基站配置信息|

#### read 读取基站定位信息

示例:

```python

res = cell.read()
print(res)
# (0, (117.1154556274414, 31.82186508178711, 550), {'near_cell': ['232301364'], 'server_cell': ([], [], [(0, 232301364, 1120, 17, 377, 26909, 1850, -72, -6)])})
```

参数:

无

返回值:

|数据类型|说明|
|:---|---|
|TUPLE|元素1成功失败，0-成功，-1失败；元素2定位信息(经度，纬度，精确度(单位米))；元素3小区信息，`near_cell`小区id列表，`server_cell`[三种网络系统（GSM、UMTS、LTE）的信息的列表](https://python.quectel.com/wiki/#/zh-cn/api/QuecPythonClasslib?id=%e8%8e%b7%e5%8f%96%e5%b0%8f%e5%8c%ba%e4%bf%a1%e6%81%af)|

### WiFiLocator

> WIFI定位模块，获取WIFI定位信息与热点MAC地址

#### 模块导入

示例:

```python
from location import WiFiLocator

wifi_cfg = {
    "token": "XXX"
}

wifi = WiFiLocator(wifi_cfg)
```

参数:

|参数|类型|说明|
|:---|---|---|
|wifi_cfg|DICT|WIFI配置信息|

#### read 读取基站定位信息

示例:

```python

res = wifi.read()
print(res)
# (0, (117.1156539916992, 31.82171249389649, 60), ['34:CE:00:09:E5:A8', '60:38:E0:C2:84:D9', '00:03:7F:12:A5:A5', 'EC:B9:70:F1:8F:B5', '24:4B:FE:0B:BE:70'])
```

参数:

无

返回值:

|数据类型|说明|
|:---|---|
|TUPLE|元素1成功失败，0-成功，-1失败；元素2定位信息(经度，纬度，精确度(单位米))；元素3热点mac地址列表|

### Location

> 定位信息读取模块，可直接传入三种定位方式的配置信息，直接一次读取指定定位方式的定位信息

#### 模块导入

示例:

```python
from location import Location

gps_mode = 2
locator_init_params = {
    "cell_cfg": {
        "timeout": 3,
        "profileIdx": 1,
        "port": 80,
        "serverAddr": "www.queclocator.com",
        "token": "XXX"
    },
    "wifi_cfg": {
        "token": "XXX"
    },
    "gps_cfg": {
        "parity": 0,
        "stopbits": 1,
        "flowctl": 0,
        "UARTn": 1,
        "buadrate": 115200,
        "databits": 8
    }
}

locator = Location(gps_mode, locator_init_params)
```

参数:

|参数|类型|说明|
|:---|---|---|
|gps_mode|INT|1 - 内置GPS; 2 - 外置GPS|
|locator_init_params|DICT|定位模块配置信息|

#### read 读取基站定位信息

示例:

```python

loc_method = 7
res = locator.read(loc_method)
print(res)
# {4: ((117.1156692504883, 31.82216453552246, 45), ['34:CE:00:09:E5:A8', '62:E5:A1:83:D6:AF', '00:0A:F5:F7:3C:48', 'EC:B9:70:F1:8F:B5', 'EE:B9:70:D1:8F:B5']), 1: '$GNGLL,3149.333010,N,11706.927563,E,064758.000,A,A*4F\r\n$BDGSV,5,5,17,11,04,276,,1*44\r\n$BDGSV,5,4,17,19,24,059,,05,18,251,,21,16,172,,25,15,312,21,1*7A\r\n$BDGSV,5,3,17,22,39,120,,02,38,230,,04,32,119,,26,25,199,,1*7A\r\n$BDGSV,5,2,17,13,49,228,,12,44,307,27,01,43,135,,24,40,254,,1*71\r\n$BDGSV,5,1,17,07,84,161,,10,78,301,23,08,64,233,,03,53,193,,1*71\r\n$GPGSV,4,4,13,24,03,306,15,1*52\r\n$GPGSV,4,3,13,02,06,249,,04,04,109,,30,04,193,,09,03,140,,1*61\r\n$GPGSV,4,2,13,06,47,264,,194,44,165,,03,43,061,15,01,17,049,18,1*5F\r\n$GPGSV,4,1,13,195,67,060,30,14,63,177,17,17,61,359,19,19,48,325,17,1*5D\r\n$GNGSA,A,3,10,12,25,,,,,,,,,,1.56,1.30,0.86,4*0F\r\n$GNGSA,A,3,14,17,195,19,01,03,,,,,,,1.56,1.30,0.86,1*3B\r\n$GNGGA,064758.000,3149.333010,N,11706.927563,E,1,9,1.30,98.483,M,-0.336,M,,*64\r\n$GNVTG,19.23,T,,M,1.19,N,2.20,K,A*13\r\n$GNRMC,064758.000,A,3149.333010,N,11706.927563,E,1.19,19.23,060522,,,A,V*31\r\n$GPTXT,01,01,02,ANTSTATUS=OPEN*2B', 2: ((117.1154556274414, 31.82186508178711, 550), {'near_cell': ['232301364'], 'server_cell': ([], [], [(0, 232301364, 1120, 17, 377, 26909, 1850, -71, -8)])})}
```

参数:

|参数|类型|说明|
|:---|---|---|
|loc_method|INT|GPS定位方式,以二进制方式组合,设置多个,1 - GPS,2 - 基站, 4 - WIFI|

返回值:

|数据类型|说明|
|:---|---|
|DICT|key为定位方式枚举值, value值为返回的定位信息, 定位信息详情见各个定位模块`read`返回值|

#### wgs84togcj02 经纬度坐标系转换

示例:

```python
wgs84_longtitude = 117.1154593833333
wgs84_latitude = 31.82221683333333

gcj02_longtitude, gcj02_latitude = locator.wgs84togcj02(wgs84_longtitude, wgs84_latitude)
print(gcj02_longtitude, gcj02_latitude)
# 117.121085101472 31.82038457486135
```

参数:

|参数|类型|说明|
|:---|---|---|
|Longtitude|FLOAT|WGS84经度|
|Latitude|FLOAT|WGS84纬度|

返回值:

|数据类型|说明|
|:---|---|
|TUPLE|元素1: GCJ02经度, 元素2: GCJ02纬度|

## logging 日志模块

> 该模块用于代码日志打印

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

## mpower 低功耗定时唤醒模块

### LowEnergyManage

> 提供定时低功耗唤醒功能，当设备不进行业务处理时，可将设备调整为低功耗模式，当设备唤醒时，可通知用户进行业务处理。
> 该模块被设计为被监听者，使用时需给其注册一个监听者，当设备唤醒时，通知监听者进行业务处理。
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

#### 模块导入

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
|INT|唤醒周期，单位s|

#### set_period 获取低功耗唤醒周期

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

> 初始化低功耗模式之前需设置好唤醒周期和低功耗模式，如未设置，则默认周期60s，默认低功耗模式`PM`。

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

## quecthing 移远云物联网模块

> 该模块用于提供移远云物联网模块相关功能，MQTT协议的消息发布与订阅, OTA升级。

### QuecObjectModel

> 该模块是将移远云导出的json格式的模型数据转化成一个物模型类，方便使用

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
```

参数:

|参数|类型|说明|
|:---|---|---|
|om_file|STRING|物模型文件全路径地址，可选，默认`/usr/quec_object_model.json`|

### QuecThing

> 还模块主要提供移远云物联网模块的连接，消息的发送，消息订阅，OTA升级功能。

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

## remote 物联网云兼容模块

> 该模块作用于云服务与设备直接消息交互的中间件

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
> - `event_rrpc_request` RRPC请求消息数据接收

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

## sensor 传感器模块(开发中)
