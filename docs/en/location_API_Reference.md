# Location Module API Reference Manual

[中文](../zh/location_API参考手册.md) | English

## Introduction

> This module provides functionality encapsulation for three positioning modes: GNSS positioning, base station positioning, and WiFi positioning. It also provides methods for converting coordinates from WGS-84 to GCJ-02 coordinate systems.

## API Description

### CoordinateSystemConvert

> Coordinate system conversion module, which can convert WGS84 coordinates to GCJ02 coordinates.

**Example:**

```python
from location import CoordinateSystemConvert

csc = CoordinateSystemConvert()
```

#### CoordinateSystemConvert.wgs84_to_gcj02

> Convert WGS84 coordinates to GCJ02 coordinates.

**Example:**

```python
wgs84_longitude = 117.1154593833333
wgs84_latitude = 31.82221683333333
gcj02_longitude, gcj02_latitude = csc.wgs84_to_gcj02(wgs84_longitude, wgs84_latitude)
print(gcj02_longitude, gcj02_latitude)
# 117.121085101472 31.82038457486135
```

**Parameters:**

|Parameter|Type|Description|
|:---|---|---|
|Longitude|float|WGS84 longitude|
|Latitude|float|WGS84 latitude|

**Return Value:**

|Data Type|Description|
|:---|---|
|tuple|Element 1: GCJ02 longitude, Element 2: GCJ02 latitude|

### NMEAParse

> NMEA plain text sentence parsing.

**Example:**

```python
from location import NMEAParse

nmea_parse = NMEAParse()
```

#### NMEAParse.set_gps_data

> Set the NMEA plain text sentence to be parsed.

**Example:**

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

**Parameters:**

|Parameter|Type|Description|
|:---|---|---|
|data|str/bytes|NMEA plain text sentence|

**Return Value:**

None

#### NMEAParse.GxRMC

> Recommended Minimum Specific GPS/TRANSIT Data (RMC) recommended positioning information.

**Data Format:**

> $GPRMC,<1>,<2>,<3>,<4>,<5>,<6>,<7>,<8>,<9>,<10>,<11>,<12>\*hh<CR><LF>

| RMC |
|---|
| <1> UTC time, hhmmss format |
| <2> Latitude ddmm.mmmm format (leading zeros will also be transmitted) |
| <3> Latitude hemisphere N (North) or S (South) |
| <4> Longitude dddmm.mmmm format (leading zeros will also be transmitted) |
| <5> Longitude hemisphere E (East) or W (West) |
| <6> GPS status: 0=not positioned, 1=non-differential positioning, 2=differential positioning, 6=estimating |
| <7> Number of satellites used for positioning (00 ~ 12) (leading zeros will also be transmitted) |
| <8> HDOP horizontal precision factor (0.5 ~ 99.9) |
| <9> Altitude (-9999.9 ~ 99999.9) |
| <10> Height of the geoid above the WGS84 ellipsoid |
| <11> Differential time (seconds since the last received differential signal; empty if not differential positioning) |
| <12> Differential station ID number 0000 ~ 1023 (leading zeros will also be transmitted; empty if not differential positioning) |

**Example:**

```python
nmea_parse.GxRMC
# $GNRMC,064758.000,A,3149.333010,N,11706.927563,E,1.19,19.23,060522,,,A,V*31
```

**Return Value:**

|Data Type|Description|
|:---|---|
|str|RMC sentence|

#### NMEAParse.GxGGA

> Recommended Minimum Specific GPS/TRANSIT Data (RMC) recommended positioning information.

**Data Format:**

> $GPGGA,<1>,<2>,<3>,<4>,<5>,<6>,<7>,<8>,<9>,M,<10>,M,<11>,<12>\*hh<CR><LF>

| GGA |
|---|
| <1> UTC time, hhmmss format |
| <2> Latitude ddmm.mmmm format (leading zeros will also be transmitted) |
| <3> Latitude hemisphere N (North) or S (South) |
| <4> Longitude dddmm.mmmm format (leading zeros will also be transmitted) |
| <5> Longitude hemisphere E (East) or W (West) |
| <6> GPS status: 0=not positioned, 1=non-differential positioning, 2=differential positioning, 6=estimating |
| <7> Number of satellites used for positioning (00 ~ 12) (leading zeros will also be transmitted) |
| <8> HDOP horizontal precision factor (0.5 ~ 99.9) |
| <9> Altitude (-9999.9 ~ 99999.9) |
| <10> Height of the geoid above the WGS84 ellipsoid |
| <11> Differential time (seconds since the last received differential signal; empty if not differential positioning) |
| <12> Differential station ID number 0000 ~ 1023 (leading zeros will also be transmitted; empty if not differential positioning) |

**Example:**

```python
nmea_parse.GxGGA
# $GNGGA,064758.000,3149.333010,N,11706.927563,E,1,9,1.30,98.483,M,-0.336,M,,*64
```

**Return Value:**

|Data Type|Description|
|:---|---|
|str|GGA sentence|

#### NMEAParse.GxVTG

> Recommended Minimum Specific GPS/TRANSIT Data (RMC) recommended positioning information.

**Data Format:**

> $GPVTG,<1>,T,<2>,M,<3>,N,<4>,K,<5>\*hh<CR><LF>

| VTG |
|---|
| <1> Total number of GSV sentences |
| <2> Number of this GSV sentence |
| <3> Total number of visible satellites (00 ~ 12, leading zeros will also be transmitted) |
| <4> PRN code (pseudo-random noise code) (01 ~ 32, leading zeros will also be transmitted) |
| <5> Satellite elevation (00 ~ 90 degrees, leading zeros will also be transmitted) |
| <6> Satellite azimuth (000 ~ 359 degrees, leading zeros will also be transmitted) |
| <7> Signal-to-noise ratio (00 ~ 99dB, empty if no satellite is being tracked, leading zeros will also be transmitted) |

**Example:**

```python
nmea_parse.GxVTG
# $GNVTG,19.23,T,,M,1.19,N,2.20,K,A*13H
```

**Return Value:**

|Data Type|Description|
|:---|---|
|str|VTG sentence|

#### NMEAParse.GxGSV

> GPS Satellites in View (GSV) visible satellite information.

**Data Format:**

> $GPGSV,<1>,<2>,<3>,<4>,<5>,<6>,<7>,…<4>,<5>,<6>,<7>\*hh<CR><LF>

| GSV |
|---|
| <1> Total number of GSV sentences |
| <2> Number of this GSV sentence |
| <3> Total number of visible satellites (00 ~ 12, leading zeros will also be transmitted) |
| <4> PRN code (pseudo-random noise code) (01 ~ 32, leading zeros will also be transmitted) |
| <5> Satellite elevation (00 ~ 90 degrees, leading zeros will also be transmitted) |
| <6> Satellite azimuth (000 ~ 359 degrees, leading zeros will also be transmitted) |
| <7> Signal-to-noise ratio (00 ~ 99dB, empty if no satellite is being tracked, leading zeros will also be transmitted) |

**Example:**

```python
nmea_parse.GxGSV
# $GPGSV,4,1,13,195,67,060,30,14,63,177,17,17,61,359,19,19,48,325,17,1*5D
```

**Return Value:**

|Data Type|Description|
|:---|---|
|str|GSV sentence|

#### NMEAParse.GxGLL

> Geographic Position (GLL) positioning geographic information.

**Data Format:**

> $GPGLL,<1>,<2>,<3>,<4>,<5>,<6>,<7>\*hh<CR><LF>

| GLL |
|---|
| <1> Latitude ddmm.mmmm format (leading zeros will also be transmitted)|
| <2> Latitude hemisphere N (North) or S (South)|
| <3> Longitude dddmm.mmmm format (leading zeros will also be transmitted)|
| <4> Longitude hemisphere E (East) or W (West)|
| <5> UTC time, hhmmss format|
| <6> Positioning status, A=valid positioning, V=invalid positioning|
| <7> Mode indicator (only output in NMEA0183 3.00 version, A=autonomous positioning, D=differential, E=estimate, N=data invalid)|

**Example:**

```python
nmea_parse.GxGLL
# $GNGLL,3149.333010,N,11706.927563,E,064758.000,A,A*4F
```

**Return Value:**

|Data Type|Description|
|:---|---|
|str|GLL sentence|

#### NMEAParse.GxGSA

> GPS DOP and Active Satellites (GSA) current satellite information.

**Data Format:**

> $GPGSA,<1>,<2>,<3>,<4>,<5>,<6>,<7>\*hh<CR><LF>

| GSA |
|---|
| <1> Mode, M=manual, A=automatic |
| <2> Positioning type, 1=no positioning, 2=2D positioning, 3=3D positioning |
| <3> PRN code (pseudo-random noise code), satellite number used for positioning (01 ~ 32, leading zeros will also be transmitted). |
| <4> PDOP position precision factor (0.5 ~ 99.9) |
| <5> HDOP horizontal precision factor (0.5 ~ 99.9) |
| <6> VDOP vertical precision factor (0.5 ~ 99.9 |

**Example:**

```python
nmea_parse.GxGSA
# $GNGSA,A,3,10,12,25,,,,,,,,,,1.56,1.30,0.86,4*0F
```

**Return Value:**

|Data Type|Description|
|:---|---|
|str|GSA sentence|

#### NMEAParse.GxRMCData

> RMC sentence returned as a tuple split by commas.

```python
nmea_parse.GxRMCData
# ("GNRMC", "064758.000", "A", "3149.333010", "N", "11706.927563", "E", "1.19", "19.23", "060522", "", "", "A", "V")
```

**Return Value:**

|Data Type|Description|
|:---|---|
|tuple|See RMC data format|

#### NMEAParse.GxGGAData

> GGA sentence returned as a tuple split by commas.

```python
nmea_parse.GxGGAData
# ("GNGGA", "064758.000", "3149.333010", "N", "11706.927563", "E", "1", "9", "1.30", "98.483", "M", "-0.336", "M", "", "")
```

**Return Value:**

|Data Type|Description|
|:---|---|
|tuple|See GGA data format|

#### NMEAParse.GxGSVData

> GSV sentence returned as a tuple split by commas.

```python
nmea_parse.GxGSVData
# ("GPGSV", "4", "1", "13", "195", "67", "060", "30", "14", "63", "177", "17", "17", "61", "359", "19", "19", "48", "325", "17", "1")
```

**Return Value:**

|Data Type|Description|
|:---|---|
|tuple|See GSV data format|

#### NMEAParse.GxGSAData

> GSA sentence returned as a tuple split by commas.

```python
nmea_parse.GxGSAData
# ("GNGSA", "A", "3", "14", "17", "195", "19", "01", "03", "", "", "", "", "", "", "1.56", "1.30", "0.86", "1")
```

**Return Value:**

|Data Type|Description|
|:---|---|
|tuple|See GSA data format|

#### NMEAParse.GxVTGData

> VTG sentence returned as a tuple split by commas.

```python
nmea_parse.GxVTGData
# ("GNVTG", "19.23", "T", "", "M", "1.19", "N", "2.20", "K", "A")
```

**Return Value:**

|Data Type|Description|
|:---|---|
|tuple|See VTG data format|

#### NMEAParse.GxGLLData

> GLL sentence returned as a tuple split by commas.

```python
nmea_parse.GxGLLData
# ("GNGLL", "3149.333010", "N", "11706.927563", "E", "064758.000", "A", "A")
```

**Return Value:**

|Data Type|Description|
|:---|---|
|tuple|See GLL data format|

#### NMEAParse.Latitude

> Latitude in GGA.

```python
nmea_parse.Latitude
# "31.82221683333333"
```

**Return Value:**

|Data Type|Description|
|:---|---|
|str|Latitude|

#### NMEAParse.Longitude

> Longitude in GGA.

```python
nmea_parse.Longitude
# "114.12411166633333"
```

**Return Value:**

|Data Type|Description|
|:---|---|
|str|Longitude|

#### NMEAParse.Altitude

> Altitude in GGA.

```python
nmea_parse.Altitude
# "98.483"
```

**Return Value:**

|Data Type|Description|
|:---|---|
|str|Altitude|

#### NMEAParse.Speed

> Speed in VTG.

```python
nmea_parse.Speed
# "2.20"
```

**Return Value:**

|Data Type|Description|
|:---|---|
|str|Speed|

### GNSS

> Read valid NMEA plain text sentences from the GNSS module. Supports built-in GNSS modules, external GNSS modules, and reading NMEA data via UART or I2C interfaces for external GNSS modules.

**Example:**

```python
from machine import UART, I2C
from location import GNSS

# Instantiate the built-in GNSS module
gps_cfg = {
    "gps_mode": GNSS.GPS_MODE.internal,
}
gnss = GNSS(**gps_cfg)

# Instantiate the external GNSS module, using UART for NMEA data reading
gps_cfg = {
    "gps_mode": GNSS.GPS_MODE.external_uart,
    "UARTn": UART.UART1,
    "buadrate": 115200,
    "databits": 8,
    "parity": 0,
