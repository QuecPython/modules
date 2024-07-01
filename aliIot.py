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
@file      :aliyunIot.py
@author    :Jack Sun (jack.sun@quectel.com)
@brief     :Aliyun server mqtt client.
@version   :1.2.0
@date      :2022-11-24 17:06:30
@copyright :Copyright (c) 2022
"""

import fota
import ujson
import utime
import _thread
import osTimer
import app_fota
import usys as sys
from queue import Queue
from aLiYun import aLiYun

from usr.modules.logging import getLogger

log = getLogger(__name__)

_read_lock = _thread.allocate_lock()

FOTA_ERROR_CODE = {
    1001: "FOTA_DOMAIN_NOT_EXIST",
    1002: "FOTA_DOMAIN_TIMEOUT",
    1003: "FOTA_DOMAIN_UNKNOWN",
    1004: "FOTA_SERVER_CONN_FAIL",
    1005: "FOTA_AUTH_FAILED",
    1006: "FOTA_FILE_NOT_EXIST",
    1007: "FOTA_FILE_SIZE_INVALID",
    1008: "FOTA_FILE_GET_ERR",
    1009: "FOTA_FILE_CHECK_ERR",
    1010: "FOTA_INTERNAL_ERR",
    1011: "FOTA_NOT_INPROGRESS",
    1012: "FOTA_NO_MEMORY",
    1013: "FOTA_FILE_SIZE_TOO_LARGE",
    1014: "FOTA_PARAM_SIZE_INVALID",
}


class AliIot:

    def __init__(self, product_key=None, device_name=None, device_secret=None, product_secret=None,
                 server=None, qos=1):
        self.__product_key = product_key
        self.__product_secret = product_secret if product_secret else None
        self.__device_name = device_name
        self.__device_secret = device_secret if device_secret else None
        self.__domain = server
        self.__qos = qos
        self.__server = "%s.%s" % (self.__product_key, self.__domain)

        if self.__product_secret is None and self.__device_secret is None:
            raise ValueError("Neither product_secret nor device_secret exist.")

        self.__id_lock = _thread.allocate_lock()
        self.__get_post_lock = _thread.allocate_lock()
        self.__callback = None
        self.__post_res = {}
        self.__conn_tag = 0
        self.__init_id_iter()
        self.__events = []
        self.__services = []

    @property
    def __timestamp(self):
        return str(utime.mktime(utime.localtime())) + "000"

    def __init_id_iter(self):
        self.__id_iter = iter(range(0xFFFF))

    @property
    def __id(self):
        """Get message id for publishing data"""
        with self.__id_lock:
            try:
                _id = next(self.__id_iter)
            except StopIteration:
                self.__init_id_iter()
                _id = next(self.__id_iter)

        return str(_id)

    def __put_post_res(self, msg_id, res):
        self.__post_res[msg_id] = res

    def __get_post_res(self, msg_id):
        with self.__get_post_lock:
            count = 0
            while count < int(30 * 1000 / 50):
                if self.__post_res.get(msg_id) is not None:
                    break
                utime.sleep_ms(50)
                count += 1
            if count >= 600 and self.__post_res.get(msg_id) is None:
                self.__post_res[msg_id] = False
            res = self.__post_res.pop(msg_id)
            return res

    def __init_topics(self):
        # module object topic
        self.ica_topic_property_post = "/sys/%s/%s/thing/event/property/post" % (self.__product_key, self.__device_name)
        self.ica_topic_property_post_reply = "/sys/%s/%s/thing/event/property/post_reply" % (self.__product_key, self.__device_name)
        self.ica_topic_property_set = "/sys/%s/%s/thing/service/property/set" % (self.__product_key, self.__device_name)
        self.ica_topic_property_set_reply = "/sys/%s/%s/thing/service/property/set_reply" % (self.__product_key, self.__device_name)
        self.ica_topic_event_post = "/sys/%s/%s/thing/event/{}/post" % (self.__product_key, self.__device_name)
        self.ica_topic_event_post_reply = "/sys/%s/%s/thing/event/{}/post_reply" % (self.__product_key, self.__device_name)
        self.ica_topic_service_sub = "/sys/%s/%s/thing/service/{}" % (self.__product_key, self.__device_name)
        self.ica_topic_service_pub_reply = "/sys/%s/%s/thing/service/{}_reply" % (self.__product_key, self.__device_name)
        # OTA topic
        self.ota_topic_device_inform = "/ota/device/inform/%s/%s" % (self.__product_key, self.__device_name)
        self.ota_topic_device_upgrade = "/ota/device/upgrade/%s/%s" % (self.__product_key, self.__device_name)
        self.ota_topic_device_progress = "/ota/device/progress/%s/%s" % (self.__product_key, self.__device_name)
        self.ota_topic_firmware_get = "/sys/%s/%s/thing/ota/firmware/get" % (self.__product_key, self.__device_name)
        self.ota_topic_firmware_get_reply = "/sys/%s/%s/thing/ota/firmware/get_reply" % (self.__product_key, self.__device_name)
        # RRPC topic
        self.rrpc_topic_request = "/sys/%s/%s/rrpc/request/+" % (self.__product_key, self.__device_name)
        self.rrpc_topic_response = "/sys/%s/%s/rrpc/response/{}" % (self.__product_key, self.__device_name)

    def __subscribe_callback(self, topic, data):
        topic = topic.decode()
        try:
            data = ujson.loads(data)
        except Exception:
            pass
        log.debug("topic: %s, data: %s" % (topic, str(data)))

        if topic.endswith("/post_reply"):
            self.__put_post_res(data["id"], True if int(data["code"]) == 200 else False)
            return
        elif topic.endswith("/thing/ota/firmware/get_reply"):
            self.__put_post_res(data["id"], True if int(data["code"]) == 200 else False)

        if self.__callback and callable(self.__callback):
            self.__callback((topic, data))

    def __subscribe_topic(self, topic):
        subscribe_res = self.__server.subscribe(topic, qos=self.__qos) if self.__server else -1
        log.debug("subscribe_topic %s %s" % (topic, "success" if subscribe_res == 0 else "falied"))
        return True if subscribe_res == 0 else False

    def __subscribe_topics(self):
        self.__init_topics()
        res = 0
        if not self.__subscribe_topic(self.ica_topic_property_post_reply):
            res = 1
        if not self.__subscribe_topic(self.ica_topic_property_set):
            res = 2
        if not self.__subscribe_topic(self.ota_topic_device_upgrade):
            res = 3
        if not self.__subscribe_topic(self.ota_topic_firmware_get_reply):
            res = 4
        if not self.__subscribe_topic(self.rrpc_topic_request):
            res = 5
        _res = 5
        for event in self.__events:
            if not self.__subscribe_topic(self.ica_topic_event_post_reply.format(event)):
                _res += 1
                break
        if _res != 5:
            res = _res
            return res
        _res = 5 + len(self.__events)
        for service in self.__services:
            if not self.__subscribe_topic(self.ica_topic_service_sub.format(service)):
                _res += 1
                break
        if _res > 5 + len(self.__events):
            res = _res
        return res

    @property
    def status(self):
        try:
            _status = self.__server.getAliyunSta() if self.__server else -1
            log.debug("getAliyunSta: %s" % _status)
            return True if _status == 0 else False
        except Exception as e:
            sys.print_exception(e)
            log.error(str(e))
            return False

    @property
    def auth_info(self):
        return {
            "product_key": self.__product_key,
            "product_secret": self.__product_secret,
            "device_name": self.__device_name,
            "device_secret": self.__device_secret
        }

    def add_event(self, event):
        if event not in self.__events:
            self.__events.append(event)
            return True
        return False

    def add_service(self, service):
        if service not in self.__services:
            self.__services.append(service)
            return True
        return False

    def set_callback(self, callback):
        self.__callback = callback

    def connect(self):
        res = -1
        log.debug("self.__product_key: %s" % self.__product_key)
        log.debug("self.__product_secret: %s" % self.__product_secret)
        log.debug("self.__device_name: %s" % self.__device_name)
        log.debug("self.__device_secret: %s" % self.__device_secret)
        log.debug("self.__server: %s" % self.__server)
        self.__server = aLiYun(self.__product_key, self.__product_secret, self.__device_name, self.__device_secret, self.__server)
        res = self.__server.setMqtt(self.__device_name)
        if res == 0:
            self.__server.setCallback(self.__subscribe_callback)
            res = self.__subscribe_topics()
            if res == 0:
                self.__server.start()
        return res

    def disconnect(self):
        """Aliyun disconnect"""
        try:
            if self.__server:
                self.__server.disconnect()
        except Exception as e:
            sys.print_exception(e)
            log.error("Ali disconnect falied. %s" % e)
        finally:
            self.__server = None
        return True

    def properties_report(self, data):
        _timestamp = self.__timestamp
        _id = self.__id
        params = {key: {"value": val, "time": _timestamp} for key, val in data.items()}
        properties = {
            "id": _id,
            "version": "1.0",
            "sys": {
                "ack": 1
            },
            "params": params,
            "method": "thing.event.property.post",
        }
        pub_res = self.__server.publish(self.ica_topic_property_post, ujson.dumps(properties), qos=self.__qos) if self.__server else -1
        return self.__get_post_res(_id) if pub_res is True else False

    def event_report(self, event, data):
        _timestamp = self.__timestamp
        _id = self.__id
        params = {"value": data, "time": _timestamp}
        properties = {
            "id": _id,
            "version": "1.0",
            "sys": {
                "ack": 1
            },
            "params": params,
            "method": "thing.event.%s.post" % event,
        }
        pub_res = self.__server.publish(self.ica_topic_event_post.format(event), ujson.dumps(properties), qos=self.__qos) if self.__server else -1
        return self.__get_post_res(_id) if pub_res is True else False

    def service_response(self, service, code, data, msg_id, message):
        pub_data = {
            "code": code,
            "data": data,
            "id": msg_id,
            "message": message,
            "version": "1.0",
        }
        return self.__server.publish(self.ica_topic_service_pub_reply.format(service), ujson.dumps(pub_data), qos=self.__qos) if self.__server else False

    def rrpc_response(self, msg_id, data):
        """Publish rrpc response

        Parameter:
            msg_id: rrpc request messasge id
            data: response message

        Return:
            Ture: Success
            False: Failed
        """
        pub_data = ujson.dumps(data) if isinstance(data, dict) else data
        return self.__server.publish(self.rrpc_topic_response.format(msg_id), pub_data, qos=self.__qos) if self.__server else False

    def property_set_reply(self, msg_id, code, msg):
        data = {
            "code": code,
            "data": {},
            "id": msg_id,
            "message": msg,
            "version": "1.0"
        }
        return self.__server.publish(self.ica_topic_property_set_reply, ujson.dumps(data), qos=self.__qos) if self.__server else False

    def ota_device_inform(self, version, module):
        _id = self.__id
        publish_data = {
            "id": _id,
            "params": {
                "version": version,
                "module": module
            }
        }
        return self.__server.publish(self.ota_topic_device_inform, ujson.dumps(publish_data), qos=self.__qos) if self.__server else False

    def ota_firmware_get(self, module):
        _id = self.__id
        publish_data = {
            "id": _id,
            "version": "1.0",
            "params": {
                "module": module,
            },
            "method": "thing.ota.firmware.get"
        }
        publish_res = self.__server.publish(self.ota_topic_firmware_get, ujson.dumps(publish_data), qos=self.__qos) if self.__server else False
        log.debug("module: %s, publish_res: %s" % (module, publish_res))
        return self.__get_post_res(_id) if publish_res else False

    def ota_device_progress(self, step, desc, module):
        _id = self.__id
        publish_data = {
            "id": _id,
            "params": {
                "step": step,
                "desc": desc,
                "module": module,
            }
        }
        return self.__server.publish(self.ota_topic_device_progress, ujson.dumps(publish_data), qos=self.__qos) if self.__server else False


class AliIotOTA:

    def __init__(self, project_name, firmware_name):
        self.__project_name = project_name
        self.__firmware_name = firmware_name
        self.__module = None
        self.__version = None
        self.__files = []
        self.__ota_timer = osTimer()
        self.__server = None
        self.__fota_queue = Queue()

    def set_server(self, server):
        if isinstance(server, AliIot):
            self.__server = server

    def set_ota_data(self, data):
        self.__module = data.get("module")
        self.__version = data.get("version")
        if data.get("url"):
            self.__files.append({
                "url": data["url"],
                "md5": data.get("md5"),
                "sign": data.get("sign"),
                "size": data.get("size"),
                "name": "fota.bin",
            })
        elif data.get("files"):
            for i in data["files"]:
                self.__files.append({
                    "url": i.get("fileUrl"),
                    "md5": i.get("fileMd5"),
                    "sign": i.get("fileSign"),
                    "size": i.get("fileSize"),
                    "name": i.get("fileName") if self.__module == self.__firmware_name else i.get("fileName", "").replace(".bin", ".py"),
                })

    def get_ota_info(self):
        return {"ota_module": self.__module, "ota_version": self.__version}

    def start(self):
        # _thread.stack_size(0x2000)
        if self.__module == self.__project_name:
            # _thread.start_new_thread(self.__start_sota, ())
            self.__start_sota()
        elif self.__module == self.__firmware_name:
            # _thread.start_new_thread(self.__start_fota, ())
            self.__start_fota()
        else:
            return False
        return True

    def __start_fota(self):
        log.debug("__start_fota")
        fota_obj = fota()
        url1 = self.__files[0]["url"]
        url2 = self.__files[1]["url"] if len(self.__files) > 1 else ""
        log.debug("start httpDownload")
        if url2:
            res = fota_obj.httpDownload(url1=url1, url2=url2, callback=self.__fota_callback) if fota_obj else -1
        else:
            res = fota_obj.httpDownload(url1=url1, callback=self.__fota_callback) if fota_obj else -1
        log.debug("httpDownload res: %s" % res)
        if res == 0:
            self.__ota_timer.start(600 * 1000, 0, self.__ota_timer_callback)
            fota_res = self.__fota_queue.get()
            self.__ota_timer.stop()
            return fota_res
        else:
            self.__server.ota_device_progress(-2, "Download File Failed.", module=self.__module)
            return False

    def __fota_callback(self, args):
        down_status = args[0]
        down_process = args[1]
        if down_status in (0, 1):
            log.debug("DownStatus: %s [%s][%s%%]" % (down_status, "=" * down_process, down_process))
            if down_process < 100:
                self.__server.ota_device_progress(down_process, "Downloading File.", module=self.__module)
            else:
                self.__server.ota_device_progress(100, "Download File Over.", module=self.__module)
                self.__fota_queue.put(True)
        elif down_status == 2:
            self.__server.ota_device_progress(100, "Download File Over.", module=self.__module)
            self.__fota_queue.put(True)
        else:
            log.error("Down Failed. Error Code [%s] %s" % (down_process, FOTA_ERROR_CODE.get(down_process, down_process)))
            self.__server.ota_device_progress(-2, FOTA_ERROR_CODE.get(down_process, down_process), module=self.__module)
            self.__fota_queue.put(False)

    def __ota_timer_callback(self, args):
        self.__server.ota_device_progress(-1, "Download File Falied.", module=self.__module)
        self.__fota_queue.put(False)

    def __start_sota(self):
        log.debug("__start_sota")
        app_fota_obj = app_fota.new()
        download_infos = [{"url": i["url"], "file_name": i["name"]} for i in self.__files]
        bulk_download_res = app_fota_obj.bulk_download(download_infos)
        log.debug("first bulk_download_res: %s" % str(bulk_download_res))
        count = 0
        while bulk_download_res:
            bulk_download_res = app_fota_obj.bulk_download(bulk_download_res)
            log.debug("[%s]retry bulk_download_res: %s" % (count, str(bulk_download_res)))
            if bulk_download_res:
                count += 1
            if count > 3 and bulk_download_res:
                break
        if not bulk_download_res:
            self.__server.ota_device_progress(100, "Download File Over.", module=self.__module)
            app_fota_obj.set_update_flag()
            return True
        else:
            self.__server.ota_device_progress(-2, "Download File Failed.", module=self.__module)
            return False
