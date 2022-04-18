from machine import UART
from usr.modules.location import Location


def test_location():
    res = {"all": 0, "success": 0, "failed": 0}

    _gps_cfg = {
        "UARTn": UART.UART1,
        "buadrate": 115200,
        "databits": 8,
        "parity": 0,
        "stopbits": 1,
        "flowctl": 0,
    }

    _cell_cfg = {
        "serverAddr": "www.queclocator.com",
        "port": 80,
        "token": "xGP77d2z0i91s67n",
        "timeout": 3,
        "profileIdx": 1,
    }

    _wifi_cfg = {
        "token": "xGP77d2z0i91s67n"
    }

    gps_mode = 0x2
    locator_init_params = {
        "gps_cfg": _gps_cfg,
        "cell_cfg": _cell_cfg,
        "wifi_cfg": _wifi_cfg,
    }

    locator = Location(gps_mode, locator_init_params)
    for loc_method in range(1, 8):
        loc_data = locator.read(loc_method)
        if loc_method & 0x1:
            assert loc_data.get(0x1) not in ("", (), None), "[test_location] FAILED: locator.read(%s) loc_data: %s." % (loc_method, loc_data)
        if loc_method & 0x2:
            assert loc_data.get(0x2) not in ("", (), None), "[test_location] FAILED: locator.read(%s) loc_data: %s." % (loc_method, loc_data)
        if loc_method & 0x4:
            assert loc_data.get(0x4) not in ("", (), None), "[test_location] FAILED: locator.read(%s) loc_data: %s." % (loc_method, loc_data)
        print("[test_location] SUCCESS: locator.read(%s) loc_data: %s." % (loc_method, loc_data))
        res["success"] += 1

    res["all"] = res["success"] + res["failed"]

    print("[test_location] ALL: %s SUCCESS: %s, FAILED: %s." % (res["all"], res["success"], res["failed"]))


if __name__ == '__main__':
    test_location()
