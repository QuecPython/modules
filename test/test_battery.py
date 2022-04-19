import osTimer

from usr.modules.battery import Battery

run_time = 0


def get_voltage_cb(args):
    global run_time
    run_time += 5


def test_battery():
    res = {"all": 0, "success": 0, "failed": 0}
    battery = Battery()

    temp = 30
    msg = "[test_battery] %s: battery.set_temp(30)."
    assert battery.set_temp(temp) and battery.__temp == temp, msg % "FAILED"
    print(msg % "SUCCESS")
    res["success"] += 1

    timer = osTimer()
    timer.start(5, 1, get_voltage_cb)
    voltage = battery.get_voltage()
    timer.stop()
    global run_time
    print("[test_battery] battery.get_voltage() run_time: %sms" % run_time)
    msg = "[test_battery] %s: battery.get_voltage() %s."
    assert isinstance(voltage, int) and voltage > 0, msg % ("FAILED", voltage)
    print(msg % ("SUCCESS", voltage))
    res["success"] += 1

    energy = battery.get_energy()
    assert isinstance(energy, int) and energy >= 0, "[test_battery] FAILED: battery.get_energy() %s." % energy
    print("[test_battery] SUCCESS: battery.get_energy() is %s." % energy)
    res["success"] += 1

    res["all"] = res["success"] + res["failed"]
    print("[test_battery] ALL: %s SUCCESS: %s, FAILED: %s." % (res["all"], res["success"], res["failed"]))


if __name__ == "__main__":
    test_battery()
