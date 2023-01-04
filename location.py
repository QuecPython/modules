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

import ure
import net
try:
    import math
except ImportError:
    math = None
import utime
import osTimer
import _thread
try:
    import wifiScan
except ImportError:
    wifiScan = None
try:
    import cellLocator
except ImportError:
    cellLocator = None

from queue import Queue
from machine import UART, Pin

from usr.modules.logging import getLogger
from usr.modules.common import Singleton, option_lock

try:
    import quecgnss
except ImportError:
    quecgnss = None

try:
    from wifilocator import wifilocator
except ImportError:
    wifilocator = None

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
        self.__gps_data = gps_data

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


class GPSPower:

    def __init__(self, PowerPin, StandbyPin, BackupPin):
        self.__PowerPin = PowerPin
        self.__StandbyPin = StandbyPin
        self.__BackupPin = BackupPin
        self.__gps_power_gpio = None
        self.__gps_standby_gpio = None
        self.__gps_backup_gpio = None

    def __power_control(self, method, onoff):
        if method == "power_switch":
            if self.__gps_power_gpio is None:
                self.__gps_power_gpio = Pin(self.__PowerPin, Pin.OUT, Pin.PULL_DISABLE, onoff)
            gpio_obj = self.__gps_power_gpio
        elif method == "standby":
            if self.__gps_standby_gpio is None:
                self.__gps_standby_gpio = Pin(self.__StandbyPin, Pin.OUT, Pin.PULL_DISABLE, onoff)
            gpio_obj = self.__gps_standby_gpio
        elif method == "backup":
            if self.__gps_backup_gpio is None:
                self.__gps_backup_gpio = Pin(self.__BackupPin, Pin.OUT, Pin.PULL_DISABLE, onoff)
            gpio_obj = self.__gps_backup_gpio
        else:
            return False

        if gpio_obj.read() != onoff:
            gpio_obj.write(onoff)
            utime.sleep_ms(50)
            if gpio_obj.read() != onoff:
                return False
        return True

    def power_switch(self, onoff):
        if self.__PowerPin is not None:
            return self.__power_control("power_switch", onoff)
        return False

    def backup(self, onoff):
        if self.__BackupPin is not None:
            return self.__power_control("backup", onoff)
        return False

    def standby(self, onoff):
        if self.__StandbyPin is not None:
            return self.__power_control("standby", onoff)
        return False


class GPS(GPSPower):

    __RMC = 0
    __GGA = 1
    __GSV = 2
    __GSA = 3
    __VTG = 4
    __GLL = 5

    class _gps_mode:
        none = 0x0
        internal = 0x1
        external = 0x2

    def __init__(self, UARTn, buadrate, databits, parity, stopbits, flowctl, gps_mode, nmea, PowerPin, StandbyPin, BackupPin):
        super().__init__(PowerPin, StandbyPin, BackupPin)
        self.__UARTn = UARTn
        self.__buadrate = buadrate
        self.__databits = databits
        self.__parity = parity
        self.__stopbits = stopbits
        self.__flowctl = flowctl
        self.__gps_mode = gps_mode
        self.__NMEA = nmea if nmea else 0b010111

        self.__external_obj = None
        self.__internal_obj = quecgnss
        self.__nmea_parse = NMEAParse()

        self.__external_retrieve_queue = None
        self.__queue_size = 2
        self.__first_break = 0
        self.__break = 0
        self.__gps_data = ""
        self.__rmc_data = ""
        self.__gga_data = ""
        self.__vtg_data = ""
        self.__gsv_data = ""

        self.__gps_timer = osTimer()
        self.__gps_data_check_timer = osTimer()

        if self.__gps_mode == self._gps_mode.external:
            self.__external_init()
        elif self.__gps_mode == self._gps_mode.internal:
            self.__internal_init()

    @option_lock(_gps_data_set_lock)
    def __set_gps_data(self, gps_data):
        self.__gps_data = gps_data

    @option_lock(_gps_data_set_lock)
    def __get_gps_data(self):
        return self.__gps_data

    def __reverse_gps_data(self, this_gps_data):
        log.debug("this_gps_data: \n%s" % this_gps_data)
        if this_gps_data:
            _gps_data = self.__get_gps_data()
            if _gps_data:
                _gps_data = CRLF.join(_gps_data.split(CRLF)[::-1])
            _gps_data += this_gps_data.strip().replace("\r", "").replace("\n", "").replace("$", CRLF + "$")
            _gps_data = CRLF.join(_gps_data.split(CRLF)[::-1])
            self.__set_gps_data(_gps_data)

    def __gps_timer_callback(self, args):
        self.__break = 1
        if self.__external_retrieve_queue is not None:
            self.__external_retrieve_queue.put(False)

    def __gps_data_check_callback(self, args):
        if not self.__check_gps_valid():
            self.__gps_nmea_data_clean()

    def __external_init(self):
        self.__external_retrieve_queue = Queue(maxsize=self.__queue_size)

    def __external_open(self):
        self.power_switch(1)
        self.__external_obj = UART(
            self.__UARTn,
            self.__buadrate,
            self.__databits,
            self.__parity,
            self.__stopbits,
            self.__flowctl
        )
        self.__external_obj.set_callback(self.__external_retrieve_cb)

    def __external_close(self):
        self.__external_obj.close()

    def __external_retrieve_cb(self, args):
        if self.__external_retrieve_queue.size() >= self.__queue_size:
            self.__external_retrieve_queue.get()
        self.__external_retrieve_queue.put(True)

    def __internal_init(self):
        if self.__internal_obj:
            if self.__internal_obj.init() != 0:
                log.error("GNSS INIT Failed.")
            else:
                log.debug("GNSS INIT Success.")
        else:
            log.error("Module quecgnss Import Error.")

    def __internal_open(self):
        return True if self.__internal_obj.gnssEnable(1) == 0 else False

    def __internal_close(self):
        return True if self.__internal_obj.gnssEnable(0) == 0 else False

    def __nmea_statement_exist(self, nmea_item):
        return (self.__NMEA & (0b1 << nmea_item)) >> nmea_item

    def __gps_nmea_data_clean(self):
        self.__set_gps_data("")
        self.__rmc_data = ""
        self.__gga_data = ""
        self.__gsv_data = ""
        self.__gsa_data = ""
        self.__vtg_data = ""
        self.__gll_data = ""

    def __check_gps_valid(self):
        self.__nmea_parse.set_gps_data(self.__get_gps_data())
        if not self.__rmc_data:
            self.__rmc_data = self.__nmea_parse.GxRMC
        _rmc_info = self.__nmea_parse.GxRMCData
        loc_status = _rmc_info[2] if _rmc_info else "V"

        if self.__rmc_data and loc_status == "A":
            if self.__nmea_statement_exist(self.__GGA) and not self.__gga_data:
                self.__gga_data = self.__nmea_parse.GxGGA
            if self.__nmea_statement_exist(self.__GSV) and not self.__gsv_data:
                self.__gsv_data = self.__nmea_parse.GxGSV
            if self.__nmea_statement_exist(self.__GSA) and not self.__gsa_data:
                self.__gsa_data = self.__nmea_parse.GxGSA
            if self.__nmea_statement_exist(self.__VTG) and not self.__vtg_data:
                self.__vtg_data = self.__nmea_parse.GxVTG
            if self.__nmea_statement_exist(self.__GLL) and not self.__gll_data:
                self.__gll_data = self.__nmea_parse.GxGLL

            if self.__nmea_statement_exist(self.__GGA) and not self.__gga_data:
                return False
            if self.__nmea_statement_exist(self.__GSV) and not self.__gsv_data:
                return False
            if self.__nmea_statement_exist(self.__GSA) and not self.__gsa_data:
                return False
            if self.__nmea_statement_exist(self.__VTG) and not self.__vtg_data:
                return False
            if self.__nmea_statement_exist(self.__GLL) and not self.__gll_data:
                return False
            return True

        return False

    def __external_read(self):
        self.__external_open()
        log.debug("__external_read start")

        while self.__break == 0:
            self.__gps_timer.start(50, 0, self.__gps_timer_callback)
            signal = self.__external_retrieve_queue.get()
            log.debug("[first] signal: %s" % signal)
            if signal:
                to_read = self.__external_obj.any()
                log.debug("[first] to_read: %s" % to_read)
                if to_read > 0:
                    self.__set_gps_data(self.__external_obj.read(to_read).decode())
            self.__gps_timer.stop()
        self.__break = 0

        self.__gps_nmea_data_clean()
        self.__gps_data_check_timer.start(2000, 1, self.__gps_data_check_callback)
        cycle = 0
        while self.__break == 0:
            self.__gps_timer.start(1500, 0, self.__gps_timer_callback)
            signal = self.__external_retrieve_queue.get()
            log.debug("[second] signal: %s" % signal)
            if signal:
                to_read = self.__external_obj.any()
                log.debug("[second] to_read: %s" % to_read)
                if to_read > 0:
                    self.__reverse_gps_data(self.__external_obj.read(to_read).decode())
                    if self.__check_gps_valid():
                        self.__break = 1

            self.__gps_timer.stop()
            cycle += 1
            if cycle >= self.__retry:
                self.__break = 1
            if self.__break != 1:
                utime.sleep(1)
        self.__gps_data_check_timer.stop()
        self.__break = 0

        # To check GPS data is usable or not.
        self.__gps_data_check_callback(None)
        self.__external_close()
        log.debug("__external_read %s." % ("success" if self.__get_gps_data() else "failed"))
        return self.__get_gps_data()

    def __internal_read(self):
        log.debug("__internal_read start.")
        self.__internal_open()

        while self.__break == 0:
            gnss_data = quecgnss.read(1024)
            if gnss_data[0] == 0:
                self.__break = 1
        self.__break = 0

        self.__gps_nmea_data_clean()
        self.__gps_data_check_timer.start(2000, 1, self.__gps_data_check_callback)
        cycle = 0
        while self.__break == 0:
            gnss_data = quecgnss.read(1024)
            if gnss_data and gnss_data[1]:
                this_gps_data = gnss_data[1].decode() if len(gnss_data) > 1 and gnss_data[1] else ""
                self.__reverse_gps_data(this_gps_data)
                if self.__check_gps_valid():
                    self.__break = 1
            cycle += 1
            if cycle >= self.__retry:
                if self.__break != 1:
                    self.__break = 1
            if self.__break != 1:
                utime.sleep(1)
        self.__gps_data_check_timer.stop()
        self.__break = 0

        self.__gps_data_check_callback(None)
        self.__internal_close()
        log.debug("__internal_read %s." % ("success" if self.__get_gps_data() else "failed"))
        return self.__get_gps_data()

    def read(self, retry=30):
        self.__retry = retry
        gps_data = ""
        if self.__gps_mode == self._gps_mode.external:
            gps_data = self.__external_read()
        elif self.__gps_mode == self._gps_mode.internal:
            gps_data = self.__internal_read()

        res = 0 if gps_data else -1
        return (res, gps_data)


class CellLocator(object):
    """This class is for reading cell location data"""

    def __init__(self, serverAddr, port, token, timeout, profileIdx):
        self.__serverAddr = serverAddr
        self.__port = port
        self.__token = token
        self.__timeout = timeout
        self.__profileIdx = profileIdx

    def read(self):
        read_loc_res = self.__read_loc()
        read_cell_res = self.__read_cell()
        res = 0 if read_loc_res[0] == 0 or read_cell_res[0] == 0 else -1
        return (res, read_loc_res[1], read_cell_res[1])

    def __read_loc(self):
        """Read cell location data.

        Return: (res_code, loc_data)
            res_code:
                -  0: Success
                - -1: Initialization failed
                - -2: The server address is too long (more than 255 bytes)
                - -3: Wrong key length, must be 16 bytes
                - -4: The timeout period is out of range, the supported range is (1 ~ 300) s
                - -5: The specified PDP network is not connected, please confirm whether the PDP is correct
                - -6: Error getting coordinates
            loc_data:
                (117.1138, 31.82279, 550)
        """
        res = -1
        loc_data = cellLocator.getLocation(
            self.__serverAddr,
            self.__port,
            self.__token,
            self.__timeout,
            self.__profileIdx
        )
        if isinstance(loc_data, tuple) and len(loc_data) == 3:
            res = 0
        else:
            res = loc_data
            loc_data = ()

        return (res, loc_data)

    def __read_cell(self):
        res = -1
        near_cell = []
        server_cell = []

        near_cells = net.getCi()
        if near_cells != -1 and isinstance(near_cells, list):
            near_cell = list(map(str, near_cells))

        server_cells = net.getCellInfo()
        if server_cells != -1 and isinstance(server_cells, tuple):
            server_cell = server_cells

        res = 0 if near_cell or server_cell else -1
        return (res, {"near_cell": near_cell, "server_cell": server_cell})


class WiFiLocator(object):
    """This class is for reading wifi location data"""

    def __init__(self, token):
        self.__wifilocator_obj = wifilocator(token)

    def read(self):
        read_loc_res = self.__read_loc()
        read_mac_res = self.__read_mac()
        res = 0 if read_loc_res[0] == 0 or read_mac_res[0] == 0 else -1
        return (res, read_loc_res[1], read_mac_res[1])

    def __read_loc(self):
        """Read wifi location data.

        Return: (res_code, loc_data)
            res_code:
                -  0: Success
                - -1: The current network is abnormal, please confirm whether the dial-up is normal
                - -2: Wrong key length, must be 16 bytes
                - -3: Error getting coordinates
            loc_data:
                (117.1138, 31.82279, 550)
        """
        res = -1
        loc_data = self.__wifilocator_obj.getwifilocator()
        if isinstance(loc_data, tuple) and len(loc_data) == 3:
            res = 0
        else:
            res = loc_data
            loc_data = ()

        return (res, loc_data)

    def __read_mac(self):
        res = -1
        macs = []
        if wifiScan.support():
            if wifiScan.control(1) == 0:
                if wifiScan.getState():
                    wifisacn_start = wifiScan.start()
                    if wifisacn_start != -1 and wifisacn_start[0] > 0:
                        macs = [i[0] for i in wifisacn_start[1]]
                        res = 0
            wifiScan.control(0)
        return (res, macs)


class Location(Singleton):
    """This class is for reading location data from gps, cell, wifi"""
    gps = None
    cellLoc = None
    wifiLoc = None

    class _loc_method(object):
        gps = 0x1
        cell = 0x2
        wifi = 0x4

    def __init__(self, loc_method, locator_init_params):
        """Init Location module

        1. If loc_method include gps then init gps module;
        2. If loc_method inculde cell then init cell module;
        3. If loc_method Include wifi then init wifi module;

        Args:
            loc_method(int):
                1 - gps
                2 - cell
                3 - cell & gps
                4 - wifi
                5 - wifi & gps
                6 - wifi & cell
                7 - wifi & cell & gps
            locator_init_params(dict):
                gps_cfg(dict):GPS module init args
                cell_cfg(dict):CELL module init args
                wifi_cfg(dict):WIFI module init args
        """
        self.__loc_method = loc_method
        self.__locator_init_params = locator_init_params
        self.__locater_init()

    def __locater_init(self):
        """Init gps, cell, wifi by loc_method"""

        if self.__loc_method & self._loc_method.gps:
            if self.gps is None:
                _gps_cfg = self.__locator_init_params.get("gps_cfg", {})
                if _gps_cfg:
                    self.gps = GPS(**_gps_cfg)
                else:
                    raise ValueError("Invalid gps init parameters.")
        else:
            self.gps = None

        if self.__loc_method & self._loc_method.cell:
            if self.cellLoc is None:
                _cell_cfg = self.__locator_init_params.get("cell_cfg")
                if _cell_cfg:
                    self.cellLoc = CellLocator(**_cell_cfg)
                else:
                    raise ValueError("Invalid cell-locator init parameters.")
        else:
            self.cellLoc = None

        if self.__loc_method & self._loc_method.wifi:
            if self.wifiLoc is None:
                _wifi_cfg = self.__locator_init_params.get("wifi_cfg")
                if _wifi_cfg:
                    self.wifiLoc = WiFiLocator(**_wifi_cfg)
                else:
                    raise ValueError("Invalid wifi-locator init parameters.")
        else:
            self.wifiLoc = None

    def __read_gps(self, retry):
        """Read loction data from gps module

        Return:
            $GPTXT,01,01,02,ANTSTATUS=OPEN*2B
            $GNRMC,073144.000,A,3149.330773,N,11706.946971,E,0.00,337.47,150422,,,D,V*07
            $GNVTG,337.47,T,,M,0.00,N,0.00,K,D*22
            $GNGGA,073144.000,3149.330773,N,11706.946971,E,2,19,0.66,85.161,M,-0.335,M,,*56
            $GNGSA,A,3,01,195,06,03,21,194,19,17,30,14,,,0.94,0.66,0.66,1*02
            $GNGSA,A,3,13,26,07,10,24,25,08,03,22,,,,0.94,0.66,0.66,4*03
            $GPGSV,3,1,12,14,84,210,31,195,67,057,46,17,52,328,28,50,51,161,33,1*54
            $GPGSV,3,2,12,194,49,157,33,03,48,090,37,19,36,305,32,06,34,242,32,1*58
            $GPGSV,3,3,12,01,32,041,35,30,17,204,22,21,07,051,13,07,03,183,,1*6B
            $BDGSV,5,1,18,07,86,063,30,10,75,322,30,08,60,211,34,03,52,192,33,1*71
            $BDGSV,5,2,18,24,44,276,33,13,43,215,33,01,43,135,30,26,40,208,37,1*71
            $BDGSV,5,3,18,02,38,230,,04,32,119,,22,26,135,30,19,25,076,,1*70
            $BDGSV,5,4,18,05,17,251,,25,06,322,27,09,02,211,22,21,02,179,,1*78
            $BDGSV,5,5,18,29,02,075,,20,01,035,,1*72
            $GNGLL,3149.330773,N,11706.946971,E,073144.000,A,D*4E
        """
        return self.gps.read(retry) if self.gps else ""

    def __read_cell(self):
        """Read loction data from cell module

        Return:
            (117.1138, 31.82279, 550) or ()
        """
        if self.cellLoc:
            cell_loc_data = self.cellLoc.read()
            return (cell_loc_data[1], cell_loc_data[2])
        return ()

    def __read_wifi(self):
        """Read loction data from wifi module

        Return:
            (117.1138, 31.82279, 550) or ()
        """
        if self.wifiLoc:
            wifi_loc_data = self.wifiLoc.read()
            return (wifi_loc_data[1], wifi_loc_data[2])
        return ()

    def read(self, retry=30):
        """Read location data

        args:
            retry(int): gps read uart data retry count.

        Returns:
            dict:
                key:
                    1 - GPS data
                    2 - CELL data
                    4 - WIFI data
            .e.g:
            {
                1: "$GPGGA,XXX",
                2: (0.00, 0.00, 0.00),
                4: (0.00, 0.00, 0.00),
            }
        """
        loc_data = {}

        if self.__loc_method & self._loc_method.gps:
            loc_data[self._loc_method.gps] = self.__read_gps(retry)

        if self.__loc_method & self._loc_method.cell:
            loc_data[self._loc_method.cell] = self.__read_cell()

        if self.__loc_method & self._loc_method.wifi:
            loc_data[self._loc_method.wifi] = self.__read_wifi()

        return loc_data
