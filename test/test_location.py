import osTimer
from machine import UART
from usr.modules.logging import getLogger
from usr.modules.location import Location, GPS, CellLocator, WiFiLocator

log = getLogger(__name__)

# EC600N_CNLB L76K
# _gps_cfg = {
#     "UARTn": UART.UART1,
#     "buadrate": 9600,
#     "databits": 8,
#     "parity": 0,
#     "stopbits": 1,
#     "flowctl": 0,
#     "PowerPin": Pin.GPIO2,
#     "StandbyPin": Pin.GPIO3,
#     "BackupPin": None
# }

# EC600U_CNLB L76K Real Device
# _gps_cfg = {
#     "UARTn": UART.UART2,
#     "buadrate": 9600,
#     "databits": 8,
#     "parity": 0,
#     "stopbits": 1,
#     "flowctl": 0,
#     "PowerPin": Pin.GPIO3,
#     "StandbyPin": None,
#     "BackupPin": None
# }

# EC600N_CNLC LC86L
_gps_cfg = {
    "UARTn": UART.UART1,
    "buadrate": 115200,
    "databits": 8,
    "parity": 0,
    "stopbits": 1,
    "flowctl": 0,
    "PowerPin": None,
    "StandbyPin": None,
    "BackupPin": None
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

gps_mode = 0x1
locator_init_params = {
    "gps_cfg": _gps_cfg,
    "cell_cfg": _cell_cfg,
    "wifi_cfg": _wifi_cfg,
}


def test_gps():
    res = {"all": 0, "success": 0, "failed": 0}

    gps_locator = GPS(_gps_cfg, gps_mode)

    if _gps_cfg["PowerPin"] is not None or gps_mode == 1:
        msg = "[test_gps] %s: GPS.power_switch(0) res: %s."
        power_switch_res = gps_locator.power_switch(0)
        assert power_switch_res, msg % ("FAILED", power_switch_res)
        print(msg % ("SUCCESS", power_switch_res))
        res["success"] += 1

        msg = "[test_gps] %s: GPS.power_switch(1) res: %s."
        power_switch_res = gps_locator.power_switch(1)
        assert power_switch_res, msg % ("FAILED", power_switch_res)
        print(msg % ("SUCCESS", power_switch_res))
        res["success"] += 1

    if _gps_cfg["StandbyPin"] is not None:
        msg = "[test_gps] %s: GPS.standby(1) res: %s."
        standby_res = gps_locator.standby(1)
        assert standby_res, msg % ("FAILED", standby_res)
        print(msg % ("SUCCESS", standby_res))
        res["success"] += 1

        msg = "[test_gps] %s: GPS.standby(0) res: %s."
        standby_res = gps_locator.standby(0)
        assert standby_res, msg % ("FAILED", standby_res)
        print(msg % ("SUCCESS", standby_res))
        res["success"] += 1

    if _gps_cfg["BackupPin"] is not None:
        msg = "[test_gps] %s: GPS.backup(1) res: %s."
        backup_res = gps_locator.backup(1)
        assert backup_res, msg % ("FAILED", backup_res)
        print(msg % ("SUCCESS", backup_res))
        res["success"] += 1

        msg = "[test_gps] %s: GPS.backup(0) res: %s."
        backup_res = gps_locator.backup(0)
        assert backup_res, msg % ("FAILED", backup_res)
        print(msg % ("SUCCESS", backup_res))
        res["success"] += 1

    while True:
        msg = "[test_gps] %s: GPS.read() gps_data: %s."
        gps_data = gps_locator.read()
        # assert gps_data[0] == 0, msg % ("FAILED", gps_data)
        print(msg % ("SUCCESS", gps_data))
        res["success"] += 1
        if gps_data[0] == 0:
            break

    if gps_data[0] == 0 and gps_data[1]:
        msg = "[test_gps] %s: GPS.read_coordinates() gps_coordinates: %s."
        gps_coordinates = gps_locator.read_coordinates(gps_data[1])
        assert gps_coordinates and isinstance(gps_coordinates, tuple), msg % ("FAILED", gps_coordinates)
        print(msg % ("SUCCESS", gps_coordinates))
        res["success"] += 1

    print("[test_gps] ALL: %s SUCCESS: %s, FAILED: %s." % (res["all"], res["success"], res["failed"]))


def test_cell():
    res = {"all": 0, "success": 0, "failed": 0}

    msg = "[test_cell] %s: CellLocator.read() cell_data: %s."
    cell_locator = CellLocator(_cell_cfg)
    cell_data = cell_locator.read()
    assert cell_data[0] == 0, msg % ("FAILED", cell_data)
    print(msg % ("SUCCESS", cell_data))
    res["success"] += 1
    print("[test_cell] ALL: %s SUCCESS: %s, FAILED: %s." % (res["all"], res["success"], res["failed"]))


def test_wifi():
    res = {"all": 0, "success": 0, "failed": 0}

    msg = "[test_wifi] %s: WiFiLocator.read() cell_data: %s."
    wifi_locator = WiFiLocator(_wifi_cfg)
    wifi_data = wifi_locator.read()
    assert wifi_data[0] == 0, msg % ("FAILED", wifi_data)
    print(msg % ("SUCCESS", wifi_data))
    res["success"] += 1
    print("[test_wifi] ALL: %s SUCCESS: %s, FAILED: %s." % (res["all"], res["success"], res["failed"]))


def test_location():
    res = {"all": 0, "success": 0, "failed": 0}

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


run_time = 0


def timer_cb(args):
    global run_time
    run_time += 5


def test_gps_time():
    gps = GPS(_gps_cfg, gps_mode, retry=100)
    # gps.power_switch(0)
    # utime.sleep(1)
    gps.power_switch(1)
    gps_timer = osTimer()
    gps_timer.start(5, 1, timer_cb)
    count = 0
    while count < 1000:
        res = gps.read()
        log.debug("gps.read(): %s" % str(res))
        if res[0] == 0:
            break
        count += 1

    gps_timer.stop()
    global run_time
    log.debug("run_time: %s" % run_time)


if __name__ == "__main__":
    test_gps()
    # test_cell()
    # test_wifi()
    # test_location()
