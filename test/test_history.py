import utime
from usr.modules.common import Observable
from usr.modules.history import History


class TestHistObservable(Observable):

    def produce_hist_data(self, local_time):
        hist_data = [{"local_time": local_time}]
        self.notifyObservers(self, *hist_data)


def test_history():
    res = {"all": 0, "success": 0, "failed": 0}

    history = History()
    test_hist_obs = TestHistObservable()
    test_hist_obs.addObserver(history)

    hist_data = [{"test": "test"}]
    assert history.write(hist_data), "[test_history] FAILED: history.write()."
    print("[test_history] SUCCESS: history.write(%s)." % str(hist_data))
    res["success"] += 1

    hist = history.read()
    assert hist.get("data") is not None and isinstance(hist["data"], list), "[test_history] FAILED: history.read() %s." % hist
    print("[test_history] SUCCESS: history.read() is %s." % hist)
    res["success"] += 1

    local_time = utime.mktime(utime.localtime())
    test_hist_obs.produce_hist_data(local_time)
    hist = history.read()
    obs_res = False
    for i in hist.get("data", []):
        if i.get("local_time") == local_time:
            obs_res = True
            break
    assert obs_res, "[test_history] FAILED: history.update() %s." % str(hist)
    print("[test_history] SUCCESS: history.update() %s." % str(hist))
    res["success"] += 1

    assert history.clean(), "[test_history] FAILED: history.clean()."
    print("[test_history] SUCCESS: history.clean().")
    res["success"] += 1

    res["all"] = res["success"] + res["failed"]
    print("[test_history] ALL: %s SUCCESS: %s, FAILED: %s." % (res["all"], res["success"], res["failed"]))


if __name__ == "__main__":
    test_history()
