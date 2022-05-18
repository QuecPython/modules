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
import utime
from machine import Pin
from usr.modules.logging import getLogger

log = getLogger(__name__)


class Buzzer(object):
    """This class is for control Buzzer"""
    def __init__(self, GPIOn, direction=Pin.OUT, pullMode=Pin.PULL_DISABLE, level=0):
        """
        Parameter:
            GPIOn: pin number
            direction: IN - input mode, OUT - output mode
            pullMode: PULL_DISABLE - float mode, PULL_PU - pull-up mode, PULL_PD - pull-down mode
            level: 0 - set the pin to low level, 1- set the pin to high level
        """
        self.__buzz = Pin(GPIOn, direction, pullMode, level)
        self.__period = 0
        self.__count = 0
        self.__runc = 0
        self.__on_period = 0
        self.__off_period = 5
        self.__buzz_timer = osTimer()
        self.__buzz_lock = _thread.allocate_lock()

    def on(self):
        self.__buzz.write(1)

    def off(self):
        self.__buzz.write(0)

    def __buzz_timer_cb(self, args):
        """buzz flicker timer."""
        if self.__count > 0:
            self.__runc += 1
            if self.__runc > self.__count:
                self.__runc = 0
                self.stop_flicker()
                return
        self.on()
        utime.sleep_ms(self.__on_period)
        self.off()
        self.__buzz_timer.start(self.__off_period, 0, self.__buzz_timer_cb)

    def start_flicker(self, on_period, off_period, count):
        """Start buzz period
        note:
            __period is 0, not start buzz timer and stop led timer.
        """
        self.__on_period = on_period
        self.__off_period = off_period
        self.__count = count
        if self.__count >= 0 and self.__on_period > 0 and self.__off_period >= 5:
            self.stop_flicker()
            if self.__buzz_timer.start(self.__off_period, 0, self.__buzz_timer_cb) == 0:
                return True

        return False

    def stop_flicker(self):
        """Stop buzz period"""
        return True if self.__buzz_timer.stop() == 0 else False



