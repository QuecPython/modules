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
@file      :common.py
@author    :Jack Sun (jack.sun@quectel.com)
@brief     :Common modules.
@version   :1.2.0
@date      :2022-11-24 17:06:30
@copyright :Copyright (c) 2022
"""

import utime
import _thread
import usys as sys
from machine import Pin


def option_lock(thread_lock):
    """Function thread lock decorator"""
    def function_lock(func):
        def wrapperd_fun(*args, **kwargs):
            with thread_lock:
                return func(*args, **kwargs)
        return wrapperd_fun
    return function_lock


class Singleton(object):
    """Singleton base class"""
    _instance_lock = _thread.allocate_lock()

    def __init__(self, *args, **kwargs):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance_dict"):
            Singleton.instance_dict = {}

        if str(cls) not in Singleton.instance_dict.keys():
            with Singleton._instance_lock:
                _instance = super().__new__(cls, *args, **kwargs)
                Singleton.instance_dict[str(cls)] = _instance

        return Singleton.instance_dict[str(cls)]


class GPIOCtrl:
    """This class is for gpio control.

    This is a base class for LED, Buzzer.
    """

    def __init__(self):
        """GPIO control object init"""
        self.__gpios = []
        self.__period = 0
        self.__count = 0
        self.__on_period = 5
        self.__off_period = 5
        self.__thread_id = None
        self.__flicker_stop = 0
        self.__onoff_lock = _thread.allocate_lock()

    def __write(self, val):
        """Set gpio level

        Args:
            val (int): 0 - low level, 1 - high level.

        Returns:
            bool: True - success, False - Failed.
        """
        with self.__onoff_lock:
            res = []
            for i in self.__gpios:
                if i.get_dir() != 1:
                    i.set_dir(Pin.OUT)
                res.append(i.write(val))
            res = tuple(set(res))
            return True if len(res) == 1 and res[0] == 0 else False

    def __flicker_running(self, on_period, off_period, count):
        """This function is for led filcker threadn.

        Args:
            on_period (int): LED on time.
            off_period (int): LED off time.
            count (int): LED flicker times.
        """
        count = count * 2
        runc = count
        while True:
            if self.state == 0:
                self.on()
                utime.sleep_ms(on_period)
            else:
                self.off()
                utime.sleep_ms(off_period)
            if count > 0:
                runc -= 1
                if runc == 0:
                    break
            if self.__flicker_stop == 1:
                break

    @property
    def state(self):
        """Read gpio now state

        Returns:
            int: 0 - low level, 1 - high level.
        """
        states = tuple(set([i.read() for i in self.__gpios]))
        return 1 if len(states) == 1 and states[0] == 1 else 0

    def add_gpio(self, gpio):
        """Add control gpio.

        Args:
            gpio (object): Pin.GPIO object.

        Returns:
            bool: True - success, False - Failed.
        """
        if isinstance(gpio, Pin):
            if gpio not in self.__gpios:
                self.__gpios.append(gpio)
            return True
        return False

    def get_gpio(self):
        """Get this object gpios

        Returns:
            list: GPIO object list.
        """
        return self.__gpios

    def on(self):
        """Set gpio high level.

        Returns:
            bool: True - Success, False - Failed.
        """
        return self.__write(1)

    def off(self):
        """Set gpio low level.

        Returns:
            bool: True - Success, False - Failed.
        """
        return self.__write(0)

    def start_flicker(self, on_period, off_period, count=0):
        """Start gpio level cyclical change.

        Args:
            on_period(int): gpio high level time, unit: ms
            off_period(int): gpio low level time, unit: ms
            count(int): flicker times, if count is 0, filcker forever. (default: {0})

        Returns:
            bool: True - success; False - falied.
        """
        self.__on_period = on_period
        self.__off_period = off_period
        self.__count = count * 2
        if self.__count >= 0 and self.__on_period >= 5 and self.__off_period >= 5:
            self.stop_flicker()
            self.__flicker_stop = 0
            try:
                _thread.stack_size(0x800)
                self.__thread_id = _thread.start_new_thread(self.__flicker_running, (on_period, off_period, count))
            except Exception as e:
                sys.print_exception(e)
        return False

    def stop_flicker(self):
        """Stop gpio level cyclical change.

        Returns:
            bool: True - success; False - falied.
        """
        self.__flicker_stop = 1
        if self.__thread_id is not None and _thread.threadIsRunning(self.__thread_id):
            try:
                _thread.stop_thread(self.__thread_id)
            except Exception as e:
                sys.print_exception(e)
        self.__thread_id = None
        return self.off()


class Waiter(object):

    def __init__(self):
        self.__info = None  # usr information for notifier

        self.__lock = _thread.allocate_lock()
        self.__lock.acquire()  # acquire immediately for holding the lock.

        self.acquire = self.__lock.acquire
        self.release = self.__lock.release

    @property
    def info(self):
        return self.__info

    @info.setter
    def info(self, info):
        self.__info = info


class Condition(object):
    """条件变量(使用互斥锁实现)"""

    def __init__(self):
        self.__lock = _thread.allocate_lock()
        self.__waiters = []

    def __create_waiter(self):
        waiter = Waiter()
        with self.__lock:
            self.__waiters.append(waiter)
        return waiter

    def wait(self):
        waiter = self.__create_waiter()
        waiter.acquire()  # block here, waiting for release in the future.
        return waiter.info

    def notify(self, n=1, info=None):
        with self.__lock:
            for waiter in self.__waiters[:n]:
                waiter.info = info
                waiter.release()  # release here, some `wait` method will be unblocked.
                self.__waiters.remove(waiter)

    def notify_all(self, info=None):
        self.notify(n=len(self.__waiters), info=info)


class Event(object):

    def __init__(self):
        self.__lock = _thread.allocate_lock()
        self.flag = False
        self.cond = Condition()

    def wait(self):
        if self.flag is not True:
            self.cond.wait()
        return self.flag

    def set(self):
        with self.__lock:
            self.flag = True
            self.cond.notify_all()

    def clear(self):
        with self.__lock:
            self.flag = False

    def is_set(self):
        return self.flag
