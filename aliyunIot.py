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

import gc
import uos
import usys as sys
import ujson
import utime
import ql_fs
import _thread
import osTimer
import ubinascii
import app_fota
import app_fota_download
try:
    import fota
except ImportError:
    fota = None
try:
    import uzlib
except ImportError:
    uzlib = None
try:
    import uhashlib
except ImportError:
    uhashlib = None

from misc import Power
from queue import Queue
from aLiYun import aLiYun

from usr.modules.logging import getLogger
from usr.modules.common import option_lock

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


class AliObjectModel:
    """This class is aliyun object model

    Attribute:
        events:
            Attribute:
                - object model event
                - attribute value data format
                {
                    "sos_alert": {
                        local_time: 1651136994000
                    }
                }
        properties:
            Attribute:
                - object model property
                - attribute value data format
                {
                    "GeoLocation": {
                        "Longitude": 0.0,
                        "Latitude": 0.0,
                        "Altitude": 0.0,
                        "CoordinateSystem": 0
                    }
                }
    """

    def __init__(self, om_file="/usr/aliyun_object_model.json"):
        self.om_file = om_file
        if not ql_fs.path_exists(self.om_file):
            raise TypeError("File %s is not exists!" % self.om_file)
        self.events = {}
        self.properties = {}
        self.services = {}
        self.__init_object_model()

    def __get_property(self, om_item):
        _key = om_item["identifier"]
        _type = om_item["dataType"]["type"]
        _prop = {_key: {"type": _type}}
        if _type == "struct":
            _struct = om_item["dataType"]["specs"]
            _prop[_key]["struct"] = {i["identifier"]: {"type": i["dataType"]["type"]} for i in _struct}
        return _prop

    def __init_properties(self, om_properties):
        for om_property in om_properties:
            self.properties.update(self.__get_property(om_property))

    def __init_events(self, om_events):
        for om_event in om_events:
            _key = om_event["identifier"]
            _out_put = om_event.get("outputData", [])
            self.events[_key] = {
                "type": om_event["type"],
            }
            if _out_put:
                self.events[_key]["output"] = {}
                for e in _out_put:
                    self.events[_key]["output"].update(self.__get_property(e))

    def __init_services(self, om_services):
        for om_service in om_services:
            _key = om_service["identifier"]
            _out_put = om_service.get("outputData", [])
            _in_put = om_service.get("inputData", [])
            self.events[_key] = {}
            if _out_put:
                self.events[_key]["output"] = {self.__get_property(om_property) for om_property in _in_put}
            if _in_put:
                self.events[_key]["input"] = {self.__get_property(om_property) for om_property in _in_put}

    def __init_object_model(self):
        with open(self.om_file, "rb") as f:
            cloud_object_model = ujson.load(f)
            self.__init_properties(cloud_object_model.get("properties", []))
            self.__init_events(cloud_object_model.get("events", []))
            self.__init_services(cloud_object_model.get("services", []))


class AliYunIot:
    """This is a class for aliyun iot.

    This class has the following functions:
        1. Cloud connect and disconnect

        2. Publish data to cloud
        2.1 Publish object module
        2.2 Publish ota device info, ota upgrade process, ota plain info request
        2.3 Publish rrpc response

        3. Subscribe data from cloud
        3.1 Subscribe publish object model result
        3.2 Subscribe cloud message
        3.3 Subscribe ota plain
        3.4 Subscribe rrpc request

    Attribute:
        ica_topic_property_post: topic for publish object model property
        ica_topic_property_post_reply: topic for subscribe publish object model property result
        ica_topic_property_set: topic for subscribe cloud object model property set
        ica_topic_event_post: topic for publish object model event
        ica_topic_event_post_reply: topic for subscribe publish object model event result
        ota_topic_device_inform: topic for publish device information
        ota_topic_device_upgrade: topic for subscribe ota plain
        ota_topic_device_progress: topic for publish ota upgrade process
        ota_topic_firmware_get: topic for publish ota plain request
        ota_topic_firmware_get_reply: topic for subscribe ota plain request response
        ota_topic_file_download: topic for publish ota mqtt file download request
        ota_topic_file_download_reply: topic for publish ota mqtt file download request response
        rrpc_topic_request: topic for subscribe rrpc message
        rrpc_topic_response: topic for publish rrpc response

    Run step:
        1. cloud = AliYunIot(pk, ps, dk, ds, server, client_id)
        2. cloud.addObserver(RemoteSubscribe)
        3. cloud.set_object_model(AliObjectModel)
        4. cloud.init()
        5. cloud.post_data(data)
        6. cloud.close()
    """

    def __init__(self, pk, ps, dk, ds, server, client_id, burning_method=0, life_time=120,
                 mcu_name="", mcu_version="", firmware_name="", firmware_version="", reconn=True):
        """Init cloud connect params and topic"""
        self.__pk = pk
        self.__ps = None if burning_method == 1 else ps
        self.__dk = dk
        self.__ds = None if burning_method == 0 else ds
        self.__server = server
        self.__burning_method = burning_method
        self.__life_time = life_time
        self.__mcu_name = mcu_name
        self.__mcu_version = mcu_version
        self.__firmware_name = firmware_name
        self.__firmware_version = firmware_version
        self.__reconn = reconn
        self.__object_model = None
        self.__client_id = client_id if client_id else dk
        self.__callback = print

        self.__ali = None
        self.__post_res = {}
        self.__breack_flag = 0

        self.__id_lock = _thread.allocate_lock()
        self.__init_id_iter()
        self.__init_topic()

        # self.__ota = AliOTA(self, self.__mcu_name, self.__firmware_name)

    def __init_topic(self):
        # module object topic
        self.ica_topic_property_post = "/sys/%s/%s/thing/event/property/post" % (self.__pk, self.__dk)
        self.ica_topic_property_post_reply = "/sys/%s/%s/thing/event/property/post_reply" % (self.__pk, self.__dk)
        self.ica_topic_property_set = "/sys/%s/%s/thing/service/property/set" % (self.__pk, self.__dk)
        self.ica_topic_event_post = "/sys/%s/%s/thing/event/{}/post" % (self.__pk, self.__dk)
        self.ica_topic_event_post_reply = "/sys/%s/%s/thing/event/{}/post_reply" % (self.__pk, self.__dk)
        self.ica_topic_service_sub = "/sys/%s/%s/thing/service/{}" % (self.__pk, self.__dk)
        self.ica_topic_service_pub_reply = "/sys/%s/%s/thing/service/{}_reply" % (self.__pk, self.__dk)

        # OTA topic
        self.ota_topic_device_inform = "/ota/device/inform/%s/%s" % (self.__pk, self.__dk)
        self.ota_topic_device_upgrade = "/ota/device/upgrade/%s/%s" % (self.__pk, self.__dk)
        self.ota_topic_device_progress = "/ota/device/progress/%s/%s" % (self.__pk, self.__dk)
        self.ota_topic_firmware_get = "/sys/%s/%s/thing/ota/firmware/get" % (self.__pk, self.__dk)
        self.ota_topic_firmware_get_reply = "/sys/%s/%s/thing/ota/firmware/get_reply" % (self.__pk, self.__dk)
        # TODO: To Download OTA File For MQTT Association (Not Support Now.)
        self.ota_topic_file_download = "/sys/%s/%s/thing/file/download" % (self.__pk, self.__dk)
        self.ota_topic_file_download_reply = "/sys/%s/%s/thing/file/download_reply" % (self.__pk, self.__dk)

        # RRPC topic
        self.rrpc_topic_request = "/sys/%s/%s/rrpc/request/+" % (self.__pk, self.__dk)
        self.rrpc_topic_response = "/sys/%s/%s/rrpc/response/{}" % (self.__pk, self.__dk)

    def __init_id_iter(self):
        self.__id_iter = iter(range(0xFFFF))

    def __get_id(self):
        """Get message id for publishing data"""
        with self.__id_lock:
            try:
                msg_id = next(self.__id_iter)
            except StopIteration:
                self.__init_id_iter()
                msg_id = next(self.__id_iter)

        return str(msg_id)

    def __put_post_res(self, msg_id, res):
        """Save publish result by message id

        Parameter:
            msg_id: publish message id
            res: publish result, True or False
        """
        self.__post_res[msg_id] = res

    @option_lock(_read_lock)
    def __get_post_res(self, msg_id):
        """Get publish result by message id

        Parameter:
            msg_id: publish message id

        Return:
            True: publish success
            False: publish failed
        """
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

    def __subscribe_topics(self):
        """Subscribe aliyun topic"""
        if not self.subscribe_topic(self.ica_topic_property_post):
            return 1
        if not self.subscribe_topic(self.ica_topic_property_post_reply):
            return 2
        if not self.subscribe_topic(self.ica_topic_property_set):
            return 3
        if not self.subscribe_topic(self.ica_topic_service_sub):
            return 4
        if not self.subscribe_topic(self.ota_topic_device_upgrade):
            return 5
        if not self.subscribe_topic(self.ota_topic_firmware_get_reply):
            return 6
        if not self.subscribe_topic(self.rrpc_topic_request):
            return 7
        res = 7
        for tsl_event_identifier in self.__object_model.events.keys():
            post_topic = self.ica_topic_event_post.format(tsl_event_identifier)
            res += 1
            if not self.subscribe_topic(post_topic):
                return res
            res += 1
            post_reply_topic = self.ica_topic_event_post_reply.format(tsl_event_identifier)
            if not self.subscribe_topic(post_reply_topic):
                return res
        # TODO: To Download OTA File For MQTT Association (Not Support Now.)
        if not self.subscribe_topic(self.ota_topic_file_download_reply):
            res += 1
            return res
        return 0

    def __subscribe_callback(self, topic, data):
        """Aliyun subscribe topic callback

        Parameter:
            topic: topic info
            data: response dictionary info
        """
        topic = topic.decode()
        try:
            data = ujson.loads(data)
        except:
            pass
        log.info("topic: %s, data: %s" % (topic, data))
        if topic.endswith("/post_reply"):
            self.__put_post_res(data["id"], True if data["code"] == 200 else False)
        elif topic.startswith("/ota/device/upgrade/"):
            self.__put_post_res(data["id"], True if int(data["code"]) == 1000 else False)
            # if int(data["code"]) == 1000:
            #     if data.get("data"):
            #         self.__ota.set_ota_info(data["data"])
            #         ota_info = {
            #             "code": 1,
            #             "data": data["data"],
            #         }
        elif topic.endswith("/thing/ota/firmware/get_reply"):
            self.__put_post_res(data["id"], True if int(data["code"]) == 200 else False)
            # if data["code"] == 200:
            #     if data.get("data"):
            #         self.__ota.set_ota_info(data["data"])
            #         ota_info = {
            #             "code": 1,
            #             "data": data["data"],
            #         }
        # TODO: To Download OTA File For MQTT Association (Not Support Now.)
        elif topic.endswith("/thing/file/download_reply"):
            self.__put_post_res(data["id"], True if int(data["code"]) == 200 else False)

        self.__callback((topic, data))

    def __data_format(self, data):
        """Publish data format by AliObjectModel

        Parameter:
            data format:
            {
                "phone_num": "123456789",
                "energy": 100,
                "GeoLocation": {
                    "Longitude": 100.26,
                    "Latitude": 26.86,
                    "Altitude": 0.0,
                    "CoordinateSystem": 1
                },
            }

        Return:
            {
                "event": [
                    {
                        "id": 1,
                        "version": "1.0",
                        "sys": {
                            "ack": 1
                        },
                        "params": {
                            "sos_alert": {
                                "value": {},
                                "time": 1649991780000
                            },
                        },
                        "method": "thing.event.sos_alert.post"
                    }
                ],
                "property": [
                    {
                        "id": 2,
                        "version": "1.0",
                        "sys": {
                            "ack": 1
                        },
                        "params": {
                            "phone_num": {
                                "value": "123456789",
                                "time": 1649991780000
                            },
                            "energy": {
                                "value": 100,
                                "time": 1649991780000
                            },
                        },
                        "method": "thing.event.property.post"
                    }
                ],
                "msg_ids": [1, 2],
                "event_topic": {
                    1: "/sys/{product_key}/{device_key}/thing/event/{event}/post",
                    2: "/sys/{product_key}/{device_key}/thing/event/property/post",
                }
            }
        """
        res = {"property": [], "event": [], "event_topic": {}, "service": [], "service_topic": {}, "msg_ids": []}
        property_params = {}
        event_params = {}
        service_params = {}
        # Format Publish Params.
        for k, v in data.items():
            if self.__object_model.properties.get(k):
                property_params[k] = {
                    "value": v if not isinstance(v, bool) else int(v),
                    "time": utime.mktime(utime.localtime()) * 1000
                }
            elif self.__object_model.events.get(k):
                event_value = {}
                if v:
                    for v_k, v_v in v.items():
                        event_item = self.__object_model.events[k].get("output", {})
                        if v_k in event_item.keys():
                            event_value.update({v_k: v_v})
                        else:
                            log.error("Key %s is not in event %s output. So pass." % (v_k, k))
                event_params[k] = {
                    "value": event_value,
                    "time": utime.mktime(utime.localtime()) * 1000
                }
            elif self.__object_model.services.get(k):
                service_params[k] = v
            else:
                log.error("Publish Key [%s] is not in property and event and service" % k)

        if property_params:
            msg_id = self.__get_id()
            publish_data = {
                "id": msg_id,
                "version": "1.0",
                "sys": {
                    "ack": 1
                },
                "params": property_params,
                "method": "thing.event.property.post"
            }
            res["property"].append(publish_data)
            res["msg_ids"].append(msg_id)

        if event_params:
            for event in event_params.keys():
                topic = self.ica_topic_event_post.format(event)
                msg_id = self.__get_id()
                publish_data = {
                    "id": msg_id,
                    "version": "1.0",
                    "sys": {
                        "ack": 1
                    },
                    "params": event_params[event],
                    "method": "thing.event.%s.post" % event
                }
                res["event"].append(publish_data)
                res["event_topic"][msg_id] = topic
                res["msg_ids"].append(msg_id)

        if service_params:
            """Service params value:
            {
                "id": "123",
                "code": 200,
                "message": "success",
                "data": {
                    "output_data_key": "output_data_val",
                    ...
                }
            }
            """
            for service in service_params.keys():
                topic = self.ica_topic_service_pub_reply.format(service)
                if service_params[service].get("id") is None:
                    log.error("Service %s id is not exists. params: %s" % (service, str(service_params[service])))
                    continue
                msg_id = service_params[service]["id"]
                publish_data = service_params[service]
                publish_data.update({"version": "1.0"})
                res["service"].append(publish_data)
                res["service_topic"][msg_id] = topic
                res["msg_ids"].append(msg_id)

        return res

    @property
    def status(self):
        """Get aliyun connect status

        Return:
            True -- connect success
           False -- connect falied
        """
        try:
            _status = self.__ali.getAliyunSta()
            log.debug("getAliyunSta: %s" % _status)
            return True if _status == 0 else False
        except Exception as e:
            sys.print_exception(e)
            return False

    def set_object_model(self, object_model):
        """Register AliObjectModel to this class"""
        if object_model and isinstance(object_model, AliObjectModel):
            self.__object_model = object_model
            return True
        return False

    def set_callback(self, callback):
        if callable(callback):
            self.__callback = callback
            return True
        return False

    def subscribe_topic(self, topic, qos=0):
        subscribe_res = self.__ali.subscribe(topic, qos=qos) if self.__ali else -1
        log.debug("subscribe_topic %s %s" % (topic, "success" if subscribe_res == 0 else "falied"))
        return True if subscribe_res == 0 else False

    def connect(self):
        """Aliyun connect and subscribe topic

        Return:
            Ture: Success
            False: Failed
        """
        self.__ali = aLiYun(self.__pk, self.__ps, self.__dk, self.__ds, self.__server)
        _res = self.__ali.setMqtt(self.__client_id, clean_session=False, keepAlive=self.__life_time, reconn=True)
        if _res == -1:
            return 1
        self.__ali.setCallback(self.__subscribe_callback)
        _res = self.__subscribe_topics()
        if _res != 0:
            return 2
        self.__ali.start()
        return self.status

    def disconnect(self):
        """Aliyun disconnect"""
        try:
            self.__ali.disconnect()
        except Exception as e:
            sys.print_exception(e)
            log.error("Ali disconnect falied. %s" % e)
        finally:
            self.__post_res = {}
            self.__ali = None
            gc.collect()

        return True

    def objmodel_report(self, data, qos=0):
        """Publish object model property, event

        Parameter:
            data format:
            {
                "phone_num": "123456789",
                "energy": 100,
                "GeoLocation": {
                    "Longitude": 100.26,
                    "Latitude": 26.86,
                    "Altitude": 0.0,
                    "CoordinateSystem": 1
                },
            }

        Return:
            Ture: Success
            False: Failed
        """
        try:
            publish_data = self.__data_format(data)
            # Publish Property Data.
            for item in publish_data["property"]:
                self.__ali.publish(self.ica_topic_property_post, ujson.dumps(item), qos=qos)
            # Publish Event Data.
            for item in publish_data["event"]:
                self.__ali.publish(publish_data["event_topic"][item["id"]], ujson.dumps(item), qos=qos)
            # Publish Service Data.
            for item in publish_data["service"]:
                res = self.__ali.publish(publish_data["service_topic"][item["id"]], ujson.dumps(item), qos=qos)
                log.debug("message_id: %s, res: %s" % (item["id"], res))
                self.__put_post_res(item["id"], res)
            # Wait server response.
            pub_res = [self.__get_post_res(msg_id) for msg_id in publish_data["msg_ids"]]
            return True if False not in pub_res else False
        except Exception as e:
            sys.print_exception(e)
            log.error("AliYun publish failed. data: %s" % str(data))

        return False

    def rrpc_response(self, message_id, data):
        """Publish rrpc response

        Parameter:
            message_id: rrpc request messasge id
            data: response message

        Return:
            Ture: Success
            False: Failed
        """
        topic = self.rrpc_topic_response.format(message_id)
        pub_data = ujson.dumps(data) if isinstance(data, dict) else data
        return self.__ali.publish(topic, pub_data, qos=0) if self.__ali else False

    def device_report(self):
        """Publish mcu and firmware name, version

        Return:
            Ture: Success
            False: Failed
        """
        muc_res = self.ota_device_inform(self.__mcu_version, module=self.__mcu_name)
        fw_res = self.ota_device_inform(self.__firmware_version, module=self.__firmware_name)
        return True if muc_res and fw_res else False

    def ota_request(self):
        """Publish mcu and firmware ota plain request

        Return:
            Ture: Success
            False: Failed
        """
        sota_res = self.ota_firmware_get(self.__mcu_name)
        fota_res = self.ota_firmware_get(self.__firmware_name)
        return True if sota_res and fota_res else False

    def ota_action(self, action, module=None):
        """Publish ota upgrade start or cancel ota upgrade

        Parameter:
            action: confirm or cancel upgrade
                - 0: cancel upgrade
                - 1: confirm upgrade

            module: mcu or firmare model name
                - e.g.: `QuecPython-Tracker`, `EC600N-CNLC`

        Return:
            Ture: Success
            False: Failed
        """
        if not module:
            log.error("Params[module] Is Empty.")
            return False
        if action not in (0, 1):
            log.error("Params[action] Should Be 0 Or 1, Not %s." % action)
            return False

        if action == 1:
            # return self.__ota.start_ota()
            return self.ota_device_progress(step=1, module=module)
        else:
            # self.__ota.set_ota_info("", "", [])
            return self.ota_device_progress(step=-1, desc="User cancels upgrade.", module=module)

        return False

    def ota_device_inform(self, version, module="default"):
        """Publish device information

        Parameter:
            version: module version
                - e.g.: `2.1.0`

            module: mcu or firmare model name
                - e.g.: `QuecPython-Tracker`

        Return:
            Ture: Success
            False: Failed
        """
        msg_id = self.__get_id()
        publish_data = {
            "id": msg_id,
            "params": {
                "version": version,
                "module": module
            }
        }
        publish_res = self.__ali.publish(self.ota_topic_device_inform, ujson.dumps(publish_data), qos=0) if self.__ali else False
        log.debug("version: %s, module: %s, publish_res: %s" % (version, module, publish_res))
        return publish_res

    def ota_device_progress(self, step, desc, module="default"):
        """Publish ota upgrade process

        Parameter:
            step: upgrade process
                - 1 ~ 100: Upgrade progress percentage
                - -1: Upgrade failed
                - -2: Download failed
                - -3: Verification failed
                - -4: Programming failed

            desc: Description of the current step, no more than 128 characters long. If an exception occurs, this field can carry error information.

            module: mcu or firmare model name
                - e.g.: `QuecPython-Tracker`

        Return:
            Ture: Success
            False: Failed
        """
        msg_id = self.__get_id()
        publish_data = {
            "id": msg_id,
            "params": {
                "step": step,
                "desc": desc,
                "module": module,
            }
        }
        publish_res = self.__ali.publish(self.ota_topic_device_progress, ujson.dumps(publish_data), qos=0) if self.__ali else False
        if publish_res:
            return self.__get_post_res(msg_id)
        else:
            log.error("ota_device_progress publish_res: %s" % publish_res)
            return False

    def ota_firmware_get(self, module):
        """Publish ota plain info request

        Parameter:
            module: mcu or firmare model name
                - e.g.: `QuecPython-Tracker`

        Return:
            Ture: Success
            False: Failed
        """
        msg_id = self.__get_id()
        publish_data = {
            "id": msg_id,
            "version": "1.0",
            "params": {
                "module": module,
            },
            "method": "thing.ota.firmware.get"
        }
        publish_res = self.__ali.publish(self.ota_topic_firmware_get, ujson.dumps(publish_data), qos=0) if self.__ali else False
        log.debug("module: %s, publish_res: %s" % (module, publish_res))
        if publish_res:
            return self.__get_post_res(msg_id)
        else:
            log.error("ota_firmware_get publish_res: %s" % publish_res)
            return False

    def ota_file_download(self, fileToken, streamId, fileId, size, offset):
        """Publish mqtt ota plain file info request

        Parameter:
            fileToken: The unique identification Token of the file
            streamId: The unique identifier when downloading the OTA upgrade package through the MQTT protocol.
            fileId: Unique identifier for a single upgrade package file.
            size: The size of the file segment requested to be downloaded, in bytes. The value range is 256 B~131072 B. If it is the last file segment, the value ranges from 1 B to 131072 B.
            offset: The starting address of the bytes corresponding to the file fragment. The value range is 0~16777216.

        Return:
            Ture: Success
            False: Failed
        """
        msg_id = self.__get_id()
        publish_data = {
            "id": msg_id,
            "version": "1.0",
            "params": {
                "fileToken": fileToken,
                "fileInfo": {
                    "streamId": streamId,
                    "fileId": fileId
                },
                "fileBlock": {
                    "size": size,
                    "offset": offset
                }
            }
        }
        publish_res = self.__ali.publish(self.ota_topic_file_download, ujson.dumps(publish_data), qos=0) if self.__ali else False
        if publish_res:
            return self.__get_post_res(msg_id)
        else:
            log.error("ota_file_download publish_res: %s" % publish_res)
            return False


class AliyunIotNew:

    def __init__(self, product_key=None, device_name=None, device_secret=None, product_secret=None, product_id=None,
                 server="iot-as-mqtt.cn-shanghai.aliyuncs.com", qos=1):
        self.__product_key = product_key
        self.__product_secret = product_secret
        self.__device_name = device_name
        self.__device_secret = device_secret
        self.__product_id = product_id
        self.__domain = server
        self.__qos = qos
        self.__cloud = None
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
        except:
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
        subscribe_res = self.__cloud.subscribe(topic, qos=self.__qos) if self.__cloud else -1
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
        res = 5
        for event in self.__events:
            if not self.__subscribe_topic(self.ica_topic_event_post_reply.format(event)):
                res += 1
                break
        if res != 5:
            return res
        res = 5 + len(self.__events)
        for service in self.__services:
            if not self.__subscribe_topic(self.ica_topic_service_sub.format(service)):
                res += 1
                break
        if res == 5 + len(self.__events):
            res = 0
        return res

    @property
    def status(self):
        try:
            _status = self.__cloud.getAliyunSta() if self.__cloud else -1
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
        self.__server = "%s.%s" % (self.__product_key, self.__domain)
        log.debug("self.__product_key: %s" % self.__product_key)
        log.debug("self.__product_secret: %s" % self.__product_secret)
        log.debug("self.__device_name: %s" % self.__device_name)
        log.debug("self.__device_secret: %s" % self.__device_secret)
        log.debug("self.__server: %s" % self.__server)
        self.__cloud = aLiYun(self.__product_key, self.__product_secret, self.__device_name, self.__device_secret, self.__server)
        res = self.__cloud.setMqtt(self.__device_name)
        if res == 0:
            self.__cloud.setCallback(self.__subscribe_callback)
            res = self.__subscribe_topics()
            if res == 0:
                self.__cloud.start()
        return res

    def disconnect(self):
        """Aliyun disconnect"""
        try:
            if self.__cloud:
                self.__cloud.disconnect()
        except Exception as e:
            sys.print_exception(e)
            log.error("Ali disconnect falied. %s" % e)
        finally:
            self.__cloud = None
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
        pub_res = self.__cloud.publish(self.ica_topic_property_post, ujson.dumps(properties), qos=self.__qos) if self.__cloud else -1
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
        pub_res = self.__cloud.publish(self.ica_topic_event_post.format(event), ujson.dumps(properties), qos=self.__qos) if self.__cloud else -1
        return self.__get_post_res(_id) if pub_res is True else False

    def service_response(self, service, code, data, msg_id, message):
        pub_data = {
            "code": code,
            "data": data,
            "id": msg_id,
            "message": message,
            "version": "1.0",
        }
        return self.__cloud.publish(self.ica_topic_service_pub_reply.format(service), ujson.dumps(pub_data), qos=self.__qos) if self.__cloud else False

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
        return self.__cloud.publish(self.rrpc_topic_response.format(msg_id), pub_data, qos=self.__qos) if self.__cloud else False

    def property_set_reply(self, mid, code, msg):
        data = {
            "code": code,
            "data": {},
            "id": mid,
            "message": msg,
            "version": "1.0"
        }
        return self.__cloud.publish(self.ica_topic_property_set_reply, ujson.dumps(data), qos=self.__qos) if self.__cloud else False

    def ota_device_inform(self, version, module):
        _id = self.__id
        publish_data = {
            "id": _id,
            "params": {
                "version": version,
                "module": module
            }
        }
        return self.__cloud.publish(self.ota_topic_device_inform, ujson.dumps(publish_data), qos=self.__qos) if self.__cloud else False

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
        publish_res = self.__cloud.publish(self.ota_topic_firmware_get, ujson.dumps(publish_data), qos=self.__qos) if self.__cloud else False
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
        return self.__cloud.publish(self.ota_topic_device_progress, ujson.dumps(publish_data), qos=self.__qos) if self.__cloud else False


class AliOTA(object):

    def __init__(self, mcu_name=None, firmware_name=None):
        self.__files = []
        self.__module = ""
        self.__version = ""
        self.__aliyuniot = None
        self.__mcu_name = mcu_name
        self.__firmware_name = firmware_name
        self.__fota_queue = Queue(maxsize=4)
        self.__callback = print

        self.__file_hash = None
        self.__tar_file = "sotaFile.tar.gz"
        self.__updater_dir = "/usr/.updater/"
        self.__ota_timer = osTimer()

    def __fota_callback(self, args):
        down_status = args[0]
        down_process = args[1]
        if down_status in (0, 1):
            log.debug("DownStatus: %s [%s][%s%%]" % (down_status, "=" * down_process, down_process))
            if down_process < 100:
                self.__aliyuniot.ota_device_progress(down_process, "Downloading File.", module=self.__module)
            else:
                self.__aliyuniot.ota_device_progress(100, "Download File Over.", module=self.__module)
                self.__set_upgrade_status(3)
                self.__fota_queue.put(True)
        elif down_status == 2:
            self.__aliyuniot.ota_device_progress(100, "Download File Over.", module=self.__module)
            self.__set_upgrade_status(3)
            self.__fota_queue.put(True)
        else:
            log.error("Down Failed. Error Code [%s] %s" % (down_process, FOTA_ERROR_CODE.get(down_process, down_process)))
            self.__aliyuniot.ota_device_progress(-2, FOTA_ERROR_CODE.get(down_process, down_process), module=self.__module)
            self.__fota_queue.put(False)

    def __ota_timer_callback(self, args):
        self.__aliyuniot.ota_device_progress(-1, "Download File Falied.", module=self.__module)
        self.__fota_queue.put(False)

    def __get_file_size(self, data):
        size = data.decode("ascii")
        size = size.rstrip("\0")
        if (len(size) == 0):
            return 0
        size = int(size, 8)
        return size

    def __get_file_name(self, name):
        file_name = name.decode("ascii")
        file_name = file_name.rstrip("\0")
        return file_name

    def __check_md5(self, cloud_md5):
        log.debug("AliOTA __check_md5")
        file_md5 = ubinascii.hexlify(self.__file_hash.digest()).decode("ascii")
        msg = "DMP Calc MD5 Value: %s, Device Calc MD5 Value: %s" % (cloud_md5, file_md5)
        log.debug(msg)
        if (cloud_md5 != file_md5):
            self.__aliyuniot.ota_device_progress(-3, "MD5 Verification Failed. %s" % msg, module=self.__module)
            log.error("MD5 Verification Failed")
            return False

        log.debug("MD5 Verification Success.")
        return True

    def __start_fota(self):
        log.debug("AliOTA __start_fota")
        fota_obj = fota() if fota else None
        url1 = self.__files[0]["url"]
        url2 = self.__files[1]["url"] if len(self.__files) > 1 else ""
        log.debug("AliOTA start httpDownload")
        if url2:
            res = fota_obj.httpDownload(url1=url1, url2=url2, callback=self.__fota_callback) if fota_obj else -1
        else:
            res = fota_obj.httpDownload(url1=url1, callback=self.__fota_callback) if fota_obj else -1
        log.debug("AliOTA httpDownload res: %s" % res)
        if res == 0:
            self.__ota_timer.start(1000 * 3600, 0, self.__ota_timer_callback)
            fota_res = self.__fota_queue.get()
            self.__ota_timer.stop()
            return fota_res
        else:
            self.__set_upgrade_status(4)
            self.__aliyuniot.ota_device_progress(-2, "Download File Failed.", module=self.__module)
            return False

    def __start_sota_tar(self):
        log.debug("AliOTA __start_sota_tar")
        count = 0
        for index, file in enumerate(self.__files):
            if self.__download(file["url"]):
                if self.__check_md5(file["md5"]):
                    if self.__upgrade(self.__unzip()):
                        count += 1
            if index + 1 != count:
                break
        if count == len(self.__files):
            self.__set_upgrade_status(3)
        else:
            self.__set_upgrade_status(4)

        app_fota_download.set_update_flag()
        Power.powerRestart()

    def __start_sota(self):
        log.debug("AliOTA __start_sota")
        app_fota_obj = app_fota.new()
        download_infos = [{"url": i["url"], "file_name": i["file_name"]} for i in self.__files]
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
            self.__aliyuniot.ota_device_progress(100, "Download File Over.", module=self.__module)
            self.__set_upgrade_status(3)
            app_fota_obj.set_update_flag()
            Power.powerRestart()
        else:
            self.__set_upgrade_status(4)
            self.__aliyuniot.ota_device_progress(-2, "Download File Failed.", module=self.__module)

    def __download(self, url):
        log.debug("AliOTA __download")
        res = app_fota_download.download(url, self.__tar_file)
        if res == 0:
            self.__file_hash = uhashlib.md5() if uhashlib else None
            with open(self.__updater_dir + self.__tar_file, "rb+") as fp:
                for fpi in fp.readlines():
                    self.__file_hash.update(fpi)
            return True
        else:
            self.__aliyuniot.ota_device_progress(-2, "Download File Failed.", module=self.__module)
            return False

    def __unzip_size(self, tar_size):
        # TDOO: To Sure unzip size is file size or tar size
        file_size = tar_size * 2
        for i in range(1, 19):
            if file_size <= 1 << i:
                break
        log.debug("__unzip_size file_size: %s, zlibsize: %s" % (file_size, i))
        return i * -1

    def __unzip(self):
        log.debug("AliOTA __unzip")
        file_list = []
        tar_size = uos.stat(self.__updater_dir + self.__tar_file)[-4]
        with open(self.__updater_dir + self.__tar_file, "rb+") as ota_file:
            ota_file.seek(10)
            unzipFp = uzlib.DecompIO(ota_file, self.__unzip_size(tar_size), 1) if uzlib else None
            log.debug("[OTA Upgrade] Unzip file success.")
            try:
                while True:
                    data = unzipFp.read(0x200)
                    if not data:
                        log.debug("[OTA Upgrade] Read file size zore.")
                        break

                    size = self.__get_file_size(data[124:135])
                    file_name = self.__get_file_name(data[:100])
                    log.debug("[OTA Upgrade] File Name: %s, File Size: %s" % (file_name, size))

                    if not size:
                        if len(file_name):
                            log.debug("[OTA Upgrade] Create file: %s" % self.__updater_dir + file_name)
                            ql_fs.mkdirs(self.__updater_dir + file_name)
                        else:
                            log.debug("[OTA Upgrade] Have no file unzip.")
                            break
                    else:
                        log.debug("File %s write size %s" % (self.__updater_dir + file_name, size))
                        with open(self.__updater_dir + file_name, "wb+") as fp:
                            read_size = 0x200
                            last_size = size
                            while last_size > 0:
                                data = unzipFp.read(read_size)
                                write_size = read_size if read_size <= last_size else last_size
                                fp.write(data[:write_size])
                                last_size -= write_size
                            log.debug("file_name: %s, size: %s" % (file_name, size))
                            file_list.append({"file_name": file_name, "size": size})
                log.debug("Remove %s" % (self.__updater_dir + self.__tar_file))
                uos.remove(self.__updater_dir + self.__tar_file)
                app_fota_download.delete_update_file(self.__tar_file)
            except Exception as e:
                sys.print_exception(e)
                err_msg = "Unpack Error: %s" % e
                self.__aliyuniot.ota_device_progress(-4, err_msg, module=self.__module)

        return file_list

    def __upgrade(self, file_list):
        log.debug("AliOTA __upgrade")

        if file_list:
            for file_name in file_list:
                app_fota_download.update_download_stat(self.__updater_dir + file_name["file_name"], "/usr/" + file_name["file_name"], file_name["size"])

            return True
        return False

    def __set_upgrade_status(self, upgrade_status):
        log.debug("__set_upgrade_status upgrade_status %s" % upgrade_status)
        self.__callback(("ota_upgrade_status", upgrade_status))

    def set_aliyuniot(self, aliyuniot):
        if isinstance(aliyuniot, AliYunIot):
            self.__aliyuniot = aliyuniot
            return True
        return False

    def set_firmware(self, mcu_name, firmware_name):
        if mcu_name and firmware_name:
            self.__mcu_name = mcu_name
            self.__firmware_name = firmware_name
            return True
        return False

    def set_ota_info(self, data):
        """
        upgrade_file:
        {
            "files": {
                "upgrade_file_name": "target_full_path_file_name"
            }
        }
        """
        upgrade_file = {}
        self.__module = data["module"]
        if self.__module == self.__mcu_name:
            upgrade_file = data.get("extData", {}).get("_package_udi")
            if upgrade_file:
                upgrade_file = ujson.loads(upgrade_file).get("files", {})
            else:
                log.error("Upgrade file comment is not exists.")
                return
        if data.get("files"):
            files = [{"size": i["fileSize"], "url": i["fileUrl"], "md5": i["fileMd5"], "file_name": upgrade_file.get(i["fileName"], "")} for i in data["files"]]
        else:
            name = ""
            for k, v in upgrade_file.items():
                name = v
                break
            files = [{"size": data["size"], "url": data["url"], "md5": data["md5"], "file_name": name}]
        self.__version = data["version"]
        self.__files = files

    def set_callback(self, callback):
        if callable(callback):
            self.__callback = callback
            return True
        return False

    def start_ota(self):
        log.debug("AliOTA start_ota module %s" % self.__module)
        self.__set_upgrade_status(2)
        if self.__module == self.__firmware_name:
            # self.__start_fota()
            _thread.start_new_thread(self.__start_fota, ())
        elif self.__module == self.__mcu_name:
            # self.__start_sota()
            _thread.start_new_thread(self.__start_sota, ())

        return True
