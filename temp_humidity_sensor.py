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
# limitations under the License.from machine import I2C

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@file      :temp_humidity_sensor.py
@author    :elian.wang@quectel.com
@brief     :Show tempurature and humidity sensor TH20 usage
@version   :0.1
@date      :2022-05-20 11:14:24
@copyright :Copyright (c) 2022
"""

import utime as time
from machine import I2C


class TempHumiditySensor:
    """Read tempurature and humidity sensor value, reset sensor"""
    def __init__(self, i2cn=I2C.I2C1, mode=I2C.STANDARD_MODE, calibration=0xE1,
                 start_measurment=0xAC, reset=0xBA, i2c_addr=0x38):
        self.__i2c = I2C(i2cn, mode)
        # Initialization command
        self.__CALIBRATION_CMD = calibration
        # Trigger measurement
        self.__START_MEASURMENT_CMD = start_measurment
        # reset
        self.__RESET_CMD = reset
        # slave address
        self.__i2c_addr = i2c_addr

    def __write_data(self, data):
        """Write data to I2C

        Args:
            data(list): command

        Returns:
            int: 0 - success, -1 - falied
        """
        return self.__i2c.write(self.__i2c_addr, bytearray(0x00), 0, bytearray(data), len(data))

    def __read_data(self, length):
        """Read data from I2C

        Args:
            length(int): bytearray length

        Returns:
            list: revice data
        """
        r_data = bytearray([0x00] * length)
        self.__i2c.read(self.__i2c_addr, bytearray(0x00), 0, r_data, length, 0)
        return list(r_data)

    def __check_data(self, data):
        """Check recive data

        Args:
            data(list): data from read data

        Returns:
            list: valid data, return empty list if no valid data
        """
        return [] if (data[0] >> 7) != 0x0 else data[1:6]

    def __start_measurment(self):
        """Trigger data conversion,send 0xAC, 0x33， 0x00

        Returns:
            bool: True - success, False - Falied
        """
        write_res = self.__write_data([self.__START_MEASURMENT_CMD, 0x33, 0x00])
        if write_res == 0:
            time.sleep_ms(200)  # at last delay 75ms
            return True
        return False

    def __get_datas(self, length):
        """Get valid i2c data

        Args:
            length(int): read data length

        Returns:
            list: read data from i2c, return empty list if start measurment falied
        """
        if self.__start_measurment():
            return self.__check_data(self.__read_data(length))
        return []

    def __get_humidity(self, data):
        """Read humidity from i2c data

        Args:
            data(list): i2c data

        Returns:
            float: humidity
        """
        humidity = (data[0] << 12) | (data[1] << 4) | ((data[2] & 0xF0) >> 4)
        return float("%.2f" % ((humidity / (1 << 20)) * 100.0))

    def __get_temperature(self, data):
        """Read temperature from i2c data

        Args:
            data(list): i2c data

        Returns:
            float: temperature
        """
        temperature = ((data[2] & 0xf) << 16) | (data[3] << 8) | data[4]
        return float("%.2f" % ((temperature * 200.0 / (1 << 20)) - 50))

    def on(self):
        """Calibrate i2c to read data.

        Abstracted into sensor open.

        Returns:
            bool: True - success, False - falied.
        """
        write_res = self.__write_data([self.__CALIBRATION_CMD, 0x08, 0x00])
        if write_res == 0:
            time.sleep_ms(300)  # at last 300ms
            return True
        return False

    def off(self):
        """Reset i2c to read data.

        Abstracted into sensor close.

        Returns:
            bool: True - success, False - falied.
        """
        write_res = self.__write_data([self.__RESET_CMD])
        if write_res == 0:
            time.sleep_ms(20)  # at last 20ms
            return True
        return False

    def read(self):
        """Read temperature and humidity from i2c

        Returns:
            tuple: (temperature, humidity)
                temperature(float): None if get failed else float data
                humidity(float): None if get failed else float data
        """
        data = self.__get_datas(6)
        if not data:
            return (None, None)
        return self.__get_temperature(data), self.__get_humidity(data)
