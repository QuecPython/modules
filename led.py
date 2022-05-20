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

import utime
import _thread
import osTimer
from machine import Pin
from usr.modules.logging import getLogger

log = getLogger(__name__)


class LED(object):
    """This class is for control LED"""

    def __init__(self, GPIOn, direction=Pin.OUT, pullMode=Pin.PULL_DISABLE, level=0):
        """LED object init

        Args:
            GPIOn: pin number
            direction: IN - input mode, OUT - output mode
            pullMode: PULL_DISABLE - float mode, PULL_PU - pull-up mode, PULL_PD - pull-down mode
            level: 0 - set the pin to low level, 1- set the pin to high level
        """
        self.__led = Pin(GPIOn, direction, pullMode, level)
        self.__period = 0
        self.__count = 0
        self.__runc = 0
        self.__on_period = 0
        self.__off_period = 5
        self.__led_timer = osTimer()
        self.__led_lock = _thread.allocate_lock()

    def on(self):
        """Set led on"""
        self.__led.write(1)

    def off(self):
        """Set led off"""
        self.__led.write(0)

    def __led_timer_cb(self, args):
        """LED flicker timer."""
        if self.__count > 0:
            self.__runc += 1
            if self.__runc > self.__count:
                self.__runc = 0
                self.stop_flicker()
                return
        self.on()
        utime.sleep_ms(self.__on_period)
        self.off()
        self.__led_timer.start(self.__off_period, 0, self.__led_timer_cb)

    def start_flicker(self, on_period, off_period, count=0):
        """Start led flicker

        Args:
            on_period(int): led on time, unit: ms
            off_period(int): led off time, unit: ms
            count(int): flicker times, if count is 0, filcker forever. (default: {0})

        Returns:
            bool: True -- success; False -- falied.
        """
        self.__on_period = on_period
        self.__off_period = off_period
        self.__count = count
        if self.__count >= 0 and self.__on_period > 0 and self.__off_period >= 5:
            self.stop_flicker()
            if self.__led_timer.start(self.__off_period, 0, self.__led_timer_cb) == 0:
                return True

        return False

    def stop_flicker(self):
        """Stop LED flicker

        Returns:
            bool: True -- success; False -- falied.
        """
        return True if self.__led_timer.stop() == 0 else False
