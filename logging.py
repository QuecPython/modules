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

# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@file      :logging.py
@author    :Jack Sun (jack.sun@quectel.com)
@brief     :Log management.
@version   :1.2.0
@date      :2023-03-22 09:46:51
@copyright :Copyright (c) 2022
"""

import sys
import ql_fs
import _thread
import uos as os
from machine import UART, RTC

_RTC_ = RTC()
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
_log_stream = sys.stdout


class Logger:
    def __init__(self, name):
        self.__name = name

    def __date_time(self):
        _datetime_ = _RTC_.datetime()
        return _datetime_[:3] + _datetime_[4:7]

    def __save_log(self, msg):
        global _log_path, _log_file
        try:
            log_size = 0
            if not ql_fs.path_exists(_log_path):
                os.mkdir(_log_path[:-1])
            if ql_fs.path_exists(_log_file):
                log_size = ql_fs.path_getsize(_log_file)
                if log_size + len(msg) >= _log_size:
                    for i in range(_log_back, 0, -1):
                        bak_file = _log_file + "." + str(i)
                        if ql_fs.path_exists(bak_file):
                            if i == _log_back:
                                os.remove(bak_file)
                            else:
                                os.rename(bak_file, _log_file + "." + str(i + 1))
                    os.rename(_log_file, _log_file + ".1")
            with open(_log_file, "a") as lf:
                lf.write(msg)
        except Exception as e:
            sys.print_exception(e)

    def __log(self, level, *message):
        global _log_save, _log_stream
        with _LOG_LOCK:
            if _log_debug is False:
                if _log_level == "debug" and level == "debug":
                    return
                if _LOG_LEVEL_CODE.get(level) < _LOG_LEVEL_CODE.get(_log_level):
                    return
            _time = "{}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(*self.__date_time())
            msg = "[{}][{}][{}]".format(_time, self.__name, level)
            print(msg, *message, file=_log_stream)
            if _log_save:
                message = [str(message) for i in message if not isinstance(message, str)]
                msg = msg + " " + " ".join(message) if message else msg
                self.__save_log(msg)

    def critical(self, *message):
        self.__log("critical", *message)

    def error(self, *message):
        self.__log("error", *message)

    def warn(self, *message):
        self.__log("warn", *message)

    def info(self, *message):
        self.__log("info", *message)

    def debug(self, *message):
        self.__log("debug", *message)


def getLogger(name):
    global _log_dict
    if not _log_dict.get(name):
        _log_dict[name] = Logger(name)
    return _log_dict[name]


def setLogFile(path, name):
    global _log_path, _log_name, _log_file
    if not path.endswith("/"):
        path += "/"
    _log_path = path
    _log_name = name
    _log_file = _log_path + _log_name
    return 0


def setSaveLog(save, size=None, backups=None):
    global _log_save, _log_size, _log_back
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
    global _log_level
    level = level.lower()
    if level not in _LOG_LEVEL_CODE.keys():
        return False
    _log_level = level
    return True


def setLogDebug(debug):
    global _log_debug
    if isinstance(debug, bool):
        _log_debug = debug
        return True
    return False


def setLogSteam(out):
    global _log_stream
    if isinstance(out, UART) or out in (sys.stdout, sys.stderr):
        _log_stream = out
        return True
    return False
