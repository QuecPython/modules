# 定位模块 API 参考手册

中文 | [English](../en/location_API_Reference.md)

## 简介

> 本模块提供了 GNSS 定位，基站定位，Wifi 定位三种定位模式的功能封装，提供了 WGS-84 转 GCJ-02 坐标系的转换方法。

## API 说明

### CoordinateSystemConvert

> 坐标系转换模块，可以将 WGS84 坐标系经纬度转换成 GCJ02 坐标系。

**示例：**

```python
from location import CoordinateSystemConvert

csc = CoordinateSystemConvert()
```

#### CoordinateSystemConvert.wgs84_to_gcj02

> WGS84 坐标系转换成 GCJ02 坐标系。

**示例：**

```python
wgs84_longitude = 117.1154593833333
wgs84_latitude = 31.82221683333333
gcj02_longitude, gcj02_latitude = csc.wgs84_to_gcj02(wgs84_longitude, wgs84_latitude)
print(gcj02_longitude, gcj02_latitude)
# 117.121085101472 31.82038457486135
```

**参数：**

|参数|类型|说明|
|:---|---|---|
|Longitude|float|WGS84 经度|
|Latitude|float|WGS84 纬度|

**返回值：**

|数据类型|说明|
|:---|---|
|tuple|元素 1：GCJ02 经度，元素 2：GCJ02 纬度|

### NMEAParse

> NMEA 明码语句解析。

**示例：**

```python
from location import NMEAParse

nmea_parse = NMEAParse()
```

#### NMEAParse.set_gps_data

> 设置需要解析的 NMEA 明码语句

**示例：**

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

**参数：**

|参数|类型|说明|
|:---|---|---|
|data|str/bytes|NMEA 明码语句|

**返回值：**

无

#### NMEAParse.GxRMC

> Recommended Minimum Specific GPS/TRANSIT Data（RMC）推荐定位信息。

**数据格式：**

> $GPRMC,<1>,<2>,<3>,<4>,<5>,<6>,<7>,<8>,<9>,<10>,<11>,<12>\*hh<CR><LF>

| RMC |
|---|
| <1> UTC 时间，hhmmss（时分秒）格式 |
| <2> 纬度 ddmm.mmmm（度分）格式（前面的 0 也将被传输） |
| <3> 纬度半球 N（北半球）或 S（南半球） |
| <4> 经度 dddmm.mmmm（度分）格式（前面的 0 也将被传输） |
| <5> 经度半球 E（东经）或 W（西经） |
| <6> GPS 状态：0=未定位，1=非差分定位，2=差分定位，6=正在估算 |
| <7> 正在使用解算位置的卫星数量（00 ~ 12）（前面的 0 也将被传输） |
| <8> HDOP 水平精度因子（0.5 ~ 99.9） |
| <9> 海拔高度（-9999.9 ~ 99999.9） |
| <10> 地球椭球面相对大地水准面的高度 |
| <11> 差分时间（从最近一次接收到差分信号开始的秒数，如果不是差分定位将为空） |
| <12> 差分站 ID 号 0000 ~ 1023（前面的 0 也将被传输，如果不是差分定位将为空） |

**示例：**

```python
nmea_parse.GxRMC
# $GNRMC,064758.000,A,3149.333010,N,11706.927563,E,1.19,19.23,060522,,,A,V*31
```

**返回值：**

|数据类型|说明|
|:---|---|
|str|RMC 语句|

#### NMEAParse.GxGGA

> Recommended Minimum Specific GPS/TRANSIT Data（RMC）推荐定位信息。

**数据格式：**

> $GPGGA,<1>,<2>,<3>,<4>,<5>,<6>,<7>,<8>,<9>,M,<10>,M,<11>,<12>\*hh<CR><LF>

| GGA |
|---|
| <1> UTC 时间，hhmmss（时分秒）格式 |
| <2> 纬度 ddmm.mmmm（度分）格式（前面的 0 也将被传输） |
| <3> 纬度半球 N（北半球）或 S（南半球） |
| <4> 经度 dddmm.mmmm（度分）格式（前面的 0 也将被传输） |
| <5> 经度半球 E（东经）或 W（西经） |
| <6> GPS状态：0=未定位，1=非差分定位，2=差分定位，6=正在估算 |
| <7> 正在使用解算位置的卫星数量（00 ~ 12）（前面的 0 也将被传输） |
| <8> HDOP 水平精度因子（0.5 ~ 99.9） |
| <9> 海拔高度（-9999.9 ~ 99999.9） |
| <10> 地球椭球面相对大地水准面的高度 |
| <11> 差分时间（从最近一次接收到差分信号开始的秒数，如果不是差分定位将为空） |
| <12> 差分站 ID 号 0000 ~ 1023（前面的 0 也将被传输，如果不是差分定位将为空） |

**示例：**

```python
nmea_parse.GxGGA
# $GNGGA,064758.000,3149.333010,N,11706.927563,E,1,9,1.30,98.483,M,-0.336,M,,*64
```

**返回值：**

|数据类型|说明|
|:---|---|
|str|GGA 语句|

#### NMEAParse.GxVTG

> Recommended Minimum Specific GPS/TRANSIT Data（RMC）推荐定位信息。

**数据格式：**

> $GPVTG,<1>,T,<2>,M,<3>,N,<4>,K,<5>\*hh<CR><LF>

| VTG |
|---|
| <1> GSV 语句的总数 |
| <2> 本句 GSV 的编号 |
| <3> 可见卫星的总数（00 ~ 12, 前面的 0 也将被传输） |
| <4> PRN 码（伪随机噪声码）（01 ~ 32, 前面的 0 也将被传输） |
| <5> 卫星仰角（00 ~ 90 度, 前面的 0 也将被传输） |
| <6> 卫星方位角（000 ~ 359 度, 前面的 0 也将被传输） |
| <7> 信噪比（00 ~ 99dB, 没有跟踪到卫星时为空, 前面的 0 也将被传输） |

**示例：**

```python
nmea_parse.GxVTG
# $GNVTG,19.23,T,,M,1.19,N,2.20,K,A*13H
```

**返回值：**

|数据类型|说明|
|:---|---|
|str|VTG 语句|

#### NMEAParse.GxGSV

> GPS Satellites in View（GSV）可见卫星信息。

**数据格式：**

> $GPGSV,<1>,<2>,<3>,<4>,<5>,<6>,<7>,…<4>,<5>,<6>,<7>\*hh<CR><LF>

| GSV |
|---|
| <1> GSV 语句的总数 |
| <2> 本句 GSV 的编号 |
| <3> 可见卫星的总数（00 ~ 12, 前面的 0 也将被传输） |
| <4> PRN 码（伪随机噪声码）（01 ~ 32, 前面的 0 也将被传输） |
| <5> 卫星仰角（00 ~ 90 度, 前面的 0 也将被传输） |
| <6> 卫星方位角（000 ~ 359 度, 前面的 0 也将被传输） |
| <7> 信噪比（00 ~ 99dB, 没有跟踪到卫星时为空, 前面的 0 也将被传输） |

**示例：**

```python
nmea_parse.GxGSV
# $GPGSV,4,1,13,195,67,060,30,14,63,177,17,17,61,359,19,19,48,325,17,1*5D
```

**返回值：**

|数据类型|说明|
|:---|---|
|str|GSV 语句|

#### NMEAParse.GxGLL

> Geographic Position（GLL）定位地理信息。

**数据格式：**

> $GPGLL,<1>,<2>,<3>,<4>,<5>,<6>,<7>\*hh<CR><LF>

| GLL |
|---|
| <1> 纬度 ddmm.mmmm（度分）格式（前面的 0 也将被传输）|
| <2> 纬度半球 N（北半球）或 S（南半球）|
| <3> 经度 dddmm.mmmm（度分）格式（前面的 0 也将被传输）|
| <4> 经度半球 E（东经）或 W（西经）|
| <5> UTC 时间，hhmmss（时分秒）格式|
| <6> 定位状态，A=有效定位，V=无效定位|
| <7> 模式指示（仅 NMEA0183 3.00 版本输出，A=自主定位，D=差分，E=估算，N=数据无效）|

**示例：**

```python
nmea_parse.GxGLL
# $GNGLL,3149.333010,N,11706.927563,E,064758.000,A,A*4F
```

**返回值：**

|数据类型|说明|
|:---|---|
|str|GLL 语句|

#### NMEAParse.GxGSA

> GPS DOP and Active Satellites（GSA）当前卫星信息。

**数据格式：**

> $GPGSA,<1>,<2>,<3>,<4>,<5>,<6>,<7>\*hh<CR><LF>

| GSA |
|---|
| <1> 模式，M=手动，A=自动 |
| <2> 定位类型，1=没有定位，2=2D 定位，3=3D 定位 |
| <3> PRN 码（伪随机噪声码），正在用于解算位置的卫星号（01 ~ 32，前面的 0 也将被传输）。 |
| <4> PDOP 位置精度因子（0.5 ~ 99.9） |
| <5> HDOP 水平精度因子（0.5 ~ 99.9） |
| <6> VDOP 垂直精度因子（0.5 ~ 99.9 |

**示例：**

```python
nmea_parse.GxGSA
# $GNGSA,A,3,10,12,25,,,,,,,,,,1.56,1.30,0.86,4*0F
```

**返回值：**

|数据类型|说明|
|:---|---|
|str|GSA 语句|

#### NMEAParse.GxRMCData

> RMC 语句按逗号分割返回元组。

```python
nmea_parse.GxRMCData
# ("GNRMC", "064758.000", "A", "3149.333010", "N", "11706.927563", "E", "1.19", "19.23", "060522", "", "", "A", "V")
```

**返回值：**

|数据类型|说明|
|:---|---|
|tuple|见 RMC 数据格式|

#### NMEAParse.GxGGAData

> GGA 语句按逗号分割返回元组。

```python
nmea_parse.GxGGAData
# ("GNGGA", "064758.000", "3149.333010", "N", "11706.927563", "E", "1", "9", "1.30", "98.483", "M", "-0.336", "M", "", "")
```

**返回值：**

|数据类型|说明|
|:---|---|
|tuple|见 GGA 数据格式|

#### NMEAParse.GxGSVData

> GSV 语句按逗号分割返回元组。

```python
nmea_parse.GxGSVData
# ("GPGSV", "4", "1", "13", "195", "67", "060", "30", "14", "63", "177", "17", "17", "61", "359", "19", "19", "48", "325", "17", "1")
```

**返回值：**

|数据类型|说明|
|:---|---|
|tuple|见 GSV 数据格式|

#### NMEAParse.GxGSAData

> GSA 语句按逗号分割返回元组。

```python
nmea_parse.GxGSAData
# ("GNGSA", "A", "3", "14", "17", "195", "19", "01", "03", "", "", "", "", "", "", "1.56", "1.30", "0.86", "1")
```

**返回值：**

|数据类型|说明|
|:---|---|
|tuple|见 GSA 数据格式|

#### NMEAParse.GxVTGData

> VTG 语句按逗号分割返回元组。

```python
nmea_parse.GxVTGData
# ("GNVTG", "19.23", "T", "", "M", "1.19", "N", "2.20", "K", "A")
```

**返回值：**

|数据类型|说明|
|:---|---|
|tuple|见 VTG 数据格式|

#### NMEAParse.GxGLLData

> GLL 语句按逗号分割返回元组。

```python
nmea_parse.GxGLLData
# ("GNGLL", "3149.333010", "N", "11706.927563", "E", "064758.000", "A", "A")
```

**返回值：**

|数据类型|说明|
|:---|---|
|tuple|见 GLL 数据格式|

#### NMEAParse.Latitude

> GGA 中的纬度。

```python
nmea_parse.Latitude
# "31.82221683333333"
```

**返回值：**

|数据类型|说明|
|:---|---|
|str|纬度|

#### NMEAParse.Longitude

> GGA 中的经度。

```python
nmea_parse.Longitude
# "114.12411166633333"
```

**Return Value:**

|Data Type|Description|
|:---|---|
|str|经度|

#### NMEAParse.Altitude

> GGA 中的海拔。

```python
nmea_parse.Altitude
# "98.483"
```

**返回值：**

|数据类型|说明|
|:---|---|
|str|海拔|

#### NMEAParse.Speed

> VTG 中的速度。

```python
nmea_parse.Speed
# "2.20"
```

**返回值：**

|数据类型|说明|
|:---|---|
|str|速度|

### GNSS

> 读取 GNSS 模块有效 NMEA 明码语句, 支持模组内置 GNSS 模块, 外挂 GNSS 模块, 外挂 GNSS 模块支持串口或 I2C 接口读取 NMEA 数据。

**示例：**

```python
from machine import UART, I2C
from location import GNSS

# 实例化模组内置 GNSS 模块
gps_cfg = {
    "gps_mode": GNSS.GPS_MODE.internal,
}
gnss = GNSS(**gps_cfg)

# 实例化外挂 GNS S模块，使用串口进行 NMEA 数据读取
gps_cfg = {
    "gps_mode": GNSS.GPS_MODE.external_uart,
    "UARTn": UART.UART1,
    "buadrate": 115200,
    "databits": 8,
    "parity": 0,
    "stopbits": 1,
    "flowctl": 0,
    "PowerPin": None,
    "StandbyPin": None,
    "BackupPin": None,
}
gnss = GNSS(**gps_cfg)

# 实例化外挂 GNSS 模块，使用 I2C 进行 NMEA 数据读取
gps_cfg = {
    "gps_mode": GNSS.GPS_MODE.external_i2c,
    "I2Cn": I2C.I2C1,
    "i2cmode": I2C.STANDARD_MODE,
    "slaveaddress": 0x55,
    "addr": bytearray([0x00]),
    "addr_len": 1,
    "PowerPin": None,
    "StandbyPin": None,
    "BackupPin": None,
}
gnss = GNSS(**gps_cfg)
```

**参数：**

|参数|类型|说明|
|:---|---|---|
|gps_mode|int|1 - 内置 GPS，2 - 外置 GPS UART 通信，3 - 外置 GPS I2C 通信|
|UARTn|int|UART 串口号|
|buadrate|int|波特率，常用波特率都支持，如 4800、9600、19200、38400、57600、115200、230400 等|
|databits|int|数据位（5 ~ 8），展锐平台当前仅支持 8 位|
|parity|int|奇偶校验（0 – NONE，1 – EVEN，2 - ODD）|
|stopbits|int|停止位（1 ~ 2）|
|flowctl|int|硬件控制流（0 – FC_NONE，1 – FC_HW）|
|I2Cn|int|I2C 通路索引号|
|i2cmode|int|I2C 的工作模式|
|slaveaddress|int| I2C 设备地址，int 类型，传入七位设备地址即可，低位自动补 1|
|addr|int| I2C I2C 寄存器地址，bytearray 类型。|
|addr_len|int| 寄存器地址长度，int 类型。|
|PowerPin|int|Power Pin 对象|
|StandbyPin|int|Standby 模式 Pin 对象|
|BackupPin|int|Backup 模式 Pin 对象|

#### GNSS.set_trans

> 设置 NMEA 原始数据透传打印使能, 透传功能默认关闭。**默认透传到标准输出**。

**示例：**

```python
gnss.set_trans(1, print)
```

**参数：**

|参数|类型|说明|
|:---|---|---|
|mode|int|0 - 关闭透传打印, 1 - 开启透传打印|
|output|fun|透传方式, 默认 `print` 方法, 也可使用其他方法进行透传, 如串口, 回调等|

#### GNSS.set_back_size

> 设置历史定位数据备份数量, 默认10。

**示例：**

```python
gnss.set_back_size(20)
```

**参数：**

|参数|类型|说明|
|:---|---|---|
|size|int|历史定位数据备份数量|

#### GNSS.start

> 开始 GNSS 模块 NMEA 数据读取与解析

**示例：**

```python
gnss.start()
```

**返回值：**

|数据类型|说明|
|:---|---|
|bool|True - 成功, False - 失败|

#### GNSS.stop

> 停止 GNSS 模块 NMEA 数据读取与解析

**示例：**

```python
gnss.stop()
```

#### GNSS.read

> 读取 GPS 数据

**示例：**

```python
# 读取格式化后当前最新 GNSS 定位数据
current_gps_data = gnss.read(mode=0)
print(current_gps_data)
# {'speed': '0.0', 'state': 'A', 'lng': '117.11553485', 'course': '000.00', 'satellites': '08', 'altitude': '94.6', 'lat_dir': 'N', 'datestamp': '081223', 'timestamp': '062555.000', 'lng_dir': 'E', 'lat': '31.8216808'}

# 读取格式化后历史 GNSS 定位数据
history_gps_data = gnss.read(mode=1)
print(history_gps_data)
# [{'speed': '0.0', 'state': 'A', 'lng': '117.11553485', 'course': '000.00', 'satellites': '08', 'altitude': '94.6', 'lat_dir': 'N', 'datestamp': '081223', 'timestamp': '062554.000', 'lng_dir': 'E', 'lat': '31.82168078333333'},{'speed': '0.0', 'state': 'A', 'lng': '117.11553485', 'course': '000.00', 'satellites': '08', 'altitude': '94.6', 'lat_dir': 'N', 'datestamp': '081223', 'timestamp': '062555.000', 'lng_dir': 'E', 'lat': '31.8216808'},]

# 读取最近一包 GNSS 原始 NMEA 定位数据
nmea_data = gnss.read(mode=2)
print(nmea_data)
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

**参数：**

|参数|类型|说明|
|:---|---|---|
|mode|int|返回不同类型定位数据，默认：0。枚举值如下：<br>0 - 格式化后当前最新 GNSS 定位数据<br>1 - 格式化后历史 GNSS 定位数据, 最多存储 10 包历史数据<br>2 - 最近一包 GNSS 原始 NMEA 定位数据。|

**返回值：**

|数据类型|说明|
|:---|---|
|dict|当前最新 GNSS 定位数据的常用定位数据信息，如需调整，可调整 `GNSSBase._parse_loc` 方法进行其他定位数据的新增<br>定位数据项:<br>state - 定位状态（A - 有效定位，V - 无效定位）<br>lng - 经度<br>lng_dir - 经度方向（E - 东，W - 西）<br>lat - 纬度<br>lat_dir - 纬度方向（N - 北，S - 南）<br>speed - 速度（单位: km/h）<br>course - 地面航向（单位: 度，以真北为参考基）<br>datestamp - 日期（DDMMYY）<br>datestamp - 时间（HHmmSS.000），UTC 时间<br>altitude - 海拔<br>satellites - 可见卫星的总数|
|list|历史 GNSS 定位数据的常用定位数据信息，只存储最近 10 条数据|
|bytes|最近一包 GNSS 原始NMEA定位数据|

### CellLocator

> 基站定位。

**示例：**

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

**参数：**

|参数|类型|说明|
|:---|---|---|
|serverAddr|str|服务器域名，长度必须小于 255 bytes，目前仅支持 `www.queclocator.com`|
|port|int|服务器端口，目前仅支持 80 端口|
|token|str|密钥，16 位字符组成，需要申请|
|timeout|int|设置超时时间，范围1 - 300s，默认：300s|
|profileIdx|int|PDP 索引，ASR 平台范围 1 - 8，展锐平台范围 1 - 7|

#### CellLocator.read

> 读取基站定位信息

**示例：**

```python
cell.read()
# (117.1154556274414, 31.82186508178711, 550)
```

**参数：**

无

**返回值：**

|数据类型|说明|
|:---|---|
|tuple|定位信息（经度, 纬度, 精确度：米），失败返回空元组|

### WiFiLocator

> WIFI 定位.

**示例：**

```python
from loction import WiFiLocator
wifi_cfg = {
    "token": "xxxxxxxxxx",
}
wifi = WiFiLocator(**wifi_cfg)
```

**参数：**

|参数|类型|说明|
|:---|---|---|
|token|str|密钥，16 位字符组成，需要申请|

#### WiFiLocator.read

> 读取基站定位信息

**示例：**

```python
wifi.read()
# (117.1154556274414, 31.82186508178711, 550)
```

**参数：**

无

**返回值：**

|数据类型|说明|
|:---|---|
|tuple|定位信息（经度，纬度，精确度：米），失败返回空元组|

## 使用说明

```python
import utime
from location import CoordinateSystemConvert, NMEAParse, GNSS, CellLocator, WiFiLocator

# 坐标转换模块初始化
csc = CoordinateSystemConvert()

# NMEA 解析模块初始化
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
    "PowerPin": None,
    "StandbyPin": None,
    "BackupPin": None,
}
gnss = GNSS(**gps_cfg)

# 启动 GNSS 数据读取解析
gnss.start()

# 读取 GNSS 定位数据
while True:
    gps_data = gnss.read(mode=0)
    utime.sleep(1)

# 读取 GNSS 原始 NMEA 定位数据进行解析
while True:
    nmea_data = gnss.read(mode=2)
    # 解析 GNSS 原始数据
    nmea_parse.set_gps_data(gps_data)

    # 获取坐标信息
    lng = nmea_parse.Longitude
    lat = nmea_parse.Latitude
    altitude = nmea_parse.Altitude
    speed = nmea_parse.Speed

    # 转换坐标系
    gcj02_lng, gcj02_lat = csc.wgs84_to_gcj02(float(lng), float(lat))
    utime.sleep(1)

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

# WIFI 定位模块初始化
wifi_cfg = {
    "token": "xxxxxxxxxx",
}
wifi = WiFiLocator(**wifi_cfg)

# 读取 WIFI 定位信息
wifi.read()
# (117.1154556274414, 31.82186508178711, 550)
```
