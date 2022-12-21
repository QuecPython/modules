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

import pm
import utime
import _thread
import osTimer

from usr.modules.logging import getLogger

try:
    from machine import RTC
except ImportError:
    RTC = None

log = getLogger(__name__)

LOW_ENERGY_METHOD = ("NULL", "PM", "PSM", "POWERDOWN")


class LowEnergyManage:
    """This class is managing low energy wake up"""

    def __init__(self, period=60, method="PM"):
        super().__init__()
        self.__period = period
        self.__low_energy_method = method
        self.__timer = None
        self.__lpm_fd = None
        self.__callback = print

        self.__tau_unit = 0
        self.__tau_time = 1
        self.__act_unit = 0
        self.__act_time = 5

    def __timer_callback(self, args):
        """This callback is for interrupting sleep"""
        # _thread.stack_size(32 * 1024)
        _thread.start_new_thread(self.__low_energy_work, ())

    def __low_energy_work(self):
        """This function is for notify Observers after interrupting sleep

        PM:
            1. Check PM init.
            2. Notify observers to run business.
            3. Unlock wake lock.
        """
        if self.__low_energy_method == "PM":
            wlk_res = pm.wakelock_lock(self.__lpm_fd)
            log.debug("pm.wakelock_lock %s." % ("Success" if wlk_res == 0 else "Falied"))

        self.__callback(self.__low_energy_method)

        if self.__low_energy_method == "PM":
            wulk_res = pm.wakelock_unlock(self.__lpm_fd)
            log.debug("pm.wakelock_unlock %s." % ("Success" if wulk_res == 0 else "Falied"))

    def __timer_init(self):
        """Use RTC or osTimer for timer"""
        if RTC is not None:
            self.__timer = RTC()
        else:
            if self.__low_energy_method in ("PSM", "POWERDOWN"):
                raise TypeError("osTimer not support %s!" % self.__low_energy_method)
            self.__timer = osTimer()

    def __pm_init(self):
        if self.__lpm_fd is None:
            pm.autosleep(1)
            self.__lpm_fd = pm.create_wakelock("pm_lock", 7)

    def __rtc_enable(self, enable):
        """Enable or disable RTC"""
        enable_alarm_res = self.__timer.enable_alarm(enable) if self.__timer else 0
        return True if enable_alarm_res == 0 else False

    def __rtc_start(self):
        """Start low energy sleep by RTC"""
        self.__rtc_enable(0)
        atime = utime.localtime(utime.mktime(utime.localtime()) + self.__period)
        alarm_time = [atime[0], atime[1], atime[2], atime[6], atime[3], atime[4], atime[5], 0]
        self.__timer.register_callback(self.__timer_callback)
        if self.__timer.set_alarm(alarm_time) == 0:
            return self.__rtc_enable(1)
        return False

    def __rtc_stop(self):
        """Stop low energy sleep by RTC"""
        return self.__rtc_enable(0)

    def __timer_start(self):
        """Start low energy sleep by osTimer"""
        res = self.__timer.start(self.__period * 1000, 0, self.__timer_callback)
        return True if res == 0 else False

    def __timer_stop(self):
        """Stop low energy sleep by osTimer"""
        res = self.__timer.stop() if self.__timer else 0
        log.debug("__timer_stop res: %s" % res)
        return True if res == 0 else False

    def __psm_start(self):
        pm.autosleep(1)
        if pm.set_psm_time(self.__tau_unit, self.__tau_time, self.__act_uint, self.__act_time):
            get_psm_res = pm.get_psm_time()
            if get_psm_res[0] == 1 and get_psm_res[1:] == [self.__tau_unit, self.__tau_time, self.__act_uint, self.__act_time]:
                return True
        return False

    def __psm_stop(self):
        return pm.set_psm_time(0)

    def get_period(self):
        """Get low energy interrupting sleep period"""
        return self.__period

    def set_period(self, seconds=0):
        """Set low energy interrupting sleep period
        Parameter:
            seconds: interrupting sleep period
        """
        if isinstance(seconds, int) and seconds > 0:
            self.__period = seconds
            return True
        return False

    def get_method(self):
        """Get low energy method
        Return:
            NULL: No low energy
            PM: wake lock
            PSM: PSM
            POWERDOWN: power down
        """
        return self.__low_energy_method

    def set_method(self, method):
        """Set low energy method
        Parameter:
            method:
                NULL: No low energy
                PM: wake lock
                PSM: PSM
                POWERDOWN: power down
        """
        if method in LOW_ENERGY_METHOD:
            if RTC is None and method in ("PSM", "POWERDOWN"):
                return False
            self.__low_energy_method = method
            return True
        return False

    def set_tau_time(self, period):
        if period % (320 * 3600) == 0:
            self.__tau_unit = 6
            self.__tau_time = int(period / (320 * 3600))
        elif period % (10 * 3600) == 0:
            self.__tau_unit = 2
            self.__tau_time = int(period / (10 * 3600))
        elif period % 3600 == 0:
            self.__tau_unit = 1
            self.__tau_time = int(period / 3600)
        elif period % 600 == 0:
            self.__tau_unit = 0
            self.__tau_time = int(period / 600)
        elif period % 60 == 0:
            self.__tau_unit = 5
            self.__tau_time = int(period / 60)
        elif period % 30 == 0:
            self.__tau_unit = 4
            self.__tau_time = int(period / 30)
        else:
            self.__tau_unit = 3
            self.__tau_time = int(period / 2)
        return True

    def set_act_time(self, seconds):
        if isinstance(seconds, int) and seconds > 0:
            if seconds % 600 == 0:
                self.__act_unit = 2
                self.__act_time = int(seconds / 600)
            elif seconds % 60 == 0:
                self.__act_unit = 1
                self.__act_time = int(seconds / 600)
            else:
                self.__act_unit = 0
                self.__act_time = int(seconds / 2)
            return True
        return False

    def set_callback(self, callback):
        if callable(callback):
            self.__callback = callback
            return True
        return False

    def start(self):
        """Start low energy sleep"""
        self.__timer_init()
        if self.__low_energy_method == "PSM":
            return self.__psm_start()
        else:
            if self.__low_energy_method == "PM":
                self.__pm_init()
            return self.__rtc_start() if RTC is not None else self.__timer_start()

    def stop(self):
        """Stop low energy sleep"""
        if self.__low_energy_method == "PSM":
            return self.__psm_stop()
        else:
            return self.__rtc_stop() if RTC is not None else self.__timer_stop()
