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
@file      :history.py
@author    :Jack Sun (jack.sun@quectel.com)
@brief     :History management.
@version   :1.2.0
@date      :2022-11-24 17:06:30
@copyright :Copyright (c) 2022
"""

import uos
import ql_fs
import ujson
import _thread


class History:
    """This class is for manage history file."""

    def __init__(self, history_file="/usr/tracker_data.hist", max_hist_num=100):
        """
        Parameter:
            history_file: filename include full path
            max_hist_num: history data list max size
        """
        self.__history = history_file
        self.__max_hist_num = max_hist_num
        self.__history_lock = _thread.allocate_lock()

    def __read(self):
        """Read history file info.

        Returns:
            dict: history data list.
                data format:
                {
                    "data": [xxx, xxx, xxx]
                }
        """
        res = {"data": []}
        if ql_fs.path_exists(self.__history):
            with open(self.__history, "r") as f:
                try:
                    hist_data = ujson.load(f)
                    if isinstance(hist_data, dict):
                        res["data"] = hist_data.get("data", [])
                except Exception:
                    pass
        return res

    def __write(self, data):
        """Write data to history file

        Args:
            data (dict): history data.
                data format:
                {
                    "data": [xxx, xxx, xxx]
                }

        Returns:
            bool: True - success, False - faliled.
        """
        try:
            with open(self.__history, "w") as f:
                ujson.dump(data, f)
                return True
        except:
            return False

    def read(self):
        """Read history info

        Return:
            data (dict): history data.
                data format:
                {
                    "data": [xxx, xxx, xxx]
                }
        """
        with self.__history_lock:
            res = self.__read()
            self.__write({"data": []})
            return res

    def write(self, data):
        """Data format for write history

        Args:
            data (list): history data list.

        Returns:
            bool: True - success, False - faliled.
        """
        with self.__history_lock:
            res = self.__read()
            res["data"].extend(data)
            if len(res["data"]) > self.__max_hist_num:
                res["data"] = res["data"][self.__max_hist_num * -1:]
            return self.__write(res)

    def clean(self):
        """Remove history file.

        Returns:
            bool: True - success, False - faliled.
        """
        with self.__history_lock:
            try:
                uos.remove(self.__history)
                return True
            except:
                return False
