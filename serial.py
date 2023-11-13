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
author: dustin.wei
email: dustin.wei@quectel.com
date: 2023-2-14

背景：QuecPython的machine.uart串口通信模块的读写均为**非阻塞**模式，现需求实现**阻塞**模式`读`操作。
功能描述：封装Serial类，实现基于QuecPython的串口通信阻塞/非阻塞读操作。
"""

import _thread
from machine import UART, Timer
from usr.modules.common import Condition


class TimerContext(object):
    """基于machine.Timer的定时器实现(ONE_SHOT模式)。支持上下文管理器协议。"""
    __timer = Timer(Timer.Timer1)

    def __init__(self, timeout, callback):
        self.timeout = timeout  # ms; >0 will start a one shot timer, <=0 do nothing.
        self.timer_cb = callback  # callback after timeout.

    def __enter__(self):
        if self.timeout > 0:
            self.__timer.start(period=self.timeout, mode=Timer.ONE_SHOT, callback=self.timer_cb)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.timeout > 0:
            self.__timer.stop()


class Serial(object):
    """串口通信"""

    def __init__(self, port=2, baudrate=115200, bytesize=8, parity=0, stopbits=1, flowctl=0):
        port = getattr(UART, 'UART{}'.format(port))
        self.__uart = UART(port, baudrate, bytesize, parity, stopbits, flowctl)
        self.__uart.set_callback(self.__uart_cb)
        self.__cond = Condition()

    def __uart_cb(self, args):
        self.__cond.notify(info=False)

    def __timer_cb(self, args):
        self.__cond.notify(info=True)

    def write(self, data):
        self.__uart.write(data)

    def read(self, size, timeout=0):
        """
        read from uart port with block or noblock mode.
        :param size: int, N bytes you want to read. if read enough bytes, return immediately.
        :param timeout: int(ms). =0 for no blocking, <0 for block forever, >0 for block until timeout.
        :return: bytes actually read.
        """
        if timeout == 0:
            return self.__uart.read(size)

        r_data = b''
        with TimerContext(timeout, self.__timer_cb):
            while len(r_data) < size:
                raw = self.__uart.read(1)
                if not raw:
                    if self.__cond.wait():
                        break
                else:
                    r_data += raw
        return r_data
