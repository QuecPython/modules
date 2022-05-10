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

import _thread
import osTimer
from machine import Pin
from usr.modules.logging import getLogger

log = getLogger(__name__)


class LED(object):
    """This class is for control LED"""

    def __init__(self, GPIOn, direction=Pin.OUT, pullMode=Pin.PULL_DISABLE, level=0):
        """
        Parameter:
            GPIOn: pin number
            direction: IN - input mode, OUT - output mode
            pullMode: PULL_DISABLE - float mode, PULL_PU - pull-up mode, PULL_PD - pull-down mode
            level: 0 - set the pin to low level, 1- set the pin to high level
        """
        self.__gpio = Pin(GPIOn, direction, pullMode, level)
        self.__period = 0
        self.__led_timer = osTimer()
        self.__led_lock = _thread.allocate_lock()

    def __led_timer_cb(self, args):
        """LED flicker timer."""
        self.switch()

    def get_period(self):
        """Get LED flicker period."""
        return self.__period

    def set_period(self, period):
        """Set LED flicker period.
        Parameter:
            period: flicker period. Unit: second.
        """
        if isinstance(period, int) and period >= 0:
            self.__period = period
            return True
        return False

    def start_flicker(self):
        """Start LED period
        note:
            __period is 0, not start led timer and stop led timer.
        """
        if self.__period > 0:
            self.stop_flicker()
            if self.__led_timer.start(self.__period, 1, self.__led_timer_cb) == 0:
                return True

        return False

    def stop_flicker(self):
        """Stop LED period"""
        return True if self.__led_timer.stop() == 0 else False

    def get_led_status(self):
        """Get LED Status From Pin
        Return:
            1 LED ON (high level).
            0 LED OFF (low level).
        """
        with self.__led_lock:
            return self.__gpio.read()

    def set_led_status(self, onoff):
        """Set LED Status
        Parameter:
            onoff:
                1 LED ON (high level).
                0 LED OFF (low level).
        """
        with self.__led_lock:
            return True if self.__gpio.write(onoff) == 0 else False

    def switch(self):
        """Auto Check LED Status ON To OFF or OFF To ON."""
        if self.get_led_status() == 1:
            return self.set_led_status(0)
        else:
            return self.set_led_status(1)
