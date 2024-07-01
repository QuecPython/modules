# Copyright (c) Quectel Wireless Solution, Co., Ltd.All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
@file      :location.py
@author    :Jack Sun (jack.sun@quectel.com)
@brief     :GNSS, Cell, Wifi location management.
@version   :1.2.0
@date      :2022-11-24 17:06:30
@copyright :Copyright (c) 2022
"""

import sys
import ure
import math
import utime
import _thread

try:
    import quecgnss
except ImportError:
    quecgnss = None
try:
    import cellLocator
except ImportError:
    cellLocator = None
try:
    from wifilocator import wifilocator
except ImportError:
    wifilocator = None

from machine import UART, Pin, I2C

from usr.modules.logging import getLogger


log = getLogger(__name__)

_gps_data_set_lock = _thread.allocate_lock()

CRLF = "\r\n"


class CoordinateSystemConvert:

    EE = 0.00669342162296594323
    EARTH_RADIUS = 6378.137  # Approximate Earth Radius(km)

    def _transformLat(self, x, y):
        ret = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * math.sqrt(math.fabs(x))
        ret += (20.0 * math.sin(6.0 * x * math.pi) + 20.0 * math.sin(2.0 * x * math.pi)) * 2.0 / 3.0
        ret += (20.0 * math.sin(y * math.pi) + 40.0 * math.sin(y / 3.0 * math.pi)) * 2.0 / 3.0
        ret += (160.0 * math.sin(y / 12.0 * math.pi) + 320 * math.sin(y * math.pi / 30.0)) * 2.0 / 3.0
        return ret

    def _transformLon(self, x, y):
        ret = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * math.sqrt(math.fabs(x))
        ret += (20.0 * math.sin(6.0 * x * math.pi) + 20.0 * math.sin(2.0 * x * math.pi)) * 2.0 / 3.0
        ret += (20.0 * math.sin(x * math.pi) + 40.0 * math.sin(x / 3.0 * math.pi)) * 2.0 / 3.0
        ret += (150.0 * math.sin(x / 12.0 * math.pi) + 300.0 * math.sin(x / 30.0 * math.pi)) * 2.0 / 3.0
        return ret

    def wgs84_to_gcj02(self, lon, lat):
        dLat = self._transformLat(lon - 105.0, lat - 35.0)
        dLon = self._transformLon(lon - 105.0, lat - 35.0)
        radLat = lat / 180.0 * math.pi
        magic = math.sin(radLat)
        magic = 1 - magic * magic * self.EE
        sqrtMagic = math.sqrt(magic)

        dLat = (dLat * 180.0) / ((self.EARTH_RADIUS * 1000 * (1 - self.EE)) / (magic * sqrtMagic) * math.pi)
        dLon = (dLon * 180.0) / (self.EARTH_RADIUS * 1000 / sqrtMagic * math.cos(radLat) * math.pi)
        lon02 = lon + dLon
        lat02 = lat + dLat

        return lon02, lat02


class NMEAParse:
    """This class is match and parse gps NEMA 0183"""

    def __init__(self):
        self.__gps_data = ""

    def __parse(self, nmea):
        return tuple(nmea[1:].split("*")[0].split(",")) if nmea else ()

    def set_gps_data(self, gps_data):
        self.__gps_data = gps_data.decode() if isinstance(gps_data, bytes) else gps_data

    @property
    def GxRMC(self):
        if self.__gps_data:
            rmc_re = ure.search(
                r"\$G[NP]RMC,\d*\.*\d*,*[AV],*\d*\.*\d*,*[NS],*\d*\.*\d*,*[EW],*\d*\.*\d*,*\d*\.*\d*,*\d*,*\d*\.*\d*,*[EW]*,*[ADEN]*,*[SCUV]*\**(\d|\w)*",
                self.__gps_data)
            if rmc_re:
                return rmc_re.group(0)
        return ""

    @property
    def GxGGA(self):
        if self.__gps_data:
            gga_re = ure.search(
                r"\$G[BLPN]GGA,\d*\.*\d*,*\d*\.*\d*,*[NS],*\d*\.*\d*,*[EW],*[0126],*\d*,*\d*\.*\d*,*-*\d*\.*\d*,*M,*-*\d*\.*\d*,*M,*\d*,*\**(\d|\w)*",
                self.__gps_data)
            if gga_re:
                return gga_re.group(0)
        return ""

    @property
    def GxVTG(self):
        if self.__gps_data:
            vtg_re = ure.search(
                r"\$G[NP]VTG,\d*\.*\d*,*T,*\d*\.*\d*,*M,*\d*\.*\d*,*N,*\d*\.*\d*,*K,*[ADEN]*\*(\d|\w)*",
                self.__gps_data)
            if vtg_re:
                return vtg_re.group(0)
        return ""

    @property
    def GxGSV(self):
        if self.__gps_data:
            gsv_re = ure.search(
                r"\$G[NP]GSV,\d*,*\d*,*\d*,*\d*,*\d*,*\d*,*\d*,*\d*,*\d*,*\d*,*\d*,*\d*,*\d*,*\d*,*\d*,*\d*,*\d*,*\d*,*\d*,*\d*\**(\d|\w)*",
                self.__gps_data)
            if gsv_re:
                return gsv_re.group(0)
        return ""

    @property
    def GxGLL(self):
        if self.__gps_data:
            gll_re = ure.search(
                r"\$G[NP]GLL,\d*\.*\d*,*[NS]*,*\d*\.*\d*,*[EW]*,*\d*\.*\d*,*[AV]*,*[ADEN]*\**(\d|\w)*",
                self.__gps_data)
            if gll_re:
                return gll_re.group(0)

    @property
    def GxGSA(self):
        if self.__gps_data:
            gsa_re = ure.search(
                r"\$G[NP]GSA,[MA]*,*[123]*,*\d*,*\d*,*\d*,*\d*,*\d*,*\d*,*\d*,*\d*,*\d*,*\d*,*\d*,*\d*,*\d*\.*\d*,*\d*\.*\d*,*\d*\.*\d*,*(\d|\w)*\**(\d|\w)*",
                self.__gps_data)
            if gsa_re:
                return gsa_re.group(0)

    @property
    def GxRMCData(self):
        """Recommended Minimum Specific GNSS Data

        Returns:
            tuple: (
                "GPRMC", UTC time, Positioning status, latitude, latitude hemisphere, longitude, longitude hemisphere,
                ground rate, ground heading, UTC date, magnetic declination, Magnetic declination direction, Mode indication
            )
        """
        return self.__parse(self.GxRMC)

    @property
    def GxGGAData(self):
        return self.__parse(self.GxGGA)

    @property
    def GxGSVData(self):
        return self.__parse(self.GxGSV)

    @property
    def GxGSAData(self):
        return self.__parse(self.GxGSA)

    @property
    def GxVTGData(self):
        return self.__parse(self.GxVTG)

    @property
    def GxGLLData(self):
        return self.__parse(self.GxGLL)

    @property
    def Latitude(self):
        lat = ""
        _gga = self.GxGGAData
        if _gga:
            lat = _gga[2]
            lat = str(float(lat[:2]) + float(lat[2:]) / 60)
            lat = ("" if _gga[3] == "N" else "-") + lat
        return lat

    @property
    def Longitude(self):
        lng = ""
        _gga = self.GxGGAData
        if _gga:
            lng = _gga[4]
            lng = str(float(lng[:3]) + float(lng[3:]) / 60)
            lng = ("" if _gga[5] == "E" else "-") + lng
        return lng

    @property
    def Altitude(self):
        _gga = self.GxGGAData
        alt = _gga[9] if _gga else ""
        return alt

    @property
    def Speed(self):
        _vtg = self.GxVTGData
        speed = _vtg[7] if _vtg else ""
        return speed


class GNSSPower:
    """This class is for GNSS power control.

    1. GNSS power switch.
    2. GNSS standby mode of low energy.
    3. GNSS backup mode of low energy.
    """

    def __init__(self, PowerPin, StandbyPin, BackupPin):
        self.__pw = {
            "power": {
                "pin": PowerPin,
                "gpio": None,
            },
            "standby": {
                "pin": StandbyPin,
                "gpio": None,
            },
            "backup": {
                "pin": BackupPin,
                "gpio": None,
            },
        }

    def __pw_ctrl(self, method, onoff):
        """Control gpio high or low level.

        Args:
            method (str): power, standby, backup.
            onoff (int): 1 - high level, 0 - low level.

        Returns:
            bool: True - success, False - failed.
        """
        if not self.__pw.get(method) or onoff not in (0, 1):
            return False
        if self.__pw[method]["gpio"] is None:
            self.__pw[method]["gpio"] = Pin(self.__pw[method]["pin"], Pin.OUT, Pin.PULL_DISABLE, onoff)
        if self.__pw[method]["gpio"].read() != onoff:
            self.__pw[method]["gpio"].write(onoff)
            utime.sleep_ms(50)
            if self.__pw[method]["gpio"].read() != onoff:
                return False
        return True

    def power(self, onoff):
        """Control gnss power.

        Args:
            onoff (int): 1 - high level, 0 - low level.

        Returns:
            bool: True - success, False - failed.
        """
        return self.__pw_ctrl("power", onoff) if self.__pw["power"]["pin"] else False

    def backup(self, onoff):
        """Control gnss backup mode of low energy.

        Args:
            onoff (int): 1 - high level, 0 - low level.

        Returns:
            bool: True - success, False - failed.
        """
        return self.__pw_ctrl("backup", onoff) if self.__pw["backup"]["pin"] else False

    def standby(self, onoff):
        """Control gnss standby mode of low energy.

        Args:
            onoff (int): 1 - high level, 0 - low level.

        Returns:
            bool: True - success, False - failed.
        """
        return self.__pw_ctrl("standby", onoff) if self.__pw["standby"]["pin"] else False


class GNSSBase(GNSSPower):
    """This class is GNSS module base class."""

    def __init__(self, PowerPin=None, StandbyPin=None, BackupPin=None):
        super().__init__(PowerPin, StandbyPin, BackupPin)
        self.__nmea_parse = NMEAParse()
        self.__running = 0
        self.__running_end = 0
        self.__tid = None
        self.__lock = _thread.allocate_lock()
        self.__current_loc = {
            "timestamp": "",
            "state": "",
            "lat": "",
            "lat_dir": "",
            "lng": "",
            "lng_dir": "",
            "speed": "",
            "course": "",
            "datestamp": "",
            "altitude": "",
            "satellites": "",
        }
        self.__hist_locs = []
        self.__hist_size = 10
        self.__current_nmea = b""
        self.__trans = 0
        self.__trans_output = print

    def _open(self):
        """Open gnss."""
        pass

    def _close(self):
        """Close gnss."""
        pass

    def _receive(self):
        """Receive gnss nmea data."""
        pass

    def _parse_loc(self, gps_data):
        """Parse gnss nmea data.

        Args:
            gps_data (str/bytes): gnss nmea data.
        """
        if not gps_data:
            return
        if self.__trans:
            self.__trans_output(gps_data)
        self.__current_nmea = gps_data
        self.__nmea_parse.set_gps_data(gps_data)
        rmc_data = self.__nmea_parse.GxRMCData
        if rmc_data and rmc_data[2] == "A":
            with self.__lock:
                self.__current_loc["timestamp"] = rmc_data[1]
                self.__current_loc["state"] = rmc_data[2]
                # self.__current_loc["lat"] = rmc_data[3]
                self.__current_loc["lat"] = str(float(rmc_data[3][:2]) + float(rmc_data[3][2:]) / 60)
                self.__current_loc["lat_dir"] = rmc_data[4]
                # self.__current_loc["lng"] = rmc_data[5]
                self.__current_loc["lng"] = str(float(rmc_data[5][:3]) + float(rmc_data[5][3:]) / 60)
                self.__current_loc["lng_dir"] = rmc_data[6]
                self.__current_loc["speed"] = str(float(rmc_data[7]) * 1.852)
                self.__current_loc["course"] = rmc_data[8]
                self.__current_loc["datestamp"] = rmc_data[9]
                gga_data = self.__nmea_parse.GxGGAData
                self.__current_loc["altitude"] = gga_data[9]
                gsv_data = self.__nmea_parse.GxGSVData
                self.__current_loc["satellites"] = gsv_data[3]

        if len(self.__hist_locs) >= self.__hist_size:
            self.__hist_locs.pop(0)
        self.__hist_locs.append(self.__current_loc)

    def set_trans(self, mode, output=print):
        """Set transparent tag for weather to print gnss nmae or not.

        Args:
            mode (int): 0 - disable, 1 - enable.
        """
        assert mode in (0, 1), "transparent mode must be 0 or 1."
        assert callable(output), "output must be callable."
        self.__trans = mode
        self.__trans_output = output

    def set_back_size(self, size):
        """Set history location data backup size.

        Args:
            size(int): History location data backup size.
        """
        assert isinstance(size, int) and size > 0, "History location data size must be int and larger than 0."
        self.__hist_size = size

    def read(self, mode=0):
        """Read gnss data.

        Args:
            mode (int): 0 - current loction data, 1 - history location datas(max numbers is 10) (default: `0`)

        Returns:
            dict/list: location data.
        """
        with self.__lock:
            return self.__current_loc if mode == 0 else (self.__hist_locs if mode == 1 else self.__current_nmea)

    def start(self):
        """Start a thread for reading and parsing gnss nmea data.

        Returns:
            bool: True - success, False - failed.
        """
        if self.__running == self.__running_end == 0:
            self.__running = 1
            try:
                if not self.__tid or (self.__tid and not _thread.threadIsRunning(self.__tid)):
                    _thread.stack_size(0x2000)
                    self.__tid = _thread.start_new_thread(self._receive, ())
                    return True
            except Exception as e:
                sys.print_exception(e)
        return False

    def stop(self):
        """Stop gnss reading thread."""
        self.__running = 0 if self.__running == 1 else self.__running


class GNSSInternal(GNSSBase):
    """This class is for internal gnss."""

    def __init__(self):
        super().__init__()
        assert quecgnss is not None, "quecgnss is not supported."
        assert quecgnss.init() == 0, "quecgnss init failed"
        self._close()

    def _open(self):
        """Enable quecgness.

        Returns:
            bool: True - success, False - failed.
        """
        return (quecgnss.gnssEnable(1) == 0)

    def _close(self):
        """Disable quecgness.

        Returns:
            bool: True - success, False - failed.
        """
        return (quecgnss.gnssEnable(0) == 0)

    def _receive(self):
        """Thread for reading and parsing gnss nmea data."""
        log.debug("__internal_read start.")
        self.__running_end = 1
        self._open()
        while self.__running:
            gnss_data = quecgnss.read(1024)
            self._parse_loc(gnss_data[1] if (isinstance(gnss_data, tuple) and gnss_data[1]) else b"")
            utime.sleep(1)
        self._close()
        self.__tid = None
        self.__running_end = 0
        log.debug("__internal_read stop.")


class GNSSExternalUART(GNSSBase):
    """This class is for external gnss."""

    def __init__(self, UARTn, buadrate, databits, parity, stopbits, flowctl, PowerPin, StandbyPin, BackupPin):
        super().__init__(PowerPin, StandbyPin, BackupPin)
        self.__uart_args = (UARTn, buadrate, databits, parity, stopbits, flowctl)
        self.__gnss = None

    def _open(self):
        """Enable gnss power and init uart for reading gnss nmea data."""
        self.power(1)
        self.__gnss = UART(*self.__uart_args)

    def _close(self):
        """Close uart for stop reading gnss nmea data."""
        self.__gnss.close()

    def _receive(self):
        """Thread for reading and parsing gnss nmea data."""
        log.debug("GNSSExternalUART _receive start.")
        self.__running_end = 1
        self._open()
        while self.__running:
            size = self.__gnss.any()
            self._parse_loc(self.__gnss.read(size) if size > 0 else b"")
            utime.sleep(1)
        self._close()
        self.__tid = None
        self.__running_end = 0
        log.debug("GNSSExternalUART _receive stop.")


class GNSSExternalI2C(GNSSBase):

    def __init__(self, I2Cn, i2cmode, slaveaddress, addr, addr_len, PowerPin, StandbyPin, BackupPin):
        super().__init__(PowerPin, StandbyPin, BackupPin)
        self.__gnss = I2C(I2Cn, i2cmode)
        self.slaveaddress = slaveaddress
        self.addr = addr
        self.addr_len = addr_len
        self.source_data = b""

    def _receive(self):
        log.debug("GNSSExternalI2C _receive start.")
        self.__running_end = 1
        self._open()
        recv_size = 1024
        nmea_data = bytearray([])
        while self.__running:
            recv_data = bytearray(recv_size)
            self.__gnss.read(self.slaveaddress, self.addr, self.addr_len, recv_data, recv_size, 0)
            nmea_data.extend(recv_data)
            nmea_data = self._parse_loc(nmea_data)
            utime.sleep_ms(500)
        self._close()
        self.__tid = None
        self.__running_end = 0
        log.debug("GNSSExternalI2C _receive stop.")

    def _parse_loc(self, data):
        gps_data = bytearray([])
        for i in data:
            if i != 0x00:
                gps_data.append(i)
            else:
                if gps_data:
                    super()._parse_loc(bytes(gps_data))
                    gps_data = bytearray([])
        return gps_data


class GNSS:
    """This class is GNSS module, return GNSSInternal or GNSSExternalUART by checking gps mode args."""

    class GPS_MODE:
        internal = 0x1
        external_uart = 0x2
        external_i2c = 0x3

    def __new__(cls, *args, **kwargs):
        if kwargs.get("gps_mode") == cls.GPS_MODE.internal:
            return GNSSInternal()
        elif kwargs.get("gps_mode") == cls.GPS_MODE.external_uart:
            return GNSSExternalUART(
                kwargs.get("UARTn"), kwargs.get("buadrate"), kwargs.get("databits"), kwargs.get("parity"), kwargs.get("stopbits"), kwargs.get("flowctl"),
                kwargs.get("PowerPin"), kwargs.get("StandbyPin"), kwargs.get("BackupPin")
            )
        elif kwargs.get("gps_mode") == cls.GPS_MODE.external_i2c:
            return GNSSExternalI2C(
                kwargs.get("I2Cn"), kwargs.get("i2cmode"), kwargs.get("slaveaddress"), kwargs.get("addr"), kwargs.get("addr_len"),
                kwargs.get("PowerPin"), kwargs.get("StandbyPin"), kwargs.get("BackupPin")
            )
        else:
            raise ValueError("Args gps_mode is not compare.")


class CellLocator:
    """This class is for reading cell location data"""

    def __init__(self, serverAddr, port, token, timeout, profileIdx):
        self.__args = (serverAddr, port, token, timeout, profileIdx)

    def read(self):
        loc_data = -1
        try:
            loc_data = cellLocator.getLocation(*self.__args) if cellLocator else -1
        except Exception as e:
            sys.print_exception(e)
        return loc_data


class WiFiLocator:
    """This class is for reading wifi location data"""

    def __init__(self, token):
        self.__wifilocator = wifilocator(token) if wifilocator else None

    def read(self):
        loc_data = -1
        try:
            return self.__wifilocator.getwifilocator() if self.__wifilocator else -1
        except Exception as e:
            sys.print_exception(e)
        return loc_data
