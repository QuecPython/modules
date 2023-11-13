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

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@file      :net_manage.py
@author    :Jack Sun (jack.sun@quectel.com)
@brief     :Net management.
@version   :1.2.0
@date      :2022-10-31 10:45:46
@copyright :Copyright (c) 2022
"""

import net
import sim
import utime
import ntptime
import dataCall
import checkNet
import usys as sys


class NetManage:
    """This class is for net management."""

    def __init__(self, project_name, project_version):
        self.__checknet = checkNet.CheckNetwork(project_name, project_version)
        self.__checknet.poweron_print_once()

    @property
    def status(self):
        """Read device net status.

        Returns:
            bool: True - net is connected, False - net is disconnected.
        """
        res = False
        try:
            data_call_info = dataCall.getInfo(1, 0)
            net_state = net.getState()
            if isinstance(data_call_info, tuple) and data_call_info[2][0] == 1 and \
                    isinstance(net_state, tuple) and len(net_state) >= 2 and net_state[1][0] in (1, 5):
                res = True
            else:
                res = False
        except Exception as e:
            sys.print_exception(e)
        return res

    @property
    def sim_status(self):
        """Read sim card status.

        Returns:
            int: 1 - sim is ready, other - sim is not ready.
        """
        return sim.getStatus()

    def wait_connect(self, timeout=60):
        """Wait net connected.

        Args:
            timeout (int): timeout seconds. (default: `60`)

        Returns:
            tuple: (3, 1) - success, other - failed.
        """
        return self.__checknet.wait_network_connected(timeout)

    def connect(self):
        """Set net connect.

        Returns:
            bool: True - success, False - failed.
        """
        if net.setModemFun(1) == 0:
            return True
        return False

    def disconnect(self, val=4):
        """Set net disconnect.

        Args:
            val (int): 0 - all close, 4 - fly mode. (default: `4`)

        Returns:
            bool: True - success, False - failed.
        """
        if val in (0, 4) and net.setModemFun(val) == 0:
            return True
        return False

    def reconnect(self):
        """Net reconnect.

        Returns:
            bool: True - success, False - failed.
        """
        if self.disconnect():
            utime.sleep_ms(200)
            return self.connect()
        return False

    def sync_time(self, timezone=8):
        """Sync device time from server.

        Args:
            timezone (int): timezone. range: [-12, 12] (default: `8`)

        Returns:
            bool: True - success, False - failed.
        """
        return True if self.status and timezone >= -12 and timezone <= 12 and ntptime.settime(timezone) == 0 else False

    def set_callback(self, callback):
        """Set callback to recive net change status.

        Args:
            callback (function): callback funtion.

        Returns:
            bool: True - success, False - failed.
        """
        if callable(callback):
            res = dataCall.setCallback(callback)
            return True if res == 0 else False
        return False
