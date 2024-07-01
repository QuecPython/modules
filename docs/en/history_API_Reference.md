# History File Module API Reference Manual

[中文](../zh/history_API参考手册.md) | English

## Introduction

> This module is mainly used for reading records and clearing historical data files.

## API Description

### History

> The data recorded by this module is mainly in JSON format, which is convenient to use. You can directly store dictionary data into the file and read records in list order.

**Example:**

```python
from history import History

hist = History(history_file="/usr/tracker_data.hist", max_hist_num=100)
```

**Parameters:**

|Parameter|Type|Description|
|:---|---|---|
|history_file|str|Full path of the history file, default: `/usr/tracker_data.hist`|
|max_hist_num|int|Maximum number of historical data entries to store, default: 100|

#### History.read

> Read data from the history file and clear the history file to prevent duplicate reads.

**Example:**

```python
data = hist.read()
print(data)
# {"data": [{"local_time": 1651136994000}]}
```

**Parameters:**

None

**Return Value:**

|Data Type|Description|
|:---|---|
|dict|Key is `data`, value is a list, and the list elements are the stored historical data|

#### History.write

> Write data into the history file. If there is data in the file, it will append the data to the file, ensuring that the total data written does not exceed the maximum number of saved data entries.

**Example:**

```python
data = [{"local_time": 1651136994000}, {"local_time": 1651136995000}]
hist.write(data)
# True
```

**Parameters:**

|Parameter|Type|Description|
|:---|---|---|
|data|list|List data, elements are defined according to specific business needs|

**Return Value:**

|Data Type|Description|
|:---|---|
|bool|`True` - Success<br>`False` - Failure|

#### History.clear

> Clear the historical data file.

**Example:**

```python
hist.clear()
# True
```

**Parameters:**

None

**Return Value:**

|Data Type|Description|
|:---|---|
|bool|`True` - Success<br>`False` - Failure|

#### History Usage Example

```python
from history import History
# Module initialization
hist = History(history_file="/usr/tracker_data.hist", max_hist_num=100)

# Write to the history file
data = [{"local_time": 1651136994000}, {"local_time": 1651136995000}]
res = hist.write(data)

# Read the history file
data = hist.read()
print(data)
# {"data": [{"local_time": 1651136994000}, {"local_time": 1651136995000}]}

# Clear the history file
hist.clean()
# True
```

### CacheFile

> This module mainly records byte data, i.e., it records according to a fixed length of bytes as one entry, writes sequentially into the file, and reads data according to the defined byte length. The main advantage of this recording method is that the recorded data is relatively neat and does not waste storage resources, making it more friendly to use on devices with small storage space.

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

**Parameters:**

|Parameter|Type|Description|
|:---|---|---|
|cache_cfg|dict|Configuration parameters:<br>RINDEX - Read start offset, default: 32<br>WINDEX - Write start offset, default: 32<br>BLOCK_SIZE - Size of block data to write (pad with 0 if insufficient), default: 64<br>BAK_NUM - Number of recorded data blocks, default: 640<br>RET_HEAD - Whether to loop back to the beginning of the file for writing, 1 - Yes, 0 - No, default: 0<br>This parameter is optional, if not filled, it will be configured with default values. Usually, it needs to be reconfigured according to actual conditions. The read and write offsets are 32, i.e., the first 32 bytes of the file are used to record this information, each piece of information occupies 4 bytes, currently occupying a total of 20 bytes, leaving redundancy for expansion.|
|filename|str|Full path and file name of the record file, default: `/usr/cache.bak`|

#### CacheFile.open

> Open the cache file.

**Example:**

```python
cache_file.open()
```

**Parameters:**

None

**Return Value:**

None

#### CacheFile.read

> Read a record of `BLOCK_SIZE` size.

**Example:**

```python
data = cache_file.read(offset=0)
```

**Parameters:**

|Parameter|Type|Description|
|:---|---|---|
|offset|int|Read offset address, default: None<br>If this parameter is provided, it will read a `BLOCK_SIZE` data block from the given offset address.<br>If not provided, default None, it will read a `BLOCK_SIZE` data block from the `RINDEX` offset address, and add a `BLOCK_SIZE` value to the `RINDEX` address, then write it to the file.|

**Return Value:**

|Data Type|Description|
|:---|---|
|bytes|A data block of `BLOCK_SIZE` size|

#### CacheFile.write

> Write a `BLOCK_SIZE` sized data block. If the length of data to be written is less than `BLOCK_SIZE`, it will pad with 0 at the end. If it exceeds `BLOCK_SIZE`, an exception will be thrown.

**Example:**

```python
data = bytes([0xFF] * 64)
cache_file.write(data)
```

**Parameters:**

|Parameter|Type|Description|
|:---|---|---|
|data|bytes/str|A string or byte string with a length not exceeding `BLOCK_SIZE`|

**Return Value:**

|Data Type|Description|
|:---|---|
|bool|`True` - Success<br>`False` - Failure|

#### CacheFile.save

> Store the written data. After `read` or `write`, this interface needs to be called to store the written data into the storage device. Otherwise, the written data will not be truly stored on the physical device, and power loss will result in data loss.

**Example:**

```python
cache_file.save()
```

**Parameters:**

None

**Return Value:**

None

#### CacheFile.clear

> Clear the markers, i.e., reset `WINDEX`, `RINDEX`, and `RET_HEAD` to default values, which are the default values in `CacheFile._CACHE_CFG_`. This allows reading and writing the file from the beginning again, but it will not actually clear the file content.

**Example:**

```python
cache_file.clear()
```

**Parameters:**

None

**Return Value:**

None

#### CacheFile.close

> Close the file.

**Example:**

```python
cache_file.close()
```

**Parameters:**

None

**Return Value:**

None

#### CacheFile.readable

> Whether the current file has readable data, i.e., whether there is data written but not yet read. If `RET_HEAD` is 0 and `RINDEX` is greater than or equal to `WINDEX`, there is no readable data; otherwise, there is readable data.

**Example:**

```python
cache_file.readable()
```

**Parameters:**

None

**Return Value:**

|Data Type|Description|
|:---|---|
|bool|`True` - Has readable data<br>`False` - No readable data|

#### CacheFile Usage Example

```python
from history import CacheFile

# Initialize cache file
cache_cfg = {
    "RINDEX": 32,
    "WINDEX": 32,
    "BLOCK_SIZE": 64,
    "BAK_NUM": 640,
    "RET_HEAD": 0,
}
filename = "/usr/cache.bak"
cache_file = CacheFile(cache_cfg=cache_cfg, filename=filename)

# Open cache file
cache_file.open()

# Write data
data = bytes([0xFF] * 64)
cache_file.write(data)

# Store data
cache_file.save()

# Check if there is readable data
if cache_file.readable():
    # Read data from RINDEX offset
    _data = cache_file.read()

    # Store data, re-record RINDEX offset into the file
    cache_file.save()
else:
    # Read data from default read start offset
    _data = cache_file.read(offset=cache_cfg["RINDEX"])

# Clear data
cache_file.clear()

# Close file
cache_file.close()
```