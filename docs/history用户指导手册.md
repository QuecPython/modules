# 历史文件模块 用户指导手册

## 简介

> 该模块主要用于读取记录与清理历史数据文件, 该模块设计成监听者模式, 可以和`remote`模块结合使用, 当`remote`发送消息失败时, 将消息通知给`history`模块, 存入历史文件中

## 使用说明

### 1. 模块初始化

```python
from history import History

hist = History(history_file="/usr/tracker_data.hist", max_hist_num=100)
```

### 2. 写入历史文件

```python
data = [{"local_time": 1651136994000}, {"local_time": 1651136995000}]
res = hist.write(data)
```

### 3. 读取历史文件

```python
data = hist.read()
print(data)
# {"data": [{"local_time": 1651136994000}, {"local_time": 1651136995000}]}
```

### 4. 清除历史文件

```python
res = hist.clean()
```

### 5. 作为监听者接收需要存储的数据

> 此处将该模块作为`remote`模块的`RemotePublish`的监听者为例

```python
from remote import RemotePublish
rmt_pub = RemotePublish()
RemotePublish.addObserver(hist)

# RemotePublish作为被监听者, 在其方法中调用hist.update方法通知监听者
data = [{"local_time": 1651136994000}, {"local_time": 1651136995000}]
hist.update(observable, *data)
```

## API说明

### History

#### 导入初始化

示例:

```python
from history import History

hist = History(history_file="/usr/tracker_data.hist", max_hist_num=100)
```

参数:

|参数|类型|说明|
|:---|---|---|
|history_file|STRING|全路径历史文件名称, 默认`/usr/tracker_data.hist`|
|max_hist_num|INT|最大存储历史数据条数, 默认100|

#### read 读取历史文件

> 将历史文件中的数据读取出来, 并将历史文件清空, 防止重复读取

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
|DICT|key值为`data`, value值为列表, 列表元素为存入的历史数据|

#### write 写入历史文件

> 将数据写入历史文件中, 当文件中有数据时, 则在文件中追加写入, 并保证总写入的数据不大于设置的最大保存数据条数

示例:

```python
data = [{"local_time": 1651136994000}, {"local_time": 1651136995000}]
res = hist.write(data)
```

参数:

|参数|类型|说明|
|:---|---|---|
|data|LIST|列表数据, 元素根据具体业务具体定义即可|

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
