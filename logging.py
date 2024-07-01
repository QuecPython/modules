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
@brief     :<description>
@version   :1.0.0
@date      :2023-03-22 09:46:51
@copyright :Copyright (c) 2022
"""

import uos
import sys
import utime
import ql_fs
import _thread

__all__ = [
    "CRITICAL", "FATAL", "ERROR", "WARNING", "WARN", "INFO", "DEBUG", "NOTSET",
    "Logger", "getLogger", "setSaveLog", "getSaveLog", "setLogLevel",
    "getLogLevel", "setLogDebug", "getLogDebug",
]

_LOG_LOCK = _thread.allocate_lock()

CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0

_levelToName = {
    CRITICAL: 'CRITICAL',
    ERROR: 'ERROR',
    WARNING: 'WARNING',
    INFO: 'INFO',
    DEBUG: 'DEBUG',
    NOTSET: 'NOTSET',
}

_nameToLevel = {
    'CRITICAL': CRITICAL,
    'FATAL': FATAL,
    'ERROR': ERROR,
    'WARNING': WARNING,
    'WARN': WARN,
    'INFO': INFO,
    'DEBUG': DEBUG,
    'NOTSET': NOTSET,
}

_LOG_DICT = {}
_LOG_PATH = "/usr/"
_LOG_NAME = "project.log"
_LOG_FILE = _LOG_PATH + _LOG_NAME
_LOG_SAVE = False
_LOG_SIZE = 0x8000
_LOG_BACK = 8
_LOG_LEVEL = DEBUG
_LOG_DEBUG = True


class Logger:
    def __init__(self, name):
        self.__name = name
        self.__file = None

    def __open_log(self):
        global _LOG_FILE
        if not self.__file:
            self.__file = open(_LOG_FILE, "wb")

    def __close_log(self):
        if self.__file:
            self.__file.close()
            self.__file = None

    def __write_log(self, msg):
        if self.__file:
            self.__file.write(msg)
            self.__file.flush()

    def __save_log(self, msg):
        try:
            msg += "\n" if not msg.endswith("\n") else ""
            log_size = 0
            if not ql_fs.path_exists(_LOG_PATH):
                uos.mkdir(_LOG_PATH[:-1])
            if ql_fs.path_exists(_LOG_FILE):
                log_size = ql_fs.path_getsize(_LOG_FILE)
                if log_size + len(msg) >= _LOG_SIZE:
                    self.__close_log()
                    for i in range(_LOG_BACK, 0, -1):
                        bak_file = _LOG_FILE + "." + str(i)
                        if ql_fs.path_exists(bak_file):
                            if i == _LOG_BACK:
                                uos.remove(bak_file)
                            else:
                                uos.rename(bak_file, _LOG_FILE + "." + str(i + 1))
                    uos.rename(_LOG_FILE, _LOG_FILE + ".1")
            self.__open_log()
            self.__write_log(msg)
        except Exception as e:
            sys.print_exception(e)

    def __log(self, level, *message):
        with _LOG_LOCK:
            if _LOG_DEBUG is False and ((_LOG_LEVEL == level == DEBUG) or level < _LOG_LEVEL):
                return
            _time = "{}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(*utime.localtime())
            msg = "[{}][{}][{}]".format(_time, self.__name, _levelToName[level])
            print(msg, *message)
            if _LOG_SAVE:
                msg = msg + " " + " ".join(message) if message else msg
                self.__save_log(msg)

    def critical(self, *message):
        self.__log(CRITICAL, *message)

    def fatal(self, *message):
        self.critical(*message)

    def error(self, *message):
        self.__log(ERROR, *message)

    def warning(self, *message):
        self.__log(WARNING, *message)

    def warn(self, *message):
        self.warning(*message)

    def info(self, *message):
        self.__log(INFO, *message)

    def debug(self, *message):
        self.__log(DEBUG, *message)


def getLogger(name):
    global _LOG_DICT
    if not _LOG_DICT.get(name):
        _LOG_DICT[name] = Logger(name)
    return _LOG_DICT[name]


def setSaveLog(save, path=None, name=None, size=None, backups=None):
    global _LOG_SAVE, _LOG_SIZE, _LOG_BACK, _LOG_PATH, _LOG_NAME, _LOG_FILE

    assert isinstance(save, bool), "Args save is not bool"
    if save:
        assert isinstance(size, int) and size > 0, "Args size is not int."
        assert isinstance(backups, int) and backups > 0, "Args backups is not int."

    _LOG_SAVE = save
    path += "/" if not path.endswith("/") else ""
    _LOG_PATH = path
    _LOG_NAME = name
    _LOG_FILE = _LOG_PATH + _LOG_NAME
    _LOG_SIZE = size
    _LOG_BACK = backups
    return True


def getSaveLog():
    return _LOG_SAVE


def setLogLevel(level):
    global _LOG_LEVEL
    if isinstance(level, str) and _nameToLevel.get(level.upper()) is not None:
        _LOG_LEVEL = _nameToLevel.get(level.upper())
        return True
    if isinstance(level, int) and _levelToName.get(level) is not None:
        _LOG_LEVEL = level
        return True
    return False


def getLogLevel():
    return _levelToName.get(_LOG_LEVEL)


def setLogDebug(debug):
    global _LOG_DEBUG
    if isinstance(debug, bool):
        _LOG_DEBUG = debug
        return True
    return False


def getLogDebug():
    return _LOG_DEBUG
