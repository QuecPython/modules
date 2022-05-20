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

import uos
import _thread

LOWENERGYMAP = {
    "EC200U": [
        "POWERDOWN",
        "PM",
    ],
    "EC600N": [
        "PM",
    ],
    "EC800G": [
        "PM"
    ],
}


def numiter(num=99999):
    """Number generation iterator"""
    return iter(range(num))


def option_lock(thread_lock):
    """Function thread lock decorator"""
    def function_lock(func):
        def wrapperd_fun(*args, **kwargs):
            with thread_lock:
                return func(*args, **kwargs)
        return wrapperd_fun
    return function_lock


class BaseError(Exception):
    """Exception base class"""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Singleton(object):
    """Singleton base class"""
    _instance_lock = _thread.allocate_lock()

    def __init__(self, *args, **kwargs):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            Singleton.instance_dict = {}

        if str(cls) not in Singleton.instance_dict.keys():
            with Singleton._instance_lock:
                _instance = super().__new__(cls)
                Singleton.instance_dict[str(cls)] = _instance

        return Singleton.instance_dict[str(cls)]


class Observer(object):
    """Observer base class"""

    def update(self, observable, *args, **kwargs):
        pass


class Observable(Singleton):
    """Observable base class"""

    def __init__(self):
        self.__observers = []

    def addObserver(self, observer):
        """Add observer"""
        try:
            self.__observers.append(observer)
            return True
        except:
            return False

    def delObserver(self, observer):
        """Delete observer"""
        try:
            self.__observers.remove(observer)
            return True
        except:
            return False

    def notifyObservers(self, *args, **kwargs):
        """Notify observer"""
        for o in self.__observers:
            o.update(self, *args, **kwargs)


class CloudObserver(object):
    """Cloud observer base class"""

    def execute(self, observable, *args, **kwargs):
        pass


class CloudObservable(Singleton):
    """Cloud observable base class"""

    def __init__(self):
        self.__observers = []

    def addObserver(self, observer):
        """Add observer"""
        self.__observers.append(observer)

    def delObserver(self, observer):
        """Delete observer"""
        self.__observers.remove(observer)

    def notifyObservers(self, *args, **kwargs):
        """Notify observer"""
        for o in self.__observers:
            o.execute(self, *args, **kwargs)

    def init(self, enforce=False):
        """Cloud init"""
        pass

    def close(self):
        """Cloud disconnect"""
        pass

    def post_data(self, data):
        """Cloud publish data"""
        pass

    def ota_request(self, *args, **kwargs):
        """Cloud publish ota plain request"""
        pass

    def ota_action(self, action, module=None):
        """Cloud publish ota upgrade or not request"""
        pass


class CloudObjectModel(Singleton):

    def __init__(self, om_file):
        self.om_file = om_file
        if self.__file_exist() is False:
            raise TypeError("File %s is not exists!" % self.om_file)
        self.events = type("events", (object,), {})
        self.properties = type("properties", (object,), {})
        self.services = type("services", (object,), {})

    def __file_exist(self):
        try:
            uos.stat(self.om_file)
            return True
        except:
            return False

    def init(self):
        pass


class DeviceDriversMeta(object):
    pass
