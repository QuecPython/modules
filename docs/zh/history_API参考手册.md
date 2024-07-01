# 历史文件模块 API 参考手册

中文 | [English](../en/history_API_Reference.md)

## 简介

> 该模块主要用于读取记录与清理历史数据文件。

## API 说明

### History

> 该模块记录的数据主要为 json 数据，使用较为方便，可以直接将字典数据直接存储进文件，按列表顺序读取记录即可。

**示例：**

```python
from history import History

hist = History(history_file="/usr/tracker_data.hist", max_hist_num=100)
```

**参数：**

|参数|类型|说明|
|:---|---|---|
|history_file|str|全路径历史文件名称，默认：`/usr/tracker_data.hist`|
|max_hist_num|int|最大存储历史数据条数，默认：100|

#### History.read

> 将历史文件中的数据读取出来，并将历史文件清空，防止重复读取。

**示例：**

```python
data = hist.read()
print(data)
# {"data": [{"local_time": 1651136994000}]}
```

**参数：**

无

**返回值：**

|数据类型|说明|
|:---|---|
|dict|key 值为 `data`，value 值为列表，列表元素为存入的历史数据|

#### History.write

> 将数据写入历史文件中，当文件中有数据时，则在文件中追加写入，并保证总写入的数据不大于设置的最大保存数据条数。

**示例：**

```python
data = [{"local_time": 1651136994000}, {"local_time": 1651136995000}]
hist.write(data)
# True
```

**参数：**

|参数|类型|说明|
|:---|---|---|
|data|list|列表数据，元素根据具体业务具体定义即可|

**返回值：**

|数据类型|说明|
|:---|---|
|bool|`True` - 成功<br>`False` - 失败|

#### History.clear

> 将历史数据文件清除。

**示例：**

```python
hist.clear()
# True
```

**参数：**

无

**返回值：**

|数据类型|说明|
|:---|---|
|bool|`True` - 成功<br>`False` - 失败|

#### History 使用示例

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

### CacheFile

> 改模块主要记录的为字节数据，即按固定长度的字节数做为一条记录，顺序写入文件，读取时也按规定好的字节长度进行读取数据，该记录方法主要优点是记录的数据相对整齐，不会浪费存储资源，在存储空间较小的设备上使用较友好。

```python
from history import CacheFile

cache_cfg = {
    "RINDEX": 32,
    "WINDEX": 32,
    "BLOCK_SIZE": 64,
    "BAK_NUM": 640,
    "RET_HEAD": 0,
}
filename = "/usr/cache.bak"
cache_file = CacheFile(cache_cfg=cache_cfg, filename=filename)
```

**参数：**

|参数|类型|说明|
|:---|---|---|
|cache_cfg|dict|配置参数：<br>RINDEX - 读取起始偏移量，默认：32<br>WINDEX - 写入起始偏移量，默认：32<br>BLOCK_SIZE - 写入块数据大小（不足补 0），默认：64<br>BAK_NUM - 记录数据块数量，默认：640<br>RET_HEAD - 是否循环从头开始写入文件，1 - 是，0 - 否，默认：0<br>该参数选填，不填按默认值配置，通常需要根据实际情况进行重新配置，读写偏移量为 32，即文件前 32 位用于记录这些数据信息，每个数据信息占用 4 个字节，目前共占用 20 个字节，留有冗余量进行扩充数据|
|filename|str|记录文件全路径和文件名称，默认：`/usr/cache.bak`|

#### CacheFile.open

> 打开缓存文件。

**示例：**

```python
cache_file.open()
```

**参数：**

无

**返回值：**

无

#### CacheFile.read

> 读取一个 `BLOCK_SIZE` 大小的记录数据。

**示例：**

```python
data = cache_file.read(offset=0)
```

**参数：**

|参数|类型|说明|
|:---|---|---|
|offset|int|读取偏移地址，默认：None<br>当传入该参数时，则从传入的偏移地址开始，读取一个 `BLOCK_SIZE` 大小的数据<br>当不传时，默认 None，则从 `RINDEX` 偏移地址开始，读取一个 `BLOCK_SIZE` 大小的数据，并将 `RINDEX` 地址加一个 `BLOCK_SIZE` 的值，并写入文件|

**返回值：**

|数据类型|说明|
|:---|---|
|bytes|一个 `BLOCK_SIZE` 大小的数据|

#### CacheFile.write

> 写入一个 `BLOCK_SIZE` 大小的数据，当写入的数据长度不足 `BLOCK_SIZE` 时，则会在末尾补 0，当大于 `BLOCK_SIZE` 时，会抛出异常。

**示例：**

```python
data = bytes([0xFF] * 64)
cache_file.write(data)
```

**参数：**

|参数|类型|说明|
|:---|---|---|
|data|bytes/str|一个长度不超过 `BLOCK_SIZE` 的字符串或字节串|

**返回值：**

|数据类型|说明|
|:---|---|
|bool|`True` - 成功<br>`False` - 失败|

#### CacheFile.save

> 存储写入的数据。在 `read` 或者 `write` 之后，需要调用一下该接口，将写入的数据存入存储设备，否则写入的数据不会真正存储在物理设备上，断电会导致数据丢失。

**示例：**

```python
cache_file.save()
```

**参数：**

无

**返回值：**

无

#### CacheFile.clear

> 清除标记，即将 `WINDEX`，`RINDEX`，`RET_HEAD` 全部重置为默认值，即 `CacheFile._CACHE_CFG_` 中的默认值。这样即可从头开始读写文件，但并不会将实际的文件内容清空。

**示例：**

```python
cache_file.clear()
```

**参数：**

无

**返回值：**

无

#### CacheFile.close

> 关闭文件。

**示例：**

```python
cache_file.close()
```

**参数：**

无

**返回值：**

无

#### CacheFile.readable

> 当前文件是否有可读取的数据，即是否有写入后还未被读取出来的数据。即当 `RET_HEAD` 为 0 时，且 `RINDEX` 大于等于 `WINDEX` 时，则无可读取的数据，反之则有可读取的数据。

**示例：**

```python
cache_file.readable()
```

**参数：**

无

**返回值：**

|数据类型|说明|
|:---|---|
|bool|`True` - 有可读数据<br>`False` - 无可读数据|

#### CacheFile 使用示例

```python
from history import CacheFile

# 初始化缓存文件
cache_cfg = {
    "RINDEX": 32,
    "WINDEX": 32,
    "BLOCK_SIZE": 64,
    "BAK_NUM": 640,
    "RET_HEAD": 0,
}
filename = "/usr/cache.bak"
cache_file = CacheFile(cache_cfg=cache_cfg, filename=filename)

# 打开缓存文件
cache_file.open()

# 写入数据
data = bytes([0xFF] * 64)
cache_file.write(data)

# 存储数据
cache_file.save()

# 判读是否有可读取的数据
if cache_file.readable():
    # 从 RINDEX 偏移量开始读取数据
    _data = cache_file.read()

    # 存储数据，将 RINDEX 偏移量重新记录进入文件
    cache_file.save()
else:
    # 从默认读取起始偏移量开始读取数据
    _data = cache_file.read(offset=cache_cfg["RINDEX"])

# 清除数据
cache_file.clear()

# 关闭文件
cache_file.close()
```
