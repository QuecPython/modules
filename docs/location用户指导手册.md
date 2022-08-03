# 定位模块 用户指导手册

## 简介

> 本模块使用的定位坐标系为WGS-84, 如需转换GCJ-02坐标系, 本模块提供了`WGS84ToGCJ02`方法进行经纬度坐标系的转换

## 使用说明

### GPSMatch

#### 1. 模块初始化

```python
from loction import GPSMatch

gps_match = GPSMatch()
```

#### 2. GPS明码语句匹配

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

#### 1. 模块初始化

```python
from loction import GPSParse

gps_parse = GPSParse()
```

#### 2. GPS内容解析

```python
gga_data = "$GNGGA,064758.000,3149.333010,N,11706.927563,E,1,9,1.30,98.483,M,-0.336,M,,*64"
vtg_data = "$GNVTG,19.23,T,,M,1.19,N,2.20,K,A*13"
gsv_data = "$GPGSV,4,4,13,24,03,306,15,1*52"

gga_satellite_num = gps_parse.GxGGA_satellite_num(gga_data)
print(gga_satellite_num)
# "9"

gga_latitude = gps_parse.GxGGA_latitude(gga_data)
print(gga_latitude)
# "31.82221683333333"

gga_longitude = gps_parse.GxGGA_longitude(gga_data)
print(gga_longitude)
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

#### 1. 模块初始化

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

#### 2. 读取GPS数据

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

#### 3. 获取GPS定位信息(经纬度, 海拔)

```python

coordinates = gps.read_coordinates(gps_data)
print(coordinates)
# (117.1154593833333, 31.82221683333333, 98.483)
```

#### 4. 关闭GPS电源或开启低功耗模式

```python
# 关闭开启
onoff = 0
res = gps.power_switch(onoff)

# backup模式低功耗开启
onoff = 1
res = gps.backup(onoff)

# standby模式低功耗开始
onoff = 1
res = gps.standby(onoff)
```

### CellLocator

#### 1. 模块初始化

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

#### 2. 定位信息读取

```python
res = cell.read()
print(res)
# (0, (117.1154556274414, 31.82186508178711, 550), {'near_cell': ['232301364'], 'server_cell': ([], [], [(0, 232301364, 1120, 17, 377, 26909, 1850, -72, -6)])})
```

### WiFiLocator

#### 1. 模块初始化

```python
from location import WiFiLocator

wifi_cfg = {
    "token": "XXX"
}

wifi = WiFiLocator(wifi_cfg)
```

#### 2. 定位信息读取

```python
res = wifi.read()
print(res)
# (0, (117.1156539916992, 31.82171249389649, 60), ['34:CE:00:09:E5:A8', '60:38:E0:C2:84:D9', '00:03:7F:12:A5:A5', 'EC:B9:70:F1:8F:B5', '24:4B:FE:0B:BE:70'])
```

### Location

#### 1. 模块初始化

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

#### 2. 定位信息读取

```python
loc_method = 7
res = locator.read(loc_method)
print(res)
# {4: ((117.1156692504883, 31.82216453552246, 45), ['34:CE:00:09:E5:A8', '62:E5:A1:83:D6:AF', '00:0A:F5:F7:3C:48', 'EC:B9:70:F1:8F:B5', 'EE:B9:70:D1:8F:B5']), 1: '$GNGLL,3149.333010,N,11706.927563,E,064758.000,A,A*4F\r\n$BDGSV,5,5,17,11,04,276,,1*44\r\n$BDGSV,5,4,17,19,24,059,,05,18,251,,21,16,172,,25,15,312,21,1*7A\r\n$BDGSV,5,3,17,22,39,120,,02,38,230,,04,32,119,,26,25,199,,1*7A\r\n$BDGSV,5,2,17,13,49,228,,12,44,307,27,01,43,135,,24,40,254,,1*71\r\n$BDGSV,5,1,17,07,84,161,,10,78,301,23,08,64,233,,03,53,193,,1*71\r\n$GPGSV,4,4,13,24,03,306,15,1*52\r\n$GPGSV,4,3,13,02,06,249,,04,04,109,,30,04,193,,09,03,140,,1*61\r\n$GPGSV,4,2,13,06,47,264,,194,44,165,,03,43,061,15,01,17,049,18,1*5F\r\n$GPGSV,4,1,13,195,67,060,30,14,63,177,17,17,61,359,19,19,48,325,17,1*5D\r\n$GNGSA,A,3,10,12,25,,,,,,,,,,1.56,1.30,0.86,4*0F\r\n$GNGSA,A,3,14,17,195,19,01,03,,,,,,,1.56,1.30,0.86,1*3B\r\n$GNGGA,064758.000,3149.333010,N,11706.927563,E,1,9,1.30,98.483,M,-0.336,M,,*64\r\n$GNVTG,19.23,T,,M,1.19,N,2.20,K,A*13\r\n$GNRMC,064758.000,A,3149.333010,N,11706.927563,E,1.19,19.23,060522,,,A,V*31\r\n$GPTXT,01,01,02,ANTSTATUS=OPEN*2B', 2: ((117.1154556274414, 31.82186508178711, 550), {'near_cell': ['232301364'], 'server_cell': ([], [], [(0, 232301364, 1120, 17, 377, 26909, 1850, -71, -8)])})}
```

#### 3. 经纬度坐标系转换

```python
wgs84_longitude = 117.1154593833333
wgs84_latitude = 31.82221683333333

gcj02_longitude, gcj02_latitude = locator.wgs84togcj02(wgs84_longitude, wgs84_latitude)
print(gcj02_longitude, gcj02_latitude)
# 117.121085101472 31.82038457486135
```

## API说明

### WGS84ToGCJ02

> 经纬度坐标系转换

示例:

```python
from location import WGS84ToGCJ02

wgs84_longitude = 117.1154593833333
wgs84_latitude = 31.82221683333333

gcj02_longitude, gcj02_latitude = WGS84ToGCJ02(wgs84_longitude, wgs84_latitude)
print(gcj02_longitude, gcj02_latitude)
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

> $GPRMC,<1>,<2>,<3>,<4>,<5>,<6>,<7>,<8>,<9>,<10>,<11>,<12>\*hh<CR><LF>

| RMC | 是否强匹配 |
|---|---|
| <1>UTC时间 | 是 |
| <2>定位状态 | 是 |
| <3>纬度 | 是 |
| <4>纬度半球N或S | 是 |
| <5>经度 | 是 |
| <6>经度半球E或W | 是 |
| <7>地面速率 | 否 |
| <8>地面航向 | 否 |
| <9>UTC日期 | 是 |
| <10>磁偏角 | 否 |
| <11>磁偏角方向E或W | 否 |
| <12>模式指示 | 否 |

参数:

|参数|类型|说明|
|:---|---|---|
|gps_data|STRING|GPS明码语句|

返回值:

|数据类型|说明|
|:---|---|
|STRING|RMC语句|

#### GxGGA GGA(全球定位系统定位数据, 如时间、定位等)

> $GPGGA,<1>,<2>,<3>,<4>,<5>,<6>,<7>,<8>,<9>,M,<10>,M,<11>,<12>\*hh<CR><LF>

| GGA | 是否强匹配 |
|---|---|
| <1>UTC时间 | 是 |
| <2>纬度 | 是 |
| <3>纬度半球N或S | 是 |
| <4>经度 | 是 |
| <5>经度半球E或W | 是 |
| <6>GPS状态 | 是 |
| <7>正在使用解算位置的卫星数量 | 是 |
| <8>HDOP水平精度因子 | 否 |
| <9>海拔高度 | 是 |
| <10>地球椭球面相对大地水准面的高度 | 否 |
| <11>差分时间 | 否 |
| <12>差分站ID号 | 否 |

参数:

|参数|类型|说明|
|:---|---|---|
|gps_data|STRING|GPS明码语句|

返回值:

|数据类型|说明|
|:---|---|
|STRING|GGA语句|

#### GxVTG VTG(矢量跟踪与对地速度)

> $GPVTG,<1>,T,<2>,M,<3>,N,<4>,K,<5>\*hh<CR><LF>

| VTG | 是否强匹配 |
|---|---|
| <1>以真北为参考基准的地面航向 | 是 |
| <2>以磁北为参考基准的地面航向 | 是 |
| <3>地面速率 | 是 |
| <4>地面速率 | 是 |
| <5>模式指示 | 是 |

参数:

|参数|类型|说明|
|:---|---|---|
|gps_data|STRING|GPS明码语句|

返回值:

|数据类型|说明|
|:---|---|
|STRING|VTG语句|

#### GxGSV GSV(可见的 GNSS 卫星)

> $GPGSV,<1>,<2>,<3>,<4>,<5>,<6>,<7>,…<4>,<5>,<6>,<7>\*hh<CR><LF>

| GSV | 是否强匹配 |
|---|---|
| <1>GSV语句的总数 | 是 |
| <2>本句GSV的编号 | 是 |
| <3>可见卫星的总数 | 是 |
| <4>PRN码 | 否 |
| <5>卫星仰角 | 否 |
| <6>卫星方位角 | 否 |
| <7>信噪比 | 否 |

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
|STRING|卫星数, 无返回空字符串|

#### GxGGA_latitude 纬度

参数:

|参数|类型|说明|
|:---|---|---|
|gga_data|STRING|GGA明码语句|

返回值:

|数据类型|说明|
|:---|---|
|STRING|纬度|

#### GxGGA_longitude 经度

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
|STRING|卫星数, 无返回空字符串|

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

gga_longitude = gps_parse.GxGGA_longitude(gga_data)
print(gga_longitude)
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

> GPS 定位模块, 用于开启关闭GPS模块, 读取GPS数据

#### 导入初始化

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
|gps_cfg|DICT|外置GPS读取uart配置信息, 内置GPS可以传空字典|
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

#### read_coordinates 获取GPS定位信息(经纬度, 海拔)

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
|TUPLE|元素1经度, 元素2纬度, 元素3海拔|

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

> 基站定位模块, 获取基站定位信息与小区信息

#### 导入初始化

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
|TUPLE|元素1成功失败, 0-成功, -1失败；元素2定位信息(经度, 纬度, 精确度(单位米))；元素3小区信息, `near_cell`小区id列表, `server_cell`[三种网络系统（GSM、UMTS、LTE）的信息的列表](https://python.quectel.com/wiki/#/zh-cn/api/QuecPythonClasslib?id=%e8%8e%b7%e5%8f%96%e5%b0%8f%e5%8c%ba%e4%bf%a1%e6%81%af)|

### WiFiLocator

> WIFI定位模块, 获取WIFI定位信息与热点MAC地址

#### 导入初始化

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
|TUPLE|元素1成功失败, 0-成功, -1失败；元素2定位信息(经度, 纬度, 精确度(单位米))；元素3热点mac地址列表|

### Location

> 定位信息读取模块, 可直接传入三种定位方式的配置信息, 直接一次读取指定定位方式的定位信息

#### 导入初始化

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
wgs84_longitude = 117.1154593833333
wgs84_latitude = 31.82221683333333

gcj02_longitude, gcj02_latitude = locator.wgs84togcj02(wgs84_longitude, wgs84_latitude)
print(gcj02_longitude, gcj02_latitude)
# 117.121085101472 31.82038457486135
```

参数:

|参数|类型|说明|
|:---|---|---|
|Longitude|FLOAT|WGS84经度|
|Latitude|FLOAT|WGS84纬度|

返回值:

|数据类型|说明|
|:---|---|
|TUPLE|元素1: GCJ02经度, 元素2: GCJ02纬度|
