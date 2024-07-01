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

import sys
import ql_fs
import _thread


class History:
    """This class is for manage history file."""

    def __init__(self, hist_file="/usr/tracker_data.hist", bak_num=100):
        """
        Parameter:
            hist_file: filename include full path
            bak_num: history data list max size
        """
        self.__hist_file = hist_file
        self.__bak_num = bak_num
        self.__lock = _thread.allocate_lock()

        if not ql_fs.path_exists(self.__hist_file):
            ql_fs.touch(self.__hist_file, {"data": []})

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
        hist_data = ql_fs.read_json(self.__hist_file)
        return res if not hist_data else hist_data

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
        if "data" in data.keys():
            return True if ql_fs.touch(self.__hist_file, data) == 0 else False

    def read(self):
        """Read history info

        Return:
            data (dict): history data.
                data format:
                {
                    "data": [xxx, xxx, xxx]
                }
        """
        with self.__lock:
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
        with self.__lock:
            res = self.__read()
            res["data"].extend(data)
            res["data"] = res["data"][(self.__bak_num * (-1 if len(res["data"]) > self.__bak_num else 0)):]
            return self.__write(res)

    def clear(self):
        """Clear history file.

        Returns:
            bool: True - success, False - faliled.
        """
        with self.__lock:
            return self.__write({"data": []})


class CacheFile:
    """This class is for caching data to file by bytes.

    This class has one file to save cache informations and cache config.

    Attributes:
        _BYTEORDER_: for config int value save to file convert to bytes.
        _FILE_: cache data save file name.
        _CACHE_CFG_: This dict is default cache config.
            RINDEX: read pointer index.
            WINDEX: write pointer index.
            BLOCK_SIZE: one cache data max block size.
            BAK_NUM: total save cache data numbers.
            RET_HEAD: if save cache data numbers larger than BAK_NUM, than this values is setted 1, for tagging writing over file.
    """

    _BYTEORDER_ = "big"
    _FILE_ = "/usr/cache.bak"
    _CACHE_CFG_ = {
        "RINDEX": 32,
        "WINDEX": 32,
        "BLOCK_SIZE": 64,
        "BAK_NUM": 640,
        "RET_HEAD": 0,
    }

    def __init__(self, cache_cfg=None, filename=None):
        """Init cache cfg and open cache data file."""
        self.cache_cfg = self._CACHE_CFG_ if not cache_cfg else cache_cfg
        self.filename = self._FILE_ if not filename else filename
        self.file = None
        self.lock = _thread.allocate_lock()
        self.open()
        self.__cache_init()

    def __cache_init(self):
        """Init cache config from cache file or _CACHE_CFG_."""
        _exist_ = ql_fs.path_exists(self.filename)
        if _exist_ and self.file.read(32):
            self.__cache_cfg_read()
        else:
            self.__cache_cfg_save()

    def __cache_cfg_save(self):
        self.file.seek(0)
        cache_cfg_bytes = b"".join([self.cache_cfg[key].to_bytes(4, self._BYTEORDER_) for key in self._CACHE_CFG_])
        cache_cfg_bytes += (0).to_bytes(32 - len(cache_cfg_bytes), self._BYTEORDER_)
        self.file.write(cache_cfg_bytes)

    def __cache_cfg_read(self):
        self.file.seek(0)
        [self.cache_cfg.update({key: int.from_bytes(self.file.read(4), self._BYTEORDER_)}) for key in self._CACHE_CFG_]

    def open(self):
        """Open cache data file."""
        with self.lock:
            self.file = open(self.filename, "wb+") if not self.file else self.file

    def read(self, offset=None):
        """Read a block cache data.

        Returns:
            bytes: cache data.
        """
        with self.lock:
            if offset is None:
                if self.cache_cfg["RET_HEAD"] == 0 and self.cache_cfg["RINDEX"] >= self.cache_cfg["WINDEX"]:
                    return b""
                if self.cache_cfg["RET_HEAD"] and self.cache_cfg["RINDEX"] < self.cache_cfg["WINDEX"]:
                    self.cache_cfg["RINDEX"] = self.cache_cfg["WINDEX"]
                if (self.cache_cfg["RINDEX"] + self.cache_cfg["BLOCK_SIZE"]) > (self.cache_cfg["BAK_NUM"] * self.cache_cfg["BLOCK_SIZE"]):
                    self.cache_cfg["RINDEX"] = self._CACHE_CFG_["RINDEX"]
                    self.cache_cfg["RET_HEAD"] = 0
                self.file.seek(self.cache_cfg["RINDEX"])
                data = self.file.read(self.cache_cfg["BLOCK_SIZE"])
                self.cache_cfg["RINDEX"] += self.cache_cfg["BLOCK_SIZE"]
                self.__cache_cfg_save()
                return data
            else:
                self.file.seek(offset)
                data = self.file.read(self.cache_cfg["BLOCK_SIZE"])
                return data

    def write(self, data):
        """Write cache data to cache file.

        Args:
            data (bytes/str): cache data.

        Returns:
            bool: True - success, False - falied.
        """
        with self.lock:
            try:
                # Check data length is large than BLOCK_SIZE.
                assert len(data) > self.cache_cfg["BLOCK_SIZE"], "This data length is %s, larger than BLOCK_SIZE %s" % (len(data), self.cache_cfg["BLOCK_SIZE"])
                # Convert cache data to bytes.
                data = data if isinstance(data, bytes) else (bytes(data) if isinstance(data, bytearray) else (data.encode() if isinstance(data, str) else str(data).encode()))
                # Append zero in cache data end if cache data length is smaller than BLOCK_SIZE
                if len(data) < self.cache_cfg["BLOCK_SIZE"]:
                    data += bytes(bytearray([0] * (self.cache_cfg["BLOCK_SIZE"] - len(data))))
                # If write over file, set WINDEX 0, for tagging file header.
                if (self.cache_cfg["WINDEX"] + self.cache_cfg["BLOCK_SIZE"]) > (self.cache_cfg["BAK_NUM"] * self.cache_cfg["BLOCK_SIZE"]):
                    self.cache_cfg["WINDEX"] = self._CACHE_CFG_["WINDEX"]
                    self.cache_cfg["RET_HEAD"] = 1
                self.file.seek(self.cache_cfg["WINDEX"])
                self.file.write(data)
                self.cache_cfg["WINDEX"] += self.cache_cfg["BLOCK_SIZE"]
                self.cache_cfg["WINDEX"] = self.cache_cfg["WINDEX"]
                self.__cache_cfg_save()
                return True
            except Exception as e:
                sys.print_exception(e)
            return False

    def save(self):
        """Save cache data file.

        Returns:
            bool: True - success, False - falied.
        """
        with self.lock:
            try:
                self.file.flush()
            except Exception as e:
                sys.print_exception(e)
            return False

    def clear(self):
        """Clear cache data by reset cache config pointer."""
        with self.lock:
            self.cache_cfg["WINDEX"] = self._CACHE_CFG_["WINDEX"]
            self.cache_cfg["RINDEX"] = self._CACHE_CFG_["RINDEX"]
            self.cache_cfg["RET_HEAD"] = 0
            self.__cache_cfg_save()

    def close(self):
        """Close cache data file."""
        with self.lock:
            self.file.flush()
            self.file.close()
            self.file = None

    def readable(self):
        """Get cache file is readable.

        Returns:
            bool: True - success, False - falied.
        """
        return not (self.cache_cfg["RET_HEAD"] == 0 and self.cache_cfg["RINDEX"] >= self.cache_cfg["WINDEX"])
