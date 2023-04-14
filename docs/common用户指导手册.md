# 公共模块 用户指导手册

## 简介

> 该模块封装了一些公用组件与基类, 方便其他模块使用

## 功能接口说明

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
