import utime
import osTimer
from machine import UART, Pin
from usr.modules.location import Location
from usr.modules.location import GPS
from usr.modules.logging import getLogger
# from usr.location import Location
# from usr.location import GPS
# from usr.logging import getLogger

log = getLogger(__name__)

# EC600N_CNLB L76K
_gps_cfg = {
    "UARTn": UART.UART1,
    "buadrate": 9600,
    "databits": 8,
    "parity": 0,
    "stopbits": 1,
    "flowctl": 0,
    "PowerPin": Pin.GPIO2,
    "StandbyPin": Pin.GPIO3,
    "BackupPin": None
}

# EC600U_CNLB L76K Real Device
# _gps_cfg = {
#     "UARTn": UART.UART2,
#     "buadrate": 9600,
#     "databits": 8,
#     "parity": 0,
#     "stopbits": 1,
#     "flowctl": 0,
#     "PowerPin": Pin.GPIO3
# }

# EC600N_CNLC LC86L
# _gps_cfg = {
#     "UARTn": UART.UART1,
#     "buadrate": 115200,
#     "databits": 8,
#     "parity": 0,
#     "stopbits": 1,
#     "flowctl": 0,
#     "PowerPin": None,
# }

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


def test_gps():
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


def test_gps_walkup():
    gpio3 = Pin(_gps_cfg["PowerPin"], Pin.OUT, Pin.PULL_PU, 0)
    utime.sleep_ms(500)
    log.debug("gpio3 read: %s" % gpio3.read())
    utime.sleep_ms(500)
    gpio3.write(1)
    utime.sleep_ms(500)
    log.debug("gpio3 read: %s" % gpio3.read())
    test_gps()


if __name__ == "__main__":
    # test_location()
    test_gps()
    # test_gps_walkup()
