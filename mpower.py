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
import net
import utime
import _thread
import osTimer

from queue import Queue

from usr.modules.common import Observable
from usr.modules.logging import getLogger

try:
    from machine import RTC
except ImportError:
    RTC = None

log = getLogger(__name__)

LOW_ENERGY_METHOD = ("NULL", "PM", "PSM", "POWERDOWN")


class LowEnergyManage(Observable):
    """This class is managing low energy wake up"""

    def __init__(self):
        super().__init__()

        self.__timer = None

        self.__period = 60
        self.__act_unit = 0
        self.__act_time = 5
        self.__tau_unit = 0
        self.__tau_time = 0
        self.__low_energy_method = "PM"
        self.__thread_id = None

        self.__lpm_fd = None
        self.__pm_lock_name = "low_energy_pm_lock"
        self.__low_energy_queue = Queue(maxsize=8)

    def __timer_callback(self, args):
        """This callback is for interrupting sleep"""
        self.__low_energy_queue.put(self.__low_energy_method)

    def __low_energy_work(self):
        """This function is for notify Observers after interrupting sleep

        PM:
            1. Check PM init.
            2. Notify observers to run business.
            3. Unlock wake lock.
        """
        while True:
            data = self.__low_energy_queue.get()
            log.debug("__low_energy_work data: %s" % data)
            if data:
                if self.__low_energy_method == "PM":
                    self.pm_init()
                    wlk_res = pm.wakelock_lock(self.__lpm_fd)
                    log.debug("pm.wakelock_lock %s." % ("Success" if wlk_res == 0 else "Falied"))

                self.notifyObservers(self, *(data,))

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

    def __rtc_enable(self, enable):
        """Enable or disable RTC"""
        enable_alarm_res = self.__timer.enable_alarm(enable)
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
        res = self.__timer.stop()
        log.debug("__timer_stop res: %s" % res)
        return True if res == 0 else False

    def __set_tau_time(self):
        if self.__period % (320 * 3600) == 0:
            self.__tau_unit = 6
            self.__tau_time = int(self.__period / (320 * 3600))
        elif self.__period % (10 * 3600) == 0:
            self.__tau_unit = 2
            self.__tau_time = int(self.__period / (10 * 3600))
        elif self.__period % 3600 == 0:
            self.__tau_unit = 1
            self.__tau_time = int(self.__period / 3600)
        if self.__period % 600 == 0:
            self.__tau_unit = 0
            self.__tau_time = int(self.__period / 600)
        elif self.__period % 60 == 0:
            self.__tau_unit = 5
            self.__tau_time = int(self.__period / 60)
        elif self.__period % 30 == 0:
            self.__tau_unit = 4
            self.__tau_time = int(self.__period / 30)
        else:
            self.__tau_unit = 3
            self.__tau_time = int(self.__period / 2)

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

    def get_low_energy_method(self):
        """Get low energy method
        Return:
            NULL: No low energy
            PM: wake lock
            PSM: PSM
            POWERDOWN: power down
        """
        return self.__low_energy_method

    def set_low_energy_method(self, method):
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

    def get_lpm_fd(self):
        """Get PM(wake lock) lock id"""
        return self.__lpm_fd

    def psm_init(self):
        self.__set_tau_time()
        self.__psm_stop()
        pm.autosleep(1)
        if pm.set_psm_time(self.__tau_unit, self.__tau_time, self.__act_uint, self.__act_time):
            get_psm_res = pm.get_psm_time()
            if get_psm_res[1:] == [self.__tau_unit, self.__tau_time, self.__act_uint, self.__act_time]:
                net.setModemFun(0, 0)
                utime.sleep_ms(300)
                net.setModemFun(1, 0)
                return True
        return False

    def pm_init(self):
        if self.__lpm_fd is None:
            pm.autosleep(1)
            self.__lpm_fd = pm.create_wakelock(self.__pm_lock_name, len(self.__pm_lock_name))

    def low_energy_init(self):
        """Init low energy"""
        try:
            if self.__thread_id is not None:
                _thread.stop_thread(self.__thread_id)
            if self.__lpm_fd is not None:
                pm.delete_wakelock(self.__lpm_fd)
                self.__lpm_fd = None

            self.__thread_id = _thread.start_new_thread(self.__low_energy_work, ())
            if self.__low_energy_method == "PM":
                self.pm_init()
            elif self.__low_energy_method == "PSM":
                self.psm_init()
            elif self.__low_energy_method in ("NULL", "POWERDOWN"):
                pass

            self.__timer_init()
            return True
        except:
            return False

    def start(self):
        """Start low energy sleep"""
        if self.__low_energy_method != "PSM":
            if RTC is not None:
                return self.__rtc_start()
            else:
                return self.__timer_start()
        return True

    def stop(self):
        """Stop low energy sleep"""
        if self.__low_energy_method != "PSM":
            if RTC is not None:
                return self.__rtc_stop()
            else:
                return self.__timer_stop()
        else:
            return self.__psm_stop()
