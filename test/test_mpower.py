import utime
from usr.modules.common import Observer
from usr.modules.mpower import LowEnergyManage


class TestLEMObserver(Observer):

    def update(self, observable, *args, **kwargs):
        print("TestLEMObserver update observable: %s" % observable)
        print("TestLEMObserver update args: %s" % str(args))
        print("TestLEMObserver update kwargs: %s" % str(kwargs))
        observable.start()
        return True


def test_low_energy_manage():
    res = {"all": 0, "success": 0, "failed": 0}

    low_energy_manage = LowEnergyManage()
    test_lem_obs = TestLEMObserver()
    low_energy_manage.addObserver(test_lem_obs)

    period = 5
    msg = "[test_low_energy_manage] %s: low_energy_manage.set_period(%s)."
    assert low_energy_manage.set_period(period), msg % ("FAILED", period)
    print(msg % ("SUCCESS", period))
    res["success"] += 1

    msg = "[test_low_energy_manage] %s: low_energy_manage.get_period()."
    assert low_energy_manage.get_period() == period, msg % "FAILED"
    print(msg % "SUCCESS")
    res["success"] += 1

    low_energy_method = "PM"
    msg = "[test_low_energy_manage] %s: low_energy_manage.set_low_energy_method(%s)."
    assert low_energy_manage.set_low_energy_method(low_energy_method), msg % ("FAILED", low_energy_method)
    print(msg % ("SUCCESS", low_energy_method))
    res["success"] += 1

    msg = "[test_low_energy_manage] %s: low_energy_manage.get_low_energy_method()."
    assert low_energy_manage.get_low_energy_method() == low_energy_method, msg % "FAILED"
    print(msg % "SUCCESS")
    res["success"] += 1

    msg = "[test_low_energy_manage] %s: low_energy_manage.low_energy_init()."
    assert low_energy_manage.low_energy_init(), msg % "FAILED"
    print(msg % "SUCCESS")
    res["success"] += 1

    msg = "[test_low_energy_manage] %s: low_energy_manage.get_lpm_fd()."
    assert low_energy_manage.get_lpm_fd() is not None, msg % "FAILED"
    print(msg % "SUCCESS")
    res["success"] += 1

    msg = "[test_low_energy_manage] %s: low_energy_manage.start()."
    assert low_energy_manage.start(), msg % "FAILED"
    print(msg % "SUCCESS")
    res["success"] += 1

    utime.sleep(period * 3 + 1)
    msg = "[test_low_energy_manage] %s: low_energy_manage.stop()."
    assert low_energy_manage.stop(), msg % "FAILED"
    print(msg % "SUCCESS")
    res["success"] += 1

    res["all"] = res["success"] + res["failed"]
    print("[test_low_energy_manage] ALL: %s SUCCESS: %s, FAILED: %s." % (res["all"], res["success"], res["failed"]))


if __name__ == "__main__":
    test_low_energy_manage()
