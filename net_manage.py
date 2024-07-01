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
@file      :net_manage.py
@author    :Jack Sun (jack.sun@quectel.com)
@brief     :Net management.
@version   :1.2.0
@date      :2022-10-31 10:45:46
@copyright :Copyright (c) 2022
"""

import sys
import net
import sim
import ntptime
import osTimer
import _thread
import dataCall
import checkNet
import utime as time

from usr.modules.logging import getLogger

log = getLogger(__name__)


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
        return self.__checknet.waitNetworkReady(timeout)

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
            time.sleep_ms(200)
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


class NetManager:

    def __init__(self):
        self.__conn_flag = 0
        self.__disconn_flag = 0
        self.__reconn_flag = 0
        self.__callback = None
        self.__net_check_timer = osTimer()
        self.__net_check_cycle = 5 * 60 * 1000
        self.__reconn_tid = None

        dataCall.setCallback(self.__net_callback)

    def __net_callback(self, args):
        log.debug("profile id[%s], net state[%s], last args[%s]" % args)
        if args[1] == 0:
            self.__net_check_timer.stop()
            self.net_check(None)
            self.__net_check_timer.start(self.__net_check_cycle, 1, self.net_check)
        if callable(self.__callback):
            self.__callback(args)

    def set_callback(self, callback):
        if callable(callback):
            self.__callback = callback
            return True
        return False

    def net_connect(self):
        res = -1
        if self.__conn_flag != 0:
            return -2
        self.__conn_flag = 1
        try:
            # Reconnect net.
            if net.getModemFun() != 1:
                _res = self.net_disconnect()
                log.debug("net_connect net_disconnect %s" % _res)
                time.sleep(5)
                _res = net.setModemFun(1)
                log.debug("net.setModemFun(1) %s" % _res)
                if _res != 0:
                    return -3

            # Check sim status
            if self.sim_status() != 1:
                log.error("SIM card is not ready.")
                return -4

            # Wait net connect.
            _res = checkNet.waitNetworkReady(300)
            log.debug("checkNet.waitNetworkReady %s" % str(_res))
            res = 0 if _res == (3, 1) else -5
        except Exception as e:
            sys.print_exception(e)
            log.error(str(e))
        finally:
            self.__conn_flag = 0
        self.__net_check_timer.stop()
        self.__net_check_timer.start(self.__net_check_cycle, 1, self.net_check)
        return res

    def net_disconnect(self):
        if self.__disconn_flag != 0:
            return False
        self.__disconn_flag = 1
        res = True if (net.setModemFun(4) == 0) else (net.setModemFun(0) == 0)
        self.__net_check_timer.stop()
        self.__disconn_flag = 0
        return res

    def net_reconnect(self):
        if self.__reconn_flag != 0:
            return False
        self.__reconn_flag = 1
        res = self.net_connect() if self.net_disconnect() else False
        self.__reconn_flag = 0
        self.__reconn_tid = None
        return res

    def net_status(self):
        return True if self.sim_status() == 1 and self.net_state() and self.call_state() else False

    def net_state(self):
        try:
            _net_state_ = net.getState()
            log.debug("net.getState() %s" % str(_net_state_))
            return True if isinstance(_net_state_, tuple) and len(_net_state_) >= 2 and _net_state_[1][0] in (1, 5) else False
        except Exception as e:
            sys.print_exception(e)
            log.error(str(e))
        return False

    def net_config(self, state=None):
        if state is None:
            return net.getConfig()
        elif state in (0, 5, 6):
            return (net.setConfig(state) == 0)
        return False

    def net_mode(self):
        _net_mode_ = net.getNetMode()
        if _net_mode_ == -1 or not isinstance(_net_mode_, tuple) or len(_net_mode_) < 4:
            return -1
        if _net_mode_[3] in (0, 1, 3):
            return 2
        elif _net_mode_[3] in (2, 4, 5, 6, 8):
            return 3
        elif _net_mode_[3] in (7, 9):
            return 4
        return -1

    def net_check(self, args):
        if not self.net_status():
            try:
                if not self.__reconn_tid or (self.__reconn_tid and not _thread.threadIsRunning(self.__reconn_tid)):
                    _thread.stack_size(0x2000)
                    self.__reconn_tid = _thread.start_new_thread(self.net_reconnect, ())
            except Exception as e:
                sys.print_exception(e)
                log.error(str(e))

    def call_state(self):
        try:
            call_info = self.call_info()
            log.debug("dataCall.getInfo %s" % str(call_info))
            return True if isinstance(call_info, tuple) and len(call_info) >= 3 and call_info[2][0] == 1 else False
        except Exception as e:
            sys.print_exception(e)
            log.error(str(e))
        return False

    def call_info(self):
        return dataCall.getInfo(1, 0)

    def sim_status(self):
        # # Check net modem.
        # if net.getModemFun() == 0:
        #     net.setModemFun(1)

        # Check sim status.
        count = 0
        while sim.getStatus() == -1 and count < 3:
            time.sleep_ms(100)
            count += 1
        return sim.getStatus()

    def sim_imsi(self):
        return sim.getImsi()

    def sim_iccid(self):
        return sim.getIccid()

    def signal_csq(self):
        return net.csqQueryPoll()

    def signal_level(self):
        signal = self.signal_csq()
        _signal_level_ = int(signal * 5 / 31) if 0 <= signal <= 31 else 0
        return _signal_level_

    def sync_time(self, timezone=8):
        """Sync device time from server.

        Args:
            timezone (int): timezone. range: [-12, 12] (default: `8`)

        Returns:
            bool: True - success, False - failed.
        """
        return (self.net_status() and timezone in range(-12, 13) and ntptime.settime(timezone) == 0)
