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
@file      :battery.py
@author    :Jack Sun (jack.sun@quectel.com)
@brief     :Battery management.
@version   :1.2.0
@date      :2022-11-24 17:06:30
@copyright :Copyright (c) 2022
"""

import utime
from misc import Power, ADC, USB
from machine import Pin, ExtInt
try:
    from modules.logging import getLogger
except ImportError:
    from usr.modules.logging import getLogger

log = getLogger(__name__)

BATTERY_OCV_TABLE = {
    "nix_coy_mnzo2": {
        55: {
            4152: 100, 4083: 95, 4023: 90, 3967: 85, 3915: 80, 3864: 75, 3816: 70, 3773: 65, 3737: 60, 3685: 55,
            3656: 50, 3638: 45, 3625: 40, 3612: 35, 3596: 30, 3564: 25, 3534: 20, 3492: 15, 3457: 10, 3410: 5, 3380: 0,
        },
        20: {
            4143: 100, 4079: 95, 4023: 90, 3972: 85, 3923: 80, 3876: 75, 3831: 70, 3790: 65, 3754: 60, 3720: 55,
            3680: 50, 3652: 45, 3634: 40, 3621: 35, 3608: 30, 3595: 25, 3579: 20, 3548: 15, 3511: 10, 3468: 5, 3430: 0,
        },
        0: {
            4147: 100, 4089: 95, 4038: 90, 3990: 85, 3944: 80, 3899: 75, 3853: 70, 3811: 65, 3774: 60, 3741: 55,
            3708: 50, 3675: 45, 3651: 40, 3633: 35, 3620: 30, 3608: 25, 3597: 20, 3585: 15, 3571: 10, 3550: 5, 3500: 0,
        },
    },
}


class Battery(object):
    """This class is for battery info.

    This class can get battery voltage and energy.
    if adc_args is not None, use cbc to read battery

    Args:
        adc_args(tuple): (adc_num, adc_period, factor)
            adc_num: ADC channel num
            adc_period: Cyclic read ADC cycle period
            factor: calculation coefficient
        chrg_gpion(int): CHRG GPIOn
        stdby_gpion(int): STDBY GPIOn
        battery_ocv(str): Battery OCV name
    """
    def __init__(self, adc_args=None, chrg_gpion=None, stdby_gpion=None, battery_ocv="nix_coy_mnzo2"):
        self.__energy = 100
        self.__temp = 20

        # ADC params
        self.__adc = None
        if adc_args:
            self.__adc_num, self.__adc_period, self.__factor = adc_args
            if not isinstance(self.__adc_num, int):
                raise TypeError("adc_args adc_num is not int number.")
            if not isinstance(self.__adc_period, int):
                raise TypeError("adc_args adc_period is not int number.")
            if not isinstance(self.__factor, float):
                raise TypeError("adc_args factor is not int float.")
            self.__adc = ADC()

        # Charge params
        self.__charge_callback = None
        self.__charge_status = None
        self.__chrg_gpion = chrg_gpion
        self.__stdby_gpion = stdby_gpion
        self.__chrg_gpio = None
        self.__stdby_gpio = None
        self.__chrg_exint = None
        self.__stdby_exint = None
        self.__usb = None
        if self.__chrg_gpion is not None and self.__stdby_gpion is not None:
            self.__init_charge()
        else:
            self.__usb = USB()

        if not BATTERY_OCV_TABLE.get(battery_ocv):
            raise TypeError("Battery OCV %s is not support." % battery_ocv)
        self.__battery_ocv = battery_ocv

    def __chrg_callback(self, args):
        """Charge status change callback"""
        self.__update_charge_status()
        if callable(self.__charge_callback):
            self.__charge_callback(self.__charge_status)

    def __stdby_callback(self, args):
        """Charge status change callback"""
        self.__update_charge_status()
        if callable(self.__charge_callback):
            self.__charge_callback(self.__charge_status)

    def __usb_callback(self, args):
        self.__update_charge_status()
        if callable(self.__charge_callback):
            self.__charge_callback(self.__charge_status)

    def __update_charge_status(self):
        """Update Charge status by gpio status"""
        if not self.__usb:
            chrg_level = self.__chrg_gpio.read()
            stdby_level = self.__stdby_gpio.read()
            if chrg_level == 1 and stdby_level == 1:
                # Not charge.
                self.__charge_status = 0
            elif chrg_level == 0 and stdby_level == 1:
                # Charging.
                self.__charge_status = 1
            elif chrg_level == 1 and stdby_level == 0:
                # Charge over.
                self.__charge_status = 2
            else:
                raise TypeError("CHRG and STDBY cannot be 0 at the same time!")
        else:
            self.__usb_charge()

    def __init_charge(self):
        """Init charge Pin and ExtInt"""
        self.__chrg_gpio = Pin(self.__chrg_gpion, Pin.IN, Pin.PULL_PU)
        self.__stdby_gpio = Pin(self.__stdby_gpion, Pin.IN, Pin.PULL_PU)
        self.__chrg_exint = ExtInt(self.__chrg_gpion, ExtInt.IRQ_RISING_FALLING, ExtInt.PULL_PU, self.__chrg_callback)
        self.__stdby_exint = ExtInt(self.__stdby_gpion, ExtInt.IRQ_RISING_FALLING, ExtInt.PULL_PU, self.__stdby_callback)
        self.__chrg_exint.enable()
        self.__stdby_exint.enable()
        self.__update_charge_status()

    def __usb_charge(self):
        _cs = self.__usb.getStatus()
        self.__charge_status = _cs

    def __get_soc_from_dict(self, key, volt_arg):
        """Get battery energy from map"""
        if BATTERY_OCV_TABLE[self.__battery_ocv].get(key):
            volts = sorted(BATTERY_OCV_TABLE[self.__battery_ocv][key].keys(), reverse=True)
            pre_volt = 0
            volt_not_under = 0  # Determine whether the voltage is lower than the minimum voltage value of soc.
            for volt in volts:
                if volt_arg > volt:
                    volt_not_under = 1
                    soc1 = BATTERY_OCV_TABLE[self.__battery_ocv][key].get(volt, 0)
                    soc2 = BATTERY_OCV_TABLE[self.__battery_ocv][key].get(pre_volt, 0)
                    break
                else:
                    pre_volt = volt
            if pre_volt == 0:  # Input Voltarg > Highest Voltarg
                return soc1
            elif volt_not_under == 0:
                return 0
            else:
                return soc2 - (soc2 - soc1) * (pre_volt - volt_arg) // (pre_volt - volt)

    def __get_soc(self, temp, volt_arg):
        """Get battery energy by temperature and voltage"""
        if temp > 30:
            return self.__get_soc_from_dict(55, volt_arg)
        elif temp < 10:
            return self.__get_soc_from_dict(0, volt_arg)
        else:
            return self.__get_soc_from_dict(20, volt_arg)

    def __get_power_vbatt(self):
        """Get vbatt from power"""
        return int(sum([Power.getVbatt() for i in range(100)]) / 100)

    def __get_adc_vbatt(self):
        """Get vbatt from adc"""
        self.__adc.open()
        utime.sleep_ms(self.__adc_period)
        adc_list = list()
        for i in range(self.__adc_period):
            adc_list.append(self.__adc.read(self.__adc_num))
            utime.sleep_ms(self.__adc_period)
        adc_list.remove(min(adc_list))
        adc_list.remove(max(adc_list))
        adc_value = int(sum(adc_list) / len(adc_list))
        self.__adc.close()
        vbatt_value = adc_value * (self.__factor + 1)
        return vbatt_value

    def set_temp(self, temp):
        """Set now temperature."""
        if isinstance(temp, int) or isinstance(temp, float):
            self.__temp = temp
            return True
        return False

    def set_charge_callback(self, charge_callback):
        """Set charge status change callback"""
        if self.__chrg_gpion is not None and self.__stdby_gpion is not None:
            if callable(charge_callback):
                self.__charge_callback = charge_callback
                return True
        return False

    @property
    def voltage(self):
        """Get battery voltage"""
        if self.__adc is None:
            return self.__get_power_vbatt()
        else:
            return self.__get_adc_vbatt()

    @property
    def energy(self):
        """Get battery energy"""
        self.__energy = self.__get_soc(self.__temp, self.voltage)
        return self.__energy

    @property
    def charge_status(self):
        """Get charge status
        Returns:
            0 - Not charged
            1 - Charging
            2 - Finished charging
        """
        self.__update_charge_status()
        return self.__charge_status
