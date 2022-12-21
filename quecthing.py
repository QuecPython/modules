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
import usys
import uzlib
import ql_fs
import ujson
import utime
import quecIot
import uhashlib
import ubinascii
import app_fota_download

from misc import Power

from usr.modules.logging import getLogger

log = getLogger(__name__)


EVENT_CODE = {
    1: {
        10200: "Device authentication succeeded.",
        10420: "Bad request data (connection failed).",
        10422: "Device authenticated (connection failed).",
        10423: "No product information found (connection failed).",
        10424: "PAYLOAD parsing failed (connection failed).",
        10425: "Signature verification failed (connection failed).",
        10426: "Bad authentication version (connection failed).",
        10427: "Invalid hash information (connection failed).",
        10430: "PK changed (connection failed).",
        10431: "Invalid DK (connection failed).",
        10432: "PK does not match authentication version (connection failed).",
        10450: "Device internal error (connection failed).",
        10466: "Boot server address not found (connection failed).",
        10500: "Device authentication failed (an unknown exception occurred in the system).",
        10300: "Other errors.",
    },
    2: {
        10200: "Access is successful.",
        10430: "Incorrect device key (connection failed).",
        10431: "Device is disabled (connection failed).",
        10450: "Device internal error (connection failed).",
        10471: "Implementation version not supported (connection failed).",
        10473: "Abnormal access heartbeat (connection timed out).",
        10474: "Network exception (connection timed out).",
        10475: "Server changes.",
        10476: "Abnormal connection to AP.",
        10500: "Access failed (an unknown exception occurred in the system).",
    },
    3: {
        10200: "Subscription succeeded.",
        10300: "Subscription failed.",
    },
    4: {
        10200: "Transparent data sent successfully.",
        10210: "Object model data sent successfully.",
        10220: "Positioning data sent successfully.",
        10300: "Failed to send transparent data.",
        10310: "Failed to send object model data.",
        10320: "Failed to send positioning data.",
    },
    5: {
        10200: "Receive transparent data.",
        10210: "Receive data from the object model.",
        10211: "Received object model query command.",
        10473: "Received data but the length exceeds the module buffer limit, receive failed.",
        10428: "The device receives too much buffer and causes current limit.",
    },
    6: {
        10200: "Logout succeeded (disconnection succeeded).",
    },
    7: {
        10700: "New OTA plain.",
        10701: "The module starts to download.",
        10702: "Package download.",
        10703: "Package download complete.",
        10704: "Package update.",
        10705: "Firmware update complete.",
        10706: "Failed to update firmware.",
        10707: "Received confirmation broadcast.",
    },
    8: {
        10428: "High-frequency messages on the device cause current throttling.",
        10429: "Exceeds the number of activations per device or daily requests current limit.",
    }
}


class QuecObjectModel:

    def __init__(self, file="/usr/quec_object_model.json"):
        self.__file = file
        if not ql_fs.path_exists(self.__file):
            raise ValueError("File %s is not exists!" % self.__file)
        self.__events = {}
        self.__services = {}
        self.__properties = {}
        self.__id_code = {}
        self.__init_object_model()

    def __init_properties(self, properties):
        for _property in properties:
            self.__properties[_property["code"]] = {
                "id": _property["id"],
                "struct": {
                    "id_code": {},
                    "code_id": {},
                }
            }
            self.__id_code[_property["id"]] = _property["code"]
            if _property["dataType"].lower() == "struct":
                struct = _property["specs"]
                id_code = {i["id"]: i["code"] for i in struct}
                code_id = {i["code"]: i["id"] for i in struct}
                self.__properties[_property["code"]]["struct"]["id_code"] = id_code
                self.__properties[_property["code"]]["struct"]["code_id"] = code_id

    def __init_struct(self, items):
        # properties_id = [int(i["$ref"].split("/")[-1]) for i in items]
        # return {self.__id_code[_id]: self.__properties[self.__id_code[_id]] for _id in properties_id}
        _struct = {}
        for i in items:
            if i.get("$ref"):
                _id = int(i["$ref"].split("/")[-1])
                _struct[self.__id_code[_id]] = self.__properties[self.__id_code[_id]]
            elif i.get("id") and i.get("code"):
                _struct[i["code"]] = {
                    "id": i["id"],
                    "struct": {
                        "id_code": {},
                        "code_id": {},
                    }
                }
                if i["dataType"].lower() == "struct":
                    _struct_ = i["specs"]
                    id_code = {i["id"]: i["code"] for i in _struct_}
                    code_id = {i["code"]: i["id"] for i in _struct_}
                    _struct[i["code"]]["struct"]["id_code"] = id_code
                    _struct[i["code"]]["struct"]["code_id"] = code_id
            else:
                log.error("Can not parse data: %s" % str(i))
        return _struct

    def __init_events(self, events):
        for event in events:
            self.__events[event["code"]] = {
                "id": event["id"],
                "output": {}
            }
            _output = event.get("outputData", [])
            self.__events[event["code"]]["output"] = self.__init_struct(_output)

    def __init_services(self, services):
        for service in services:
            self.__services[service["code"]] = {
                "id": service["id"],
                "output": {},
                "input": {}
            }
            _output = service.get("outputData", [])
            self.__services[service["code"]]["output"] = self.__init_struct(_output)
            _input = service.get("inputData", [])
            self.__services[service["code"]]["input"] = self.__init_struct(_input)
            self.__id_code[service["id"]] = service["code"]

    def __init_object_model(self):
        with open(self.__file, "rb") as f:
            _obj_model = ujson.load(f)
            self.__init_properties(_obj_model.get("properties", []))
            self.__init_events(_obj_model.get("events", []))
            self.__init_services(_obj_model.get("services", []))

    def convert_to_server(self, data):
        _data = {}
        for k, v in data.items():
            if k in self.__properties.keys():
                _data[self.__properties[k]["id"]] = v
                if self.__properties[k]["struct"]["code_id"]:
                    __v = {}
                    for _k, _v in v.items():
                        if _k in self.__properties[k]["struct"]["code_id"].keys():
                            __v[self.__properties[k]["struct"]["code_id"][_k]] = _v
                    _data[self.__properties[k]["id"]] = __v
            elif k in self.__events.keys():
                _data[self.__events[k]["id"]] = v
                __v = {}
                for _k, _v in v.items():
                    if _k in self.__events[k]["output"].keys():
                        __v[self.__events[k]["output"][_k]["id"]] = _v
                _data[self.__events[k]["id"]] = __v
            elif k in self.__services.keys():
                _data[self.__services[k]["id"]] = v
                __v = {}
                for _k, _v in v.items():
                    if _k in self.__events[k]["output"].keys():
                        __v[self.__services[k]["output"][_k]["id"]] = _v
                _data[self.__services[k]["id"]] = __v
            else:
                log.warn("Key[%s] Value[%s] is not compare." % (k, v))
        return _data

    def convert_to_client(self, data):
        _data = {
            "property": {},
            "service": {},
        }
        for k, v in data.items():
            code = self.__id_code.get(k)
            if code:
                if self.__properties.get(code):
                    _data["property"][code] = v
                    if isinstance(v, dict):
                        __v = {}
                        for _k, _v in v.items():
                            __v[self.__properties[code]["struct"]["id_code"][_k]] = _v
                        _data["property"][code] = __v
                elif self.__services.get(code):
                    _data["service"][code] = v
                    # TODO: Parse servier value if value is dict.
            else:
                log.error("Key[%s] Value[%s] is not compare." % (k, v))
        return _data

    @property
    def id_code(self):
        return self.__id_code


class QuecThing:

    def __init__(self, pk, ps, dk, ds, mode=1, server="iot-south.quectel.com:1883", life_time=120, fw_name="", fw_version=""):
        self.__pk = pk
        self.__ps = ps
        self.__dk = dk
        self.__ds = ds
        self.__mode = mode
        self.__server = server
        self.__life_time = life_time
        self.__fw_name = fw_name
        self.__fw_version = fw_version
        self.__callback = None
        self.__report_res = {}

    def __event_callback(self, args):
        _data = ()
        event, errcode = args[:2]
        data = args[2] if len(args) > 2 else b""
        log.debug("Event[%s] ErrCode[%s] Data[%s]" % (event, errcode, data))
        if event in (1, 2, 3, 6):
            if errcode == 10200:
                msg = ""
                if event == 1:
                    msg = "Device authentication succeeded."
                elif event == 2:
                    msg = "Access is successful."
                elif event == 3:
                    msg = "Subscription succeeded."
                elif event == 6:
                    msg = "Logout succeeded (disconnection succeeded)."
                log.debug(msg)
        if event == 4:
            if errcode == 10200:
                self.__set_report_res(0, True)
            elif errcode == 10300:
                self.__set_report_res(0, False)
            elif errcode == 10210:
                self.__set_report_res(1, True)
            elif errcode == 10310:
                self.__set_report_res(1, False)
            elif errcode == 10220:
                self.__set_report_res(2, True)
            elif errcode == 10320:
                self.__set_report_res(2, False)
        if event in (5, 7):
            _data = (event, errcode, data)
            if self.__callback:
                self.__callback(_data)

    def __get_device_secret(self):
        if self.__dk and not self.__ds:
            retry = 0
            while retry < 5:
                if self.status:
                    dk_ds = quecIot.getDkDs()
                    if dk_ds:
                        self.__dk, self.__ds = dk_ds
                        break
                retry += 1
                utime.sleep(1)

    def __get_report_res(self, mode):
        report_res = False
        retry = 0
        while retry < 10:
            if mode in self.__report_res.keys():
                report_res = self.__report_res.pop(mode)
                break
            retry += 1
            utime.sleep(1)

        return report_res

    def __set_report_res(self, mode, res):
        self.__report_res[mode] = res

    @property
    def status(self):
        ws = quecIot.getWorkState()
        cm = quecIot.getConnmode()
        log.debug("QuecIot WorkState[%s] ConnMode[%s]" % (ws, cm))
        return True if ws == 8 and cm == 1 else False

    @property
    def device_secret(self):
        return self.__ds

    def set_callback(self, callback):
        if callable(callback):
            self.__callback = callback
            return True
        return False

    def connect(self):
        if not quecIot.init():
            return 1
        if not quecIot.setEventCB(self.__event_callback):
            return 2
        if not quecIot.setProductinfo(self.__pk, self.__ps):
            return 3
        if self.__dk:
            if not quecIot.setDkDs(self.__dk, self.__ds):
                return 4
        if not quecIot.setServer(self.__mode, self.__server):
            return 5
        if not quecIot.setLifetime(self.__life_time):
            return 6
        if not quecIot.setMcuVersion(self.__fw_name, self.__fw_version):
            return 7
        if not quecIot.setConnmode(1):
            return 8

        self.__get_device_secret()
        utime.sleep_ms(200)
        return self.status

    def disconnect(self):
        return quecIot.setConnmode(0)

    def objmodel_report(self, data, qos=2):
        res = quecIot.phymodelReport(qos, data)
        return self.__get_report_res(1) if res else False

    def loc_report(self, data, mode="gps"):
        res = False
        if mode == "gps":
            res = quecIot.locReportOutside(data)
        else:
            res = quecIot.locReportInside(data)
        return self.__get_report_res(2) if res else False

    def device_report(self):
        return quecIot.devInfoReport([i for i in range(1, 13)])

    def ota_search(self, mode=0):
        return quecIot.otaRequest(mode) if mode in (0, 1) else False

    def ota_action(self, action=0):
        return quecIot.otaAction(action) if action in range(4) else False


class QuecOTA:

    def __init__(self):
        self.__ota_file = "/usr/sotaFile.tar.gz"
        self.__updater_dir = "/usr/.updater/usr/"
        self.__file_hash = uhashlib.md5()
        self.__file_size = 0
        self.__file_md5 = ""
        self.__download_size = 0

    def __write_ota_file(self, data):
        with open(self.__ota_file, "ab+") as fp:
            fp.write(data)
            self.__file_hash.update(data)

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

    def __check_md5(self):
        file_md5 = ubinascii.hexlify(self.__file_hash.digest()).decode("ascii")
        log.debug("DMP Calc MD5 Value: %s, Device Calc MD5 Value: %s" % (self.__file_md5, file_md5))
        if (self.__file_md5 != file_md5):
            log.error("MD5 Verification Failed")
            return False

        log.debug("MD5 Verification Success.")
        return True

    def __download(self, start_addr, piece_size):
        res = 2
        readsize = 4096
        while piece_size > 0:
            readsize = readsize if readsize <= piece_size else piece_size
            updateFile = quecIot.mcuFWDataRead(start_addr, readsize)
            self.__write_ota_file(updateFile)
            log.debug("Download File Size: %s" % readsize)
            piece_size -= readsize
            start_addr += readsize
            self.__download_size += readsize
            if (self.__download_size == self.__file_size):
                log.debug("File Download Success, Update Start.")
                res = 3
                quecIot.otaAction(res)
                break
            else:
                quecIot.otaAction(res)

        return res

    def __upgrade(self):
        with open(self.__ota_file, "rb+") as ota_file:
            ota_file.seek(10)
            unzipFp = uzlib.DecompIO(ota_file, -15, 1)
            log.debug("[OTA Upgrade] Unzip file success.")
            ql_fs.mkdirs(self.__updater_dir)
            file_list = []
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
                            file_list.append({"file_name": "/usr/" + file_name, "size": size})

                for file_name in file_list:
                    app_fota_download.update_download_stat("/usr/.updater" + file_name["file_name"], file_name["file_name"], file_name["size"])

                log.debug("Remove %s" % self.__ota_file)
                uos.remove(self.__ota_file)

                app_fota_download.set_update_flag()
            except Exception as e:
                usys.print_exception(e)
                return False

        return True

    def set_ota_info(self, size, md5):
        self.__file_size = size
        self.__file_md5 = md5

    def start_ota(self, start_addr, piece_size):
        ota_download_res = self.__download(start_addr, piece_size)
        if ota_download_res == 3:
            if self.__check_md5():
                if self.__upgrade():
                    log.debug("File Update Success, Power Restart.")
                else:
                    log.debug("File Update Failed, Power Restart.")

        Power.powerRestart()
