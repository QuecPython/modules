from machine import UART

from usr.modules.location import Location, _loc_method, GPSMatch
from usr.modules.quecthing import QuecThing, QuecObjectModel
from usr.modules.remote import RemoteSubscribe

PROJECT_NAME = "QuecPython-Quecthing"

PROJECT_VERSION = "v2.1.0"


def get_quec_loc_data(loc_method, loc_data):
    __gps_match = GPSMatch()

    if loc_method == 0x1:
        res = {"gps": []}
        r = __gps_match.GxRMC(loc_data)
        if r:
            res["gps"].append(r)

        r = __gps_match.GxGGA(loc_data)
        if r:
            res["gps"].append(r)

        r = __gps_match.GxVTG(loc_data)
        if r:
            res["gps"].append(r)
        return res
    elif loc_method == 0x2:
        return {"non_gps": ["LBS"]}
    elif loc_method == 0x4:
        return {"non_gps": []}


class QuecCloudConfig(object):
    # trackdev0304 (PROENV)
    PK = "p11275"
    PS = "Q0ZQQndaN3pCUFd6"
    DK = "trackdev0304"
    DS = ""
    SERVER = "iot-south.quectel.com:1883"
    life_time = 120


def test_quecthing():
    res = {"all": 0, "success": 0, "failed": 0}

    cloud_init_params = QuecCloudConfig.__dict__
    cloud = QuecThing(
        cloud_init_params["PK"],
        cloud_init_params["PS"],
        cloud_init_params["DK"],
        cloud_init_params["DS"],
        cloud_init_params["SERVER"],
        mcu_name=PROJECT_NAME,
        mcu_version=PROJECT_VERSION
    )
    remote_sub = RemoteSubscribe()
    cloud.addObserver(remote_sub)

    quec_om = QuecObjectModel()
    msg = "[test_quecthing] %s: cloud.set_object_model(%s)."
    assert cloud.set_object_model(quec_om), msg % ("FAILED", quec_om)
    print(msg % ("SUCCESS", quec_om))
    res["success"] += 1

    msg = "[test_quecthing] %s: cloud.init()."
    assert cloud.init(), msg % "FAILED"
    print(msg % "SUCCESS")
    res["success"] += 1

    msg = "[test_quecthing] %s: get_quec_loc_data(%s, %s) %s."
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
    locator_init_params = {"gps_cfg": _gps_cfg}

    locator = Location(gps_mode, locator_init_params)
    loc_data = locator.read(loc_method)
    quec_loc_data = get_quec_loc_data(loc_method, loc_data.get(loc_method))
    assert quec_loc_data != "", msg % ("FAILED", loc_method, loc_data, quec_loc_data)
    print(msg % ("SUCCESS", loc_method, loc_data, quec_loc_data))
    res["success"] += 1

    msg = "[test_quecthing] %s: cloud.post_data(%s)."
    assert cloud.post_data(quec_loc_data), msg % ("FAILED", str(quec_loc_data))
    print(msg % ("SUCCESS", str(quec_loc_data)))
    res["success"] += 1

    msg = "[test_quecthing] %s: cloud.ota_request()."
    assert cloud.ota_request(), msg % ("FAILED",)
    print(msg % ("SUCCESS",))
    res["success"] += 1

    # # PASS: No OTA Plain, ota_action Return False
    # msg = "[test_quecthing] %s: cloud.ota_action()."
    # assert cloud.ota_action() is True, msg % ("FAILED",)
    # print(msg % ("SUCCESS",))

    msg = "[test_quecthing] %s: cloud.close()."
    assert cloud.close(), msg % "FAILED"
    print(msg % "SUCCESS")
    res["success"] += 1

    res["all"] = res["success"] + res["failed"]
    print("[test_quecthing] ALL: %s SUCCESS: %s, FAILED: %s." % (res["all"], res["success"], res["failed"]))


if __name__ == "__main__":
    test_quecthing()
