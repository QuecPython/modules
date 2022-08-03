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

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@file      :test_temp_humidity.py
@author    :Jack Sun (jack.sun@quectel.com)
@brief     :<description>
@version   :1.0.0
@date      :2022-06-23 09:07:44
@copyright :Copyright (c) 2022
"""

from machine import I2C
from usr.modules.temp_humidity_sensor import TempHumiditySensor


def test_temp_humidity():
    res = {"all": 0, "success": 0, "failed": 0}

    temp_humidity_obj = TempHumiditySensor(i2cn=I2C.I2C1, mode=I2C.FAST_MODE)

    msg = "[test_temp_humidity] %s: temp_humidity_obj.on(): %s."
    on_res = temp_humidity_obj.on()
    assert on_res, msg % ("FAILED", on_res)
    print(msg % ("SUCCESS", on_res))
    res["success"] += 1

    msg = "[test_temp_humidity] %s: temp_humidity_obj.read(): temperature: %s°C, humidity: %s%%."
    temperature, humidity = temp_humidity_obj.read()
    assert temperature is not None and humidity is not None, msg % ("FAILED", temperature, humidity)
    print(msg % ("SUCCESS", temperature, humidity))
    res["success"] += 1

    msg = "[test_temp_humidity] %s: temp_humidity_obj.off(): %s."
    off_res = temp_humidity_obj.off()
    assert off_res, msg % ("FAILED", off_res)
    print(msg % ("SUCCESS", off_res))
    res["success"] += 1


if __name__ == '__main__':
    test_temp_humidity()
