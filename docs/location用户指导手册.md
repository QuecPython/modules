# 定位模块 用户指导手册

## 简介

> 本模块使用的定位坐标系为WGS-84, 如需转换GCJ-02坐标系, 本模块提供了`WGS84ToGCJ02`方法进行经纬度坐标系的转换

## API说明

### CoordinateSystemConvert

> 坐标系转换模块, 可以降WGS84坐标系经纬度转换成GCJ02坐标系

#### 实例化对象

**示例:**

```python
from location import CoordinateSystemConvert

csc = CoordinateSystemConvert()
```

#### wgs84_to_gcj02

> WGS84坐标系转换成GCJ02坐标系

**示例:**

```python
wgs84_longitude = 117.1154593833333
wgs84_latitude = 31.82221683333333
gcj02_longitude, gcj02_latitude = csc.wgs84_to_gcj02(wgs84_longitude, wgs84_latitude)
print(gcj02_longitude, gcj02_latitude)
# 117.121085101472 31.82038457486135
```

**参数:**

|参数|类型|说明|
|:---|---|---|
|Longitude|float|WGS84经度|
|Latitude|float|WGS84纬度|

**返回值:**

|数据类型|说明|
|:---|---|
|tuple|元素1: GCJ02经度, 元素2: GCJ02纬度|

### NMEAParse

> NMEA明码语句解析

#### 实例化对象

**示例:**

```python
from location import NMEAParse

nmea_parse = NMEAParse()
```

#### set_gps_data

> 设置需要解析的NMEA明码语句

**示例:**

```python
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
nmea_parse.set_gps_data(gps_data)
```

**参数:**

|参数|类型|说明|
|:---|---|---|
|data|str|NMEA明码语句|

**返回值:**

无

#### GxRMC

> Recommended Minimum Specific GPS/TRANSIT Data（RMC）推荐定位信息

**数据格式:**

> $GPRMC,<1>,<2>,<3>,<4>,<5>,<6>,<7>,<8>,<9>,<10>,<11>,<12>\*hh<CR><LF>

| RMC |
|---|
| <1> UTC时间, hhmmss（时分秒）格式 |
| <2> 纬度ddmm.mmmm（度分）格式（前面的0也将被传输） |
| <3> 纬度半球N（北半球）或S（南半球） |
| <4> 经度dddmm.mmmm（度分）格式（前面的0也将被传输） |
| <5> 经度半球E（东经）或W（西经） |
| <6> GPS状态：0=未定位, 1=非差分定位, 2=差分定位, 6=正在估算 |
| <7> 正在使用解算位置的卫星数量（00~12）（前面的0也将被传输） |
| <8> HDOP水平精度因子（0.5~99.9） |
| <9> 海拔高度（-9999.9~99999.9） |
| <10> 地球椭球面相对大地水准面的高度 |
| <11> 差分时间（从最近一次接收到差分信号开始的秒数, 如果不是差分定位将为空） |
| <12> 差分站ID号0000~1023（前面的0也将被传输, 如果不是差分定位将为空） |

**示例:**

```python
nmea_parse.GxRMC
# $GNRMC,064758.000,A,3149.333010,N,11706.927563,E,1.19,19.23,060522,,,A,V*31
```

**返回值:**

|数据类型|说明|
|:---|---|
|str|RMC语句|

#### GxGGA

> Recommended Minimum Specific GPS/TRANSIT Data（RMC）推荐定位信息

**数据格式:**

> $GPGGA,<1>,<2>,<3>,<4>,<5>,<6>,<7>,<8>,<9>,M,<10>,M,<11>,<12>\*hh<CR><LF>

| GGA |
|---|
| <1> UTC时间, hhmmss（时分秒）格式 |
| <2> 纬度ddmm.mmmm（度分）格式（前面的0也将被传输） |
| <3> 纬度半球N（北半球）或S（南半球） |
| <4> 经度dddmm.mmmm（度分）格式（前面的0也将被传输） |
| <5> 经度半球E（东经）或W（西经） |
| <6> GPS状态：0=未定位, 1=非差分定位, 2=差分定位, 6=正在估算 |
| <7> 正在使用解算位置的卫星数量（00~12）（前面的0也将被传输） |
| <8> HDOP水平精度因子（0.5~99.9） |
| <9> 海拔高度（-9999.9~99999.9） |
| <10> 地球椭球面相对大地水准面的高度 |
| <11> 差分时间（从最近一次接收到差分信号开始的秒数, 如果不是差分定位将为空） |
| <12> 差分站ID号0000~1023（前面的0也将被传输, 如果不是差分定位将为空） |

**示例:**

```python
nmea_parse.GxGGA
# $GNGGA,064758.000,3149.333010,N,11706.927563,E,1,9,1.30,98.483,M,-0.336,M,,*64
```

**返回值:**

|数据类型|说明|
|:---|---|
|str|GGA语句|

#### GxVTG

> Recommended Minimum Specific GPS/TRANSIT Data（RMC）推荐定位信息

**数据格式:**

> $GPVTG,<1>,T,<2>,M,<3>,N,<4>,K,<5>\*hh<CR><LF>

| VTG |
|---|
| <1> GSV语句的总数 |
| <2> 本句GSV的编号 |
| <3> 可见卫星的总数（00~12, 前面的0也将被传输） |
| <4> PRN码（伪随机噪声码）（01~32, 前面的0也将被传输） |
| <5> 卫星仰角（00~90度, 前面的0也将被传输） |
| <6> 卫星方位角（000~359度, 前面的0也将被传输） |
| <7> 信噪比（00~99dB, 没有跟踪到卫星时为空, 前面的0也将被传输） |

**示例:**

```python
nmea_parse.GxVTG
# $GNVTG,19.23,T,,M,1.19,N,2.20,K,A*13H
```

**返回值:**

|数据类型|说明|
|:---|---|
|str|VTG语句|

#### GxGSV

> GPS Satellites in View（GSV）可见卫星信息

**数据格式:**

> $GPGSV,<1>,<2>,<3>,<4>,<5>,<6>,<7>,…<4>,<5>,<6>,<7>\*hh<CR><LF>

| GSV |
|---|
| <1> GSV语句的总数 |
| <2> 本句GSV的编号 |
| <3> 可见卫星的总数（00~12, 前面的0也将被传输） |
| <4> PRN码（伪随机噪声码）（01~32, 前面的0也将被传输） |
| <5> 卫星仰角（00~90度, 前面的0也将被传输） |
| <6> 卫星方位角（000~359度, 前面的0也将被传输） |
| <7> 信噪比（00~99dB, 没有跟踪到卫星时为空, 前面的0也将被传输） |

**示例:**

```python
nmea_parse.GxGSV
# $GPGSV,4,1,13,195,67,060,30,14,63,177,17,17,61,359,19,19,48,325,17,1*5D
```

**返回值:**

|数据类型|说明|
|:---|---|
|str|GSV语句|

#### GxGLL

> Geographic Position（GLL）定位地理信息

**数据格式:**

> $GPGLL,<1>,<2>,<3>,<4>,<5>,<6>,<7>\*hh<CR><LF>

| GLL |
|---|
| <1> 纬度ddmm.mmmm（度分）格式（前面的0也将被传输）|
| <2> 纬度半球N（北半球）或S（南半球）|
| <3> 经度dddmm.mmmm（度分）格式（前面的0也将被传输）|
| <4> 经度半球E（东经）或W（西经）|
| <5> UTC时间, hhmmss（时分秒）格式|
| <6> 定位状态, A=有效定位, V=无效定位|
| <7> 模式指示（仅NMEA0183 3.00版本输出, A=自主定位, D=差分, E=估算, N=数据无效）|

**示例:**

```python
nmea_parse.GxGLL
# $GNGLL,3149.333010,N,11706.927563,E,064758.000,A,A*4F
```

**返回值:**

|数据类型|说明|
|:---|---|
|str|GLL语句|

#### GxGSA

> GPS DOP and Active Satellites（GSA）当前卫星信息

**数据格式:**

> $GPGSA,<1>,<2>,<3>,<4>,<5>,<6>,<7>\*hh<CR><LF>

| GSA |
|---|
| <1> 模式, M=手动, A=自动 |
| <2> 定位类型, 1=没有定位, 2=2D定位, 3=3D定位 |
| <3> PRN码（伪随机噪声码）, 正在用于解算位置的卫星号（01~32, 前面的0也将被传输）。 |
| <4> PDOP位置精度因子（0.5~99.9） |
| <5> HDOP水平精度因子（0.5~99.9） |
| <6> VDOP垂直精度因子（0.5~99.9 |

**示例:**

```python
nmea_parse.GxGSA
# $GNGSA,A,3,10,12,25,,,,,,,,,,1.56,1.30,0.86,4*0F
```

**返回值:**

|数据类型|说明|
|:---|---|
|str|GSA语句|

#### GxRMCData

> RMC语句按逗号分割返回元组

```python
nmea_parse.GxRMCData
# ("GNRMC", "064758.000", "A", "3149.333010", "N", "11706.927563", "E", "1.19", "19.23", "060522", "", "", "A", "V")
```

**返回值:**

|数据类型|说明|
|:---|---|
|tuple|见RMC数据格式|

#### GxGGAData

> GGA语句按逗号分割返回元组

```python
nmea_parse.GxGGAData
# ("GNGGA", "064758.000", "3149.333010", "N", "11706.927563", "E", "1", "9", "1.30", "98.483", "M", "-0.336", "M", "", "")
```

**返回值:**

|数据类型|说明|
|:---|---|
|tuple|见GGA数据格式|

#### GxGSVData

> GSV语句按逗号分割返回元组

```python
nmea_parse.GxGSVData
# ("GPGSV", "4", "1", "13", "195", "67", "060", "30", "14", "63", "177", "17", "17", "61", "359", "19", "19", "48", "325", "17", "1")
```

**返回值:**

|数据类型|说明|
|:---|---|
|tuple|见GSV数据格式|

#### GxGSAData

> GSA语句按逗号分割返回元组

```python
nmea_parse.GxGSAData
# ("GNGSA", "A", "3", "14", "17", "195", "19", "01", "03", "", "", "", "", "", "", "1.56", "1.30", "0.86", "1")
```

**返回值:**

|数据类型|说明|
|:---|---|
|tuple|见GSA数据格式|

#### GxVTGData

> VTG语句按逗号分割返回元组

```python
nmea_parse.GxVTGData
# ("GNVTG", "19.23", "T", "", "M", "1.19", "N", "2.20", "K", "A")
```

**返回值:**

|数据类型|说明|
|:---|---|
|tuple|见VTG数据格式|

#### GxGLLData

> GLL语句按逗号分割返回元组

```python
nmea_parse.GxGLLData
# ("GNGLL", "3149.333010", "N", "11706.927563", "E", "064758.000", "A", "A")
```

**返回值:**

|数据类型|说明|
|:---|---|
|tuple|见GLL数据格式|

#### Latitude

> GGA中的维度

```python
nmea_parse.Latitude
# "31.82221683333333"
```

**返回值:**

|数据类型|说明|
|:---|---|
|str|纬度|

#### Altitude

> GGA中的海拔

```python
nmea_parse.Altitude
# "98.483"
```

**返回值:**

|数据类型|说明|
|:---|---|
|str|海拔|

#### Speed

> VTG中的速度

```python
nmea_parse.Speed
# "2.20"
```

**返回值:**

|数据类型|说明|
|:---|---|
|str|速度|

### GNSS

> 读取GNSS模块(内置/外置)有效NMEA明码语句.

#### 实例化对象

**示例:**

```python
from machine import UART
from location import GNSS

gps_cfg = {
    "UARTn": UART.UART1,
    "buadrate": 115200,
    "databits": 8,
    "parity": 0,
    "stopbits": 1,
    "flowctl": 0,
    "gps_mode": 2,
    "nmea": 0b010111,
    "PowerPin": None,
    "StandbyPin": None,
    "BackupPin": None,
}
gnss = GNSS(**gps_cfg)
```

**参数:**

|参数|类型|说明|
|:---|---|---|
|UARTn|int|UART串口号|
|buadrate|int|波特率, 常用波特率都支持, 如4800、9600、19200、38400、57600、115200、230400等|
|databits|int|数据位（5 ~ 8）, 展锐平台当前仅支持8位|
|parity|int|奇偶校验（0 – NONE, 1 – EVEN, 2 - ODD）|
|stopbits|int|停止位（1 ~ 2）|
|flowctl|int|硬件控制流（0 – FC_NONE,  1 – FC_HW）|
|gps_mode|int|1 - 内置GPS, 2 - 外置GPS|
|nmea|int|按位标识需要匹配的NMEA项<br>0b000001 - RMC<br>0b000010 - GGA<br>0b000100 - GSV<br>0b001000 - GSA<br>0b010000 - VTG<br>0b100000 - GLL|
|PowerPin|int|Power Pin对象|
|StandbyPin|int|Standby模式Pin对象|
|BackupPin|int|Backup模式Pin对象|

#### read

> 读取GPS数据

**示例:**

```python
retry = 10
gps_data = gnss.read(retry=retry)
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

**参数:**

|参数|类型|说明|
|:---|---|---|
|retry|int|GPS位置信息读取重试次数, 默认100|

**返回值:**

|数据类型|说明|
|:---|---|
|str|GPS NMEA明码语句|

### CellLocator

> 基站定位.

#### 实例化对象

**示例:**

```python
from loction import CellLocator
cell_cfg = {
    "serverAddr": "www.queclocator.com",
    "port": 80,
    "token": "xxxxxxxxxx",
    "timeout": 3,
    "profileIdx": profile_idx,
}
cell = CellLocator(**cell_cfg)
```

**参数:**

|参数|类型|说明|
|:---|---|---|
|serverAddr|str|服务器域名, 长度必须小于255 bytes, 目前仅支持 `www.queclocator.com`|
|port|int|服务器端口, 目前仅支持 80 端口|
|token|str|密钥, 16位字符组成, 需要申请|
|timeout|int|设置超时时间, 范围1-300s, 默认300s|
|profileIdx|int|PDP索引, ASR平台范围1-8, 展锐平台范围1-7|

#### read

> 读取基站定位信息

**示例:**

```python
cell.read()
# (117.1154556274414, 31.82186508178711, 550)
```

**参数:**

无

**返回值:**

|数据类型|说明|
|:---|---|
|TUPLE|定位信息(经度, 纬度, 精确度(单位米)), 失败返回空元组|

### WiFiLocator

> WIFI定位.

#### 实例化对象

**示例:**

```python
from loction import WiFiLocator
wifi_cfg = {
    "token": "xxxxxxxxxx",
}
wifi = WiFiLocator(**wifi_cfg)
```

**参数:**

|参数|类型|说明|
|:---|---|---|
|token|str|密钥, 16位字符组成, 需要申请|

#### read

> 读取基站定位信息

**示例:**

```python
wifi.read()
# (117.1154556274414, 31.82186508178711, 550)
```

**参数:**

无

**返回值:**

|数据类型|说明|
|:---|---|
|TUPLE|定位信息(经度, 纬度, 精确度(单位米)), 失败返回空元组|

## 使用说明

```python
from location import CoordinateSystemConvert, NMEAParse, GNSS, CellLocator, WiFiLocator

# 坐标转换模块初始化
csc = CoordinateSystemConvert()

# NMEA解析模块初始化
nmea_parse = NMEAParse()

# GNSS 模块初始化
gps_cfg = {
    "UARTn": UART.UART1,
    "buadrate": 115200,
    "databits": 8,
    "parity": 0,
    "stopbits": 1,
    "flowctl": 0,
    "gps_mode": 2,
    "nmea": 0b010111,
    "PowerPin": None,
    "StandbyPin": None,
    "BackupPin": None,
}
gnss = GNSS(**gps_cfg)

# 读取GNSS元素数据
retry = 300
gps_data = gnss.read(retry=retry)

# 解析GNSS原始数据
nmea_parse.set_gps_data(gps_data)

# 获取坐标信息
lng = nmea_parse.Longitude
lat = nmea_parse.Latitude
altitude = nmea_parse.Altitude
speed = nmea_parse.Speed

# 转换坐标系
gcj02_lng, gcj02_lat = csc.wgs84_to_gcj02(float(lng), float(lat))

# 基站定位模块初始化
cell_cfg = {
    "serverAddr": "www.queclocator.com",
    "port": 80,
    "token": "xxxxxxxxxx",
    "timeout": 3,
    "profileIdx": profile_idx,
}
cell = CellLocator(**cell_cfg)

# 读取基站定位信息
cell.read()
# (117.1154556274414, 31.82186508178711, 550)

# WIFI定位模块初始化
wifi_cfg = {
    "token": "xxxxxxxxxx",
}
wifi = WiFiLocator(**wifi_cfg)

# 读取WIFI定位信息
wifi.read()
# (117.1154556274414, 31.82186508178711, 550)
```
