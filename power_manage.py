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
@file      :power_manage.py
@author    :Jack Sun (jack.sun@quectel.com)
@brief     :Device sleep management.
@version   :1.2.0
@date      :2023-03-22 15:49:20
@copyright :Copyright (c) 2022
"""

import pm
from usr.modules.logging import getLogger

log = getLogger(__name__)


class PMLock:
    """Power manage lock."""

    def __init__(self, lock_name):
        if len(lock_name) > 8:
            raise ValueError("lock_name length is larger than 8 size.")
        self.lock = pm.create_wakelock(lock_name, len(lock_name))

    def __enter__(self, *args, **kwargs):
        pm.wakelock_lock(self.lock)

    def __exit__(self, *args, **kwargs):
        pm.wakelock_unlock(self.lock)


class PowerManage:
    """This class is for device sleep."""

    def __init__(self):
        self.__act_unit = 1
        self.__act_time = 1
        self.__tau_unit = 0
        self.__tau_time = 0

    def __init_tau(self, seconds):
        """Change tau seconds to psm args.

        Args:
            seconds (int): tau seconds. unit: second.
        """
        if isinstance(seconds, int) and seconds > 0:
            if seconds >= (320 * 3600) and (seconds % (320 * 3600) == 0 or (int(seconds / (320 * 3600)) > 0 and int(seconds / (320 * 3600)) <= 31 and int(seconds / (10 * 3600)) >= 31)):
                self.__tau_unit = 6
                self.__tau_time = int(seconds / (320 * 3600))
            elif seconds >= (10 * 3600) and (seconds % (10 * 3600) == 0 or (int(seconds / (10 * 3600)) > 0 and int(seconds / (10 * 3600)) <= 31 and int(seconds / 3600) > 31)):
                self.__tau_unit = 2
                self.__tau_time = int(seconds / (10 * 3600))
            elif seconds >= 3600 and (seconds % 3600 == 0 or (int(seconds / 3600) > 0 and int(seconds / 3600) <= 31 and int(seconds / 600) >= 31)):
                self.__tau_unit = 1
                self.__tau_time = int(seconds / 3600)
            elif seconds >= 600 and (seconds % 600 == 0 or (int(seconds / 600) > 0 and int(seconds / 600) <= 31 and int(seconds / 60) >= 31)):
                self.__tau_unit = 0
                self.__tau_time = int(seconds / 600)
            elif seconds >= 60 and (seconds % 60 == 0 or (int(seconds / 60) > 0 and int(seconds / 60) <= 31 and int(seconds / 30) >= 31)):
                self.__tau_unit = 5
                self.__tau_time = int(seconds / 60)
            elif seconds >= 30 and (seconds % 30 == 0 or (int(seconds / 30) > 0 and int(seconds / 30) <= 31)):
                self.__tau_unit = 4
                self.__tau_time = int(seconds / 30)
            else:
                self.__tau_unit = 3
                self.__tau_time = int(seconds / 2)

    def __init_act(self, seconds):
        """Change act seconds to psm args.

        Args:
            seconds (int): act seconds. unit: second.
        """
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

    def autosleep(self, val):
        """Set device autosleep.

        Args:
            val (int): 0 - disable, 1 - enable.

        Returns:
            bool: True - success. False - failed.
        """
        return True if hasattr(pm, "autosleep") and val in (0, 1) and pm.autosleep(val) == 0 else False

    def set_psm(self, mode=1, tau=None, act=None):
        """Set device psm.

        Args:
            mode (int): 0 - disable psm, 1 - enable psm.
            tau (int/None): tau seconds. When mode is 0, this value is None. (default: `None`)
            act (int/None): act seconds. When mode is 0, this value is None. (default: `None`)

        Returns:
            bool: True - success. False - failed.
        """
        if not hasattr(pm, "set_psm_time") or not hasattr(pm, "get_psm_time"):
            return False
        if mode == 0:
            return pm.set_psm_time(0)
        else:
            self.__init_tau(tau)
            self.__init_act(act)
            res = pm.set_psm_time(self.__tau_unit, self.__tau_time, self.__act_unit, self.__act_time)
            log.info("set_psm_time: %s" % res)
            if res:
                get_psm_res = pm.get_psm_time()
                log.debug("get_psm_res: %s" % str(get_psm_res))
                if get_psm_res[0] == 1 and get_psm_res[1:] == [self.__tau_unit, self.__tau_time, self.__act_unit, self.__act_time]:
                    log.debug("PSM time equal set time.")
            return res

    def set_hibernate(self):
        """Set device force into hibernate.

        Returns:
            bool: True - success. False - failed.
        """
        return True if hasattr(pm, "Forcehib") and pm.Forcehib() == 0 else False
