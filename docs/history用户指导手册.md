# 历史文件模块 用户指导手册

## 简介

> 该模块主要用于读取记录与清理历史数据文件。

## API说明

### 实例化对象

**示例:**

```python
from history import History

hist = History(history_file="/usr/tracker_data.hist", max_hist_num=100)
```

**参数:**

|参数|类型|说明|
|:---|---|---|
|history_file|str|全路径历史文件名称, 默认`/usr/tracker_data.hist`|
|max_hist_num|int|最大存储历史数据条数, 默认100|

### read

> 将历史文件中的数据读取出来, 并将历史文件清空, 防止重复读取

**示例:**

```python
data = hist.read()
print(data)
# {"data": [{"local_time": 1651136994000}]}
```

**参数:**

无

**返回值:**

|数据类型|说明|
|:---|---|
|dict|key值为`data`, value值为列表, 列表元素为存入的历史数据|

### write

> 将数据写入历史文件中, 当文件中有数据时, 则在文件中追加写入, 并保证总写入的数据不大于设置的最大保存数据条数

**示例:**

```python
data = [{"local_time": 1651136994000}, {"local_time": 1651136995000}]
hist.write(data)
# True
```

**参数:**

|参数|类型|说明|
|:---|---|---|
|data|list|列表数据, 元素根据具体业务具体定义即可|

**返回值:**

|数据类型|说明|
|:---|---|
|bool|`True`成功<br>`False`失败|

### clean

> 将历史数据文件清除

**示例:**

```python
hist.clean()
# True
```

**参数:**

无

**返回值:**

|数据类型|说明|
|:---|---|
|bool|`True`成功<br>`False`失败|

## 使用示例

```python
from history import History
# 模块初始化
hist = History(history_file="/usr/tracker_data.hist", max_hist_num=100)

# 写入历史文件
data = [{"local_time": 1651136994000}, {"local_time": 1651136995000}]
res = hist.write(data)

# 读取历史文件
data = hist.read()
print(data)
# {"data": [{"local_time": 1651136994000}, {"local_time": 1651136995000}]}

# 清除历史文件
hist.clean()
# True
```
