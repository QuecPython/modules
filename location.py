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
import math
import utime
import osTimer
import _thread
import wifiScan
import cellLocator

from queue import Queue
from machine import UART, Pin
try:
    from wifilocator import wifilocator
except:
    wifilocator = None

from usr.modules.logging import getLogger
from usr.modules.common import Singleton, option_lock

try:
    import quecgnss
except ImportError:
    quecgnss = None

log = getLogger(__name__)

_gps_read_lock = _thread.allocate_lock()
_gps_data_set_lock = _thread.allocate_lock()

EE = 0.00669342162296594323
EARTH_RADIUS = 6378.137  # Approximate Earth Radius(km)
M_PI = math.pi


class _loc_method(object):
    gps = 0x1
    cell = 0x2
    wifi = 0x4


class _gps_mode(object):
    none = 0x0
    internal = 0x1
    external = 0x2


def transformLat(x, y):
    ret = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * math.sqrt(math.fabs(x))
    ret += (20.0 * math.sin(6.0 * x * M_PI) + 20.0 * math.sin(2.0 * x * M_PI)) * 2.0 / 3.0
    ret += (20.0 * math.sin(y * M_PI) + 40.0 * math.sin(y / 3.0 * M_PI)) * 2.0 / 3.0
    ret += (160.0 * math.sin(y / 12.0 * M_PI) + 320 * math.sin(y * M_PI / 30.0)) * 2.0 / 3.0
    return ret


def transformLon(x, y):
    ret = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * math.sqrt(math.fabs(x))
    ret += (20.0 * math.sin(6.0 * x * M_PI) + 20.0 * math.sin(2.0 * x * M_PI)) * 2.0 / 3.0
    ret += (20.0 * math.sin(x * M_PI) + 40.0 * math.sin(x / 3.0 * M_PI)) * 2.0 / 3.0
    ret += (150.0 * math.sin(x / 12.0 * M_PI) + 300.0 * math.sin(x / 30.0 * M_PI)) * 2.0 / 3.0
    return ret


def WGS84ToGCJ02(lon, lat):
    dLat = transformLat(lon - 105.0, lat - 35.0)
    dLon = transformLon(lon - 105.0, lat - 35.0)
    radLat = lat / 180.0 * M_PI
    magic = math.sin(radLat)
    magic = 1 - magic * magic * EE
    sqrtMagic = math.sqrt(magic)

    dLat = (dLat * 180.0) / ((EARTH_RADIUS * 1000 * (1 - EE)) / (magic * sqrtMagic) * M_PI)
    dLon = (dLon * 180.0) / (EARTH_RADIUS * 1000 / sqrtMagic * math.cos(radLat) * M_PI)
    lon02 = lon + dLon
    lat02 = lat + dLat

    return lon02, lat02


class GPSMatch(object):
    """This class is match gps NEMA 0183"""

    def GxRMC(self, gps_data):
        """Match Recommended Minimum Specific GPS/TRANSIT Data（RMC）

        Args:
            gps_data(str): GPS NMEA string.

        Returns:
            str: RMC NMEA string.
        """
        if gps_data:
            rmc_re = ure.search(
                r"\$G[NP]RMC,\d*\.*\d*,*[AV],*\d*\.*\d*,*[NS],*\d*\.*\d*,*[EW],*\d*\.*\d*,*\d*\.*\d*,*\d*,*\d*\.*\d*,*[EW]*,*[ADEN]*,*[SCUV]*\**(\d|\w)*",
                gps_data)
            if rmc_re:
                return rmc_re.group(0)
        return ""

    def GxGGA(self, gps_data):
        """Match Global Positioning System Fix Data（GGA）

        Args:
            gps_data(str): GPS NMEA string.

        Returns:
            str: GGA NMEA string.
        """
        if gps_data:
            gga_re = ure.search(
                r"\$G[BLPN]GGA,\d*\.*\d*,*\d*\.*\d*,*[NS],*\d*\.*\d*,*[EW],*[0126],*\d*,*\d*\.*\d*,*-*\d*\.*\d*,*M,*-*\d*\.*\d*,*M,*\d*,*\**(\d|\w)*",
                gps_data)
            if gga_re:
                return gga_re.group(0)
        return ""

    def GxVTG(self, gps_data):
        """Match Track Made Good and Ground Speed（VTG）

        Args:
            gps_data(str): GPS NMEA string.

        Returns:
            str: VTG NMEA string.
        """
        if gps_data:
            vtg_re = ure.search(r"\$G[NP]VTG,\d*\.*\d*,*T,*\d*\.*\d*,*M,*\d*\.*\d*,*N,*\d*\.*\d*,*K,*[ADEN]*\*(\d|\w)*", gps_data)
            if vtg_re:
                return vtg_re.group(0)
        return ""

    def GxGSV(self, gps_data):
        """Mactch GPS Satellites in View（GSV）

        Args:
            gps_data(str): GPS NMEA string.

        Returns:
            str: GSV NMEA string.
        """
        if gps_data:
            gsv_re = ure.search(r"\$G[NP]GSV,\d*,*\d*,*\d*,*\d*,*\d*,*\d*,*\d*,*\d*,*\d*,*\d*,*\d*,*\d*,*\d*,*\d*,*\d*,*\d*,*\d*,*\d*,*\d*,*\d*\**(\d|\w)*", gps_data)
            if gsv_re:
                return gsv_re.group(0)
        return ""

    def GxGLL(self, gps_data):
        """Geographic Position

        Args:
            gps_data(str): GPS NMEA string.

        Returns:
            str: GLL NMEA string.
        """
        if gps_data:
            gll_re = ure.search(r"\$G[NP]GLL,\d*\.*\d*,*[NS]*,*\d*\.*\d*,*[EW]*,*\d*\.*\d*,*[AV]*,*[ADEN]*\**(\d|\w)*", gps_data)
            if gll_re:
                return gll_re.group(0)

    def GxGSA(self, gps_data):
        """GNSS DOP and Active Satellites

        Args:
            gps_data(str): GPS NMEA string.

        Returns:
            str: GSA NMEA string.
        """
        if gps_data:
            gsa_re = ure.search(r"\$G[NP]GSA,[MA]*,*[123]*,*\d*,*\d*,*\d*,*\d*,*\d*,*\d*,*\d*,*\d*,*\d*,*\d*,*\d*,*\d*,*\d*\.*\d*,*\d*\.*\d*,*\d*\.*\d*,*(\d|\w)*\**(\d|\w)*", gps_data)
            if gsa_re:
                return gsa_re.group(0)


class GPSParse(object):
    """Parse details from gps data"""

    def GxGGA_satellite_num(self, gga_data):
        """Parse satellite num from GGA"""
        if gga_data:
            satellite_num_re = ure.search(r",[EW],[0126],\d+,", gga_data)
            if satellite_num_re:
                return satellite_num_re.group(0).split(",")[-2]
        return ""

    def GxGGA_latitude(self, gga_data):
        """Parse latitude from GGA"""
        if gga_data:
            latitude_re = ure.search(r",[0-9]+\.[0-9]+,[NS],", gga_data)
            if latitude_re:
                latitude = latitude_re.group(0)[1:-3]
                return str(float(latitude[:2]) + float(latitude[2:]) / 60)
        return ""

    def GxGGA_longitude(self, gga_data):
        """Parse longitude from GGA"""
        if gga_data:
            longitude_re = ure.search(r",[0-9]+\.[0-9]+,[EW],", gga_data)
            if longitude_re:
                longitude = longitude_re.group(0)[1:-3]
                return str(float(longitude[:3]) + float(longitude[3:]) / 60)
        return ""

    def GxGGA_altitude(self, gga_data):
        """Parse altitude from GGA"""
        if gga_data:
            altitude_re = ure.search(r",-*[0-9]+\.[0-9]+,M,", gga_data)
            if altitude_re:
                return altitude_re.group(0)[1:-3]
        return ""

    def GxVTG_speed(self, vtg_data):
        """Parse speed from VTG"""
        if vtg_data:
            speed_re = ure.search(r",N,\d+\.\d+,K,", vtg_data)
            if speed_re:
                return speed_re.group(0)[3:-3]
        return ""

    def GxGSV_satellite_num(self, gsv_data):
        """Parse satellite num from GSV"""
        if gsv_data:
            satellite_num_re = ure.search(r"\$G[NP]GSV,\d+,\d+,\d+,", gsv_data)
            if satellite_num_re:
                return satellite_num_re.group(0).split(",")[-2]
        return ""

    def GxRMC_loc_status(self, rmc_data):
        if rmc_data:
            loc_status_re = ure.search(r"\$G[NP]RMC,\d*\.*\d*,[AV],", rmc_data)
            if loc_status_re:
                loc_status = loc_status_re.group(0).split(",")[-2]
                return True if loc_status == "A" else False
        return False

    def __nmea_parse(self, nmea):
        return tuple(nmea[1:].split("*")[0].split(",")) if nmea else ()

    def GxRMC(self, rmc_data):
        return self.__nmea_parse(rmc_data)

    def GxGGA(self, gga_data):
        return self.__nmea_parse(gga_data)

    def GxGSV(self, gsv_data):
        return self.__nmea_parse(gsv_data)

    def GxGSA(self, gsa_data):
        return self.__nmea_parse(gsa_data)

    def GxVTG(self, vtg_data):
        return self.__nmea_parse(vtg_data)

    def GxGLL(self, gll_data):
        return self.__nmea_parse(gll_data)


class GPS(Singleton):
    """This class if for reading gps data.

    Now support external gps and internal gps.

    Sleep power consumption:
        power off < backup < standby
    """

    __RMC = 0
    __GGA = 1
    __GSV = 2
    __GSA = 3
    __VTG = 4
    __GLL = 5
    __NMEA = 0b010111

    def __init__(self, UARTn, buadrate, databits, parity, stopbits, flowctl, PowerPin, StandbyPin, BackupPin, gps_mode):
        """Init GPS module

        [description]

        Args:
            UARTn(int): UART No.
            buadrate(int): baud rate
            databits(int): data bits (5 ~ 8)
            parity(int): parity (0 – NONE，1 – EVEN，2 - ODD)
            stopbits(int): stop bit
            flowctl(int): hardware control flow (0 – FC_NONE， 1 – FC_HW)
            PowerPin(int): Power GIPO Pin
            StandbyPin(int): Standby GPIO Pin
            BackupPin(int): Back GPIO Pin
            gps_mode(int): GPS mode
                0 - None
                1 - internal GPS
                2 - external GPS
        """
        self.__UARTn = UARTn
        self.__buadrate = buadrate
        self.__databits = databits
        self.__parity = parity
        self.__stopbits = stopbits
        self.__flowctl = flowctl
        self.__PowerPin = PowerPin
        self.__StandbyPin = StandbyPin
        self.__BackupPin = BackupPin
        self.__gps_mode = gps_mode

        self.__external_obj = None
        self.__internal_obj = quecgnss
        self.__gps_match = GPSMatch()
        self.__gps_parse = GPSParse()
        self.__gps_power_gpio = None
        self.__gps_standby_gpio = None
        self.__gps_backup_gpio = None

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

        if self.__gps_mode & _gps_mode.external:
            self.__external_init()
        elif self.__gps_mode & _gps_mode.internal:
            self.__internal_init()

    def __gps_power_control(self, GPIOn, onoff, method):
        if method == "power_switch":
            if self.__gps_power_gpio is None:
                self.__gps_power_gpio = Pin(GPIOn, Pin.OUT, Pin.PULL_DISABLE, onoff)
            gpio_obj = self.__gps_power_gpio
        elif method == "standby":
            if self.__gps_standby_gpio is None:
                self.__gps_standby_gpio = Pin(GPIOn, Pin.OUT, Pin.PULL_DISABLE, onoff)
            gpio_obj = self.__gps_standby_gpio
        elif method == "backup":
            if self.__gps_backup_gpio is None:
                self.__gps_backup_gpio = Pin(GPIOn, Pin.OUT, Pin.PULL_DISABLE, onoff)
            gpio_obj = self.__gps_backup_gpio
        else:
            raise TypeError("Param method %s is not compare." % method)

        if gpio_obj.read() != onoff:
            gpio_obj.write(onoff)
            if gpio_obj.read() != onoff:
                return False
        return True

    def __reverse_gps_data(self, this_gps_data):
        """Reverse GPS data for regular match get the latest data"""
        log.debug("this_gps_data: \n%s" % this_gps_data)
        delimiter = "\r\n"
        if this_gps_data:
            _gps_data = self.__get_gps_data()
            if _gps_data:
                _gps_data = delimiter.join(_gps_data.split(delimiter)[::-1])
            _gps_data += this_gps_data.strip().replace("\r", "").replace("\n", "").replace("$", delimiter + "$")
            _gps_data = delimiter.join(_gps_data.split(delimiter)[::-1])
            self.__set_gps_data(_gps_data)

    def __read_latitude(self, gps_data):
        """Read latitude from gps data"""
        return self.__gps_parse.GxGGA_latitude(self.__gps_match.GxGGA(gps_data))

    def __read_longitude(self, gps_data):
        """Read longitude from gps data"""
        return self.__gps_parse.GxGGA_longitude(self.__gps_match.GxGGA(gps_data))

    def __read_altitude(self, gps_data):
        """Read altitude from gps data"""
        return self.__gps_parse.GxGGA_altitude(self.__gps_match.GxGGA(gps_data))

    @option_lock(_gps_data_set_lock)
    def __set_gps_data(self, gps_data):
        self.__gps_data = gps_data

    @option_lock(_gps_data_set_lock)
    def __get_gps_data(self):
        return self.__gps_data

    def __gps_timer_callback(self, args):
        """GPS read timer callback
        When over time to get uart data, break queue wait
        """
        self.__break = 1
        if self.__external_retrieve_queue is not None:
            self.__external_retrieve_queue.put(False)

    def __gps_data_check_callback(self, args):
        """GPS read old data clean timer callback
        When GPS read over time, clean old gps data, wait to read new gps data.
        """
        clean = False
        if "" in (self.__rmc_data, self.__gga_data, self.__gsv_data):
            clean = True
        else:
            if self.__nmea_statement_exist(self.__GSA) and not self.__gsa_data:
                clean = True
            elif self.__nmea_statement_exist(self.__VTG) and not self.__vtg_data:
                clean = True
            elif self.__nmea_statement_exist(self.__GLL) and not self.__gll_data:
                clean = True

        if clean:
            self.__gps_nmea_data_clean()

    def __external_init(self):
        """External GPS init"""
        self.__external_retrieve_queue = Queue(maxsize=self.__queue_size)

    def __external_open(self):
        """External GPS start, UART init"""
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
        """External GPS close, UART close, NOT GPS stop"""
        self.__external_obj.close()

    def __external_retrieve_cb(self, args):
        """
        GPS data retrieve callback from UART
        When data comes, send a message to queue of data length
        """
        # log.debug("GPS __external_retrieve_cb args: %s" % str(args))
        if self.__external_retrieve_queue.size() >= self.__queue_size:
            self.__external_retrieve_queue.get()
        self.__external_retrieve_queue.put(True)

    def __internal_init(self):
        """Internal GPS init"""
        if self.__internal_obj:
            if self.__internal_obj.init() != 0:
                self.__internal_open()
                log.error("GNSS INIT Failed.")
            else:
                log.debug("GNSS INIT Success.")
        else:
            log.error("Module quecgnss Import Error.")

    def __internal_open(self):
        """Internal GPS enable"""
        if self.__internal_obj.get_state() == 0:
            return True if self.__internal_obj.gnssEnable(1) == 0 else False
        else:
            return True

    def __internal_close(self):
        """Internal GPS close"""
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

    def __check_gps_valid(self, gps_data):
        self.__reverse_gps_data(gps_data)

        if not self.__rmc_data:
            self.__rmc_data = self.__gps_match.GxRMC(self.__get_gps_data())
        loc_status = self.__gps_parse.GxRMC_loc_status(self.__rmc_data)

        if self.__rmc_data and loc_status:
            if self.__nmea_statement_exist(self.__GGA) and not self.__gga_data:
                self.__gga_data = self.__gps_match.GxGGA(self.__get_gps_data())
            if self.__nmea_statement_exist(self.__GSV) and not self.__gsv_data:
                self.__gsv_data = self.__gps_match.GxGSV(self.__get_gps_data())
            if self.__nmea_statement_exist(self.__GSA) and not self.__gsa_data:
                self.__gsa_data = self.__gps_match.GxGSA(self.__get_gps_data())
            if self.__nmea_statement_exist(self.__VTG) and not self.__vtg_data:
                self.__vtg_data = self.__gps_match.GxVTG(self.__get_gps_data())
            if self.__nmea_statement_exist(self.__GLL) and not self.__gll_data:
                self.__gll_data = self.__gps_match.GxGLL(self.__get_gps_data())

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

    @option_lock(_gps_read_lock)
    def __external_read(self):
        """Read external GPS data

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
                    if self.__check_gps_valid(self.__external_obj.read(to_read).decode()):
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
        log.debug("__external_read data: %s" % self.__get_gps_data())
        return self.__get_gps_data()

    @option_lock(_gps_read_lock)
    def __internal_read(self):
        log.debug("__internal_read start.")
        """Read internal GPS data

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
                _gps_valid = self.__check_gps_valid(this_gps_data)
                log.debug("_gps_valid: %s" % _gps_valid)
                if _gps_valid:
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
        return self.__get_gps_data()

    def read(self, retry=30):
        """For user to read gps data

        Return: (res_code, gps_data)
            res_code:
                -  0: Success
                - -1: Failed
            gps_data:
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
        self.__retry = retry
        gps_data = ""
        if self.__gps_mode & _gps_mode.external:
            gps_data = self.__external_read()
        elif self.__gps_mode & _gps_mode.internal:
            gps_data = self.__internal_read()

        res = 0 if gps_data else -1
        return (res, gps_data)

    def read_coordinates(self, gps_data):
        """Read positioning coordinates.

        Params:
            gps_data: read gps data.
            map_coordinate_system: `WGS84` or GCJ02

        Return:
            (longitude, latitude, altitude)
        """
        latitude = self.__read_latitude(gps_data)
        latitude = float(latitude) if latitude else latitude
        longitude = self.__read_longitude(gps_data)
        longitude = float(longitude) if longitude else longitude
        altitude = self.__read_altitude(gps_data)
        altitude = float(altitude) if altitude else altitude
        return (longitude, latitude, altitude)

    def power_switch(self, onoff):
        """GPS module power switch

        Params:
            onoff: 0 -- off, 1 -- on
        """
        if self.__gps_mode & _gps_mode.external:
            if self.__PowerPin is not None:
                return self.__gps_power_control(self.__PowerPin, onoff, "power_switch")
            else:
                return False
        elif self.__gps_mode & _gps_mode.internal:
            # TODO: Interal GNSS power down will not be used this api.
            if onoff == 0:
                return self.__internal_close()
            else:
                return self.__internal_open()

    def backup(self, onoff):
        """GPS module low enery mode backup

        Params:
            onoff: 0 -- off, 1 -- on
        """
        if self.__BackupPin is not None:
            return self.__gps_power_control(self.__BackupPin, onoff, "backup")
        else:
            return False

    def standby(self, onoff):
        """GPS module low enery mode standby

        Params:
            onoff: 0 -- off, 1 -- on
        """
        if self.__StandbyPin is not None:
            return self.__gps_power_control(self.__StandbyPin, onoff, "standby")
        else:
            return False

    def set_nmea_statement(self, nmea_statement):
        """Set NMEA statement to check gps info valid

        RMC, GGA, GSV must be required.

        Args:
            nmea_statement(int):
                RMC - 0b1 << 0 (bit0), 0 - off, 1 - on
                GGA - 0b1 << 1 (bit1), 0 - off, 1 - on
                GSV - 0b1 << 2 (bit2), 0 - off, 1 - on
                GSA - 0b1 << 3 (bit3), 0 - off, 1 - on
                VTG - 0b1 << 4 (bit4), 0 - off, 1 - on
                GLL - 0b1 << 5 (bit5), 0 - off, 1 - on

        Returns:
            bool: True - success, False - falied.
        """
        if nmea_statement >= 0b111:
            self.__NMEA = nmea_statement
            return True
        return False


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

        if self.__loc_method & _loc_method.gps:
            if self.gps is None:
                _gps_cfg = self.__locator_init_params.get("gps_cfg", {})
                if _gps_cfg:
                    self.gps = GPS(**_gps_cfg)
                    if _gps_cfg.get("nmea_cfg") is not None:
                        self.gps.set_nmea_statement(_gps_cfg.get("nmea_cfg"))
                else:
                    raise ValueError("Invalid gps init parameters.")
        else:
            self.gps = None

        if self.__loc_method & _loc_method.cell:
            if self.cellLoc is None:
                _cell_cfg = self.__locator_init_params.get("cell_cfg")
                if _cell_cfg:
                    self.cellLoc = CellLocator(**_cell_cfg)
                else:
                    raise ValueError("Invalid cell-locator init parameters.")
        else:
            self.cellLoc = None

        if self.__loc_method & _loc_method.wifi:
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
        if self.gps:
            return self.gps.read(retry)[1]
        return ""

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

        if self.__loc_method & _loc_method.gps:
            loc_data[_loc_method.gps] = self.__read_gps(retry)

        if self.__loc_method & _loc_method.cell:
            loc_data[_loc_method.cell] = self.__read_cell()

        if self.__loc_method & _loc_method.wifi:
            loc_data[_loc_method.wifi] = self.__read_wifi()

        return loc_data

    def wgs84togcj02(self, Longitude, Latitude):
        return WGS84ToGCJ02(Longitude, Latitude)
