import uos
import modem
from machine import UART

from usr.modules.location import Location, _loc_method, GPSMatch, GPSParse
from usr.modules.aliyunIot import AliYunIot, AliObjectModel
from usr.modules.remote import RemoteSubscribe

PROJECT_NAME = "QuecPython-AliyunIot"

PROJECT_VERSION = "2.1.0"

DEVICE_FIRMWARE_NAME = uos.uname()[0].split("=")[1]

DEVICE_FIRMWARE_VERSION = modem.getDevFwVersion()


def get_ali_loc_data(loc_method, loc_data):
    res = {"GeoLocation": {}}

    __gps_match = GPSMatch()
    __gps_parse = GPSParse()

    if loc_method == 0x1:
        gga_data = __gps_match.GxGGA(loc_data)
        data = {}
        if gga_data:
            Latitude = __gps_parse.GxGGA_latitude(gga_data)
            if Latitude:
                data["Latitude"] = float("%.2f" % float(Latitude))
            Longtitude = __gps_parse.GxGGA_longtitude(gga_data)
            if Longtitude:
                data["Longtitude"] = float("%.2f" % float(Longtitude))
            Altitude = __gps_parse.GxGGA_altitude(gga_data)
            if Altitude:
                data["Altitude"] = float("%.2f" % float(Altitude))
            if data:
                data["CoordinateSystem"] = 1
        res = {"GeoLocation": data}
    elif loc_method in (0x2, 0x4):
        if loc_data:
            res["GeoLocation"] = {
                "Longtitude": round(loc_data[0], 2),
                "Latitude": round(loc_data[1], 2),
                # "Altitude": 0.0,
                "CoordinateSystem": 1
            }

    return res


class AliCloudConfig(object):
    PK = "a1q1kmZPwU2"
    PS = "HQraBqtV8WsfCEuy"
    DK = "tracker_dev_jack"
    DS = "bfdfcca5075715e8309eff8597663c4b"

    SERVER = "a1q1kmZPwU2.iot-as-mqtt.cn-shanghai.aliyuncs.com"
    client_id = ""
    life_time = 120
    burning_method = 1


def test_aliyuniot():
    res = {"all": 0, "success": 0, "failed": 0}

    cloud_init_params = AliCloudConfig.__dict__
    client_id = cloud_init_params["client_id"] if cloud_init_params.get("client_id") else modem.getDevImei()
    cloud = AliYunIot(
        cloud_init_params["PK"],
        cloud_init_params["PS"],
        cloud_init_params["DK"],
        cloud_init_params["DS"],
        cloud_init_params["SERVER"],
        client_id,
        burning_method=cloud_init_params["burning_method"],
        mcu_name=PROJECT_NAME,
        mcu_version=PROJECT_VERSION,
        firmware_name=DEVICE_FIRMWARE_NAME,
        firmware_version=DEVICE_FIRMWARE_VERSION
    )
    remote_sub = RemoteSubscribe()
    cloud.addObserver(remote_sub)

    ali_om = AliObjectModel()
    msg = "[test_aliyuniot] %s: cloud.set_object_model(%s)."
    assert cloud.set_object_model(ali_om), msg % ("FAILED", ali_om)
    print(msg % ("SUCCESS", ali_om))
    res["success"] += 1

    msg = "[test_aliyuniot] %s: cloud.init()."
    assert cloud.init(), msg % "FAILED"
    print(msg % "SUCCESS")
    res["success"] += 1

    msg = "[test_aliyuniot] %s: get_ali_loc_data(%s, %s) %s."
    loc_method = _loc_method.gps
    gps_mode = 2
    _gps_cfg = {
        "UARTn": UART.UART1,
        "buadrate": 115200,
        "databits": 8,
        "parity": 0,
        "stopbits": 1,
        "flowctl": 0,
    }
    locator_init_params = {'gps_cfg': _gps_cfg}

    locator = Location(gps_mode, locator_init_params)
    loc_data = locator.read(loc_method)
    ali_loc_data = get_ali_loc_data(loc_method, loc_data.get(loc_method))
    assert ali_loc_data["GeoLocation"] != {}, msg % ("FAILED", loc_method, loc_data, ali_loc_data)
    print(msg % ("SUCCESS", loc_method, loc_data, ali_loc_data))
    res["success"] += 1

    msg = "[test_aliyuniot] %s: cloud.post_data(%s)."
    assert cloud.post_data(ali_loc_data), msg % ("FAILED", str(ali_loc_data))
    print(msg % ("SUCCESS", str(ali_loc_data)))
    res["success"] += 1

    msg = "[test_aliyuniot] %s: cloud.ota_request()."
    assert cloud.ota_request(), msg % ("FAILED",)
    print(msg % ("SUCCESS",))
    res["success"] += 1

    msg = "[test_aliyuniot] %s: cloud.device_report()."
    assert cloud.device_report(), msg % ("FAILED",)
    print(msg % ("SUCCESS",))
    res["success"] += 1

    # # PASS: No OTA Plain, ota_action Return False
    # msg = "[test_aliyuniot] %s: cloud.ota_action()."
    # assert cloud.ota_action() is True, msg % ("FAILED",)
    # print(msg % ("SUCCESS",))

    msg = "[test_aliyuniot] %s: cloud.close()."
    assert cloud.close() and cloud.__ali.getAliyunSta() != 0, msg % "FAILED"
    print(msg % "SUCCESS")
    res["success"] += 1

    res["all"] = res["success"] + res["failed"]
    print("[test_aliyuniot] ALL: %s SUCCESS: %s, FAILED: %s." % (res["all"], res["success"], res["failed"]))


if __name__ == '__main__':
    test_aliyuniot()
