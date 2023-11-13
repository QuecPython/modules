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
@file      :logging.py
@author    :Jack Sun (jack.sun@quectel.com)
@brief     :Log management.
@version   :1.2.0
@date      :2022-11-24 17:06:30
@copyright :Copyright (c) 2022
"""

import uos
import utime
import ql_fs
import _thread
import usys as sys

_LOG_LOCK = _thread.allocate_lock()
_LOG_LEVEL_CODE = {
    "debug": 0,
    "info": 1,
    "warn": 2,
    "error": 3,
    "critical": 4,
}

_log_dict = {}
_log_path = "/usr/log/"
_log_name = "tracker.log"
_log_file = _log_path + _log_name
_log_save = False
_log_size = 0x2000
_log_back = 8
_log_level = "debug"
_log_debug = True


class Logger:
    """This class is for show log message."""
    def __init__(self, name):
        self.__name = name

    def __save_log(self, msg):
        """Save log message to local file.

        Args:
            msg (str): log message.
        """
        global _log_path, _log_file
        try:
            log_size = 0
            if not ql_fs.path_exists(_log_path):
                uos.mkdir(_log_path[:-1])
            if ql_fs.path_exists(_log_file):
                log_size = ql_fs.path_getsize(_log_file)
                if log_size + len(msg) >= _log_size:
                    for i in range(_log_back, 0, -1):
                        bak_file = _log_file + "." + str(i)
                        if ql_fs.path_exists(bak_file):
                            if i == _log_back:
                                uos.remove(bak_file)
                            else:
                                uos.rename(bak_file, _log_file + "." + str(i + 1))
                    uos.rename(_log_file, _log_file + ".1")
            with open(_log_file, "a") as lf:
                lf.write(msg)
        except Exception as e:
            sys.print_exception(e)

    def __log(self, level, *message):
        """Show log message to screen.

        Args:
            level (str): level name.
            message (tuple): message items.
        """
        global _log_save
        with _LOG_LOCK:
            if _log_debug is False:
                if _log_level == "debug" and level == "debug":
                    return
                if _LOG_LEVEL_CODE.get(level) < _LOG_LEVEL_CODE.get(_log_level):
                    return

            _time = "{}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(*utime.localtime())
            msg = "[{}][{}][{}]".format(_time, self.__name, level)
            print(msg, *message)
            if _log_save:
                msg = (msg + " " + " ".join(message)) if message else msg
                self.__save_log(msg)

    def critical(self, *message):
        """Show critical level log.

        Args:
            message (tuple): message items.
        """
        self.__log("critical", *message)

    def error(self, *message):
        """Show error level log.

        Args:
            message (tuple): message items.
        """
        self.__log("error", *message)

    def warn(self, *message):
        """Show warn level log.

        Args:
            message (tuple): message items.
        """
        self.__log("warn", *message)

    def info(self, *message):
        """Show info level log.

        Args:
            message (tuple): message items.
        """
        self.__log("info", *message)

    def debug(self, *message):
        """Show debug level log.

        Args:
            message (tuple): message items.
        """
        self.__log("debug", *message)


def getLogger(name):
    """Get Logger object by name.

    Args:
        name (str): log object name, default use file name.

    Returns:
        object: Logger object.
    """
    global _log_dict
    if not _log_dict.get(name):
        _log_dict[name] = Logger(name)
    return _log_dict[name]


def setLogSave(save, path, name, size=None, backups=None):
    """Set project log save onff, file size, backup file counts.

    [description]

    Args:
        save (bool): True - save log to file, False - not save log to file.
        path (str): Log file path.
        name (str): Log file name.
        size (int): Log file max size. (default: `None`)
        backups (int): Log file max backup count. (default: `None`)

    Returns:
        tuple: set result.
            (result code, result message)
            result code:
                0 - success.
                1 - save args error.
                2 - size args error.
                3 - backups args error.
            result message:
                error message.
    """
    global _log_save, _log_path, _log_name, _log_file, _log_size, _log_back
    if not path.endswith("/"):
        path += "/"
    _log_path = path
    _log_name = name
    _log_file = _log_path + _log_name

    if not isinstance(save, bool):
        return (1, "save is not bool.")
    _log_save = save
    if _log_save:
        if not isinstance(size, int):
            return (2, "size is not int.")
        _log_size = size
        if not isinstance(backups, int):
            return (3, "backups is not int.")
        _log_back = backups
    return (0, "success.")


def setLogLevel(level):
    """Set project log level.

    Args:
        level (str): Log level.

    Returns:
        bool: True - success, False - failed.
    """
    global _log_level
    level = level.lower()
    if level not in _LOG_LEVEL_CODE.keys():
        return False
    _log_level = level
    return True


def setLogDebug(debug):
    """Set project log debug.

    Args:
        debug (bool): Log debug.

    Returns:
        bool: True - success, False - failed.
    """
    global _log_debug
    if isinstance(debug, bool):
        _log_debug = debug
        return True
    return False
