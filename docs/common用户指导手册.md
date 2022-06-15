# 公共模块 用户指导手册

## 简介

> 该模块封装了一些公用组件与基类, 方便其他模块使用

## 功能接口说明

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
|num|INT|迭代数值范围, 默认99999|

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

> 监听模式中的被监听者基类, 动态注册与移除监听者, 通知监听者信息

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

> 针对云服务中间件封装的监听者基类, 当云端下发指令到设备时, 通过监听者进行消息的分类转发

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

> 云服务被监听者基类, 用于定义封装的不同云服务方法的基本功能, 方便统一不同云的兼容使用, 用户可根据不同的云服务编写`init`, `close`, `post_data`, `ota_request`, `ota_action`方法

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
|module|STRING|升级模块, 非必填|

返回值:

无

### CloudObjectModel 云服务物模型基类

> 将物模型转换成抽象类的方法, 方便项目使用, 用户可根据不同的云服务的物模型重写`init`方法

#### init 物模型json文件解析

参数:

无

返回值:

无
