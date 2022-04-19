from usr.modules.logging import Logger


def test_logger():
    res = {"all": 0, "success": 0, "failed": 0}

    log = Logger("test_logger")
    log.debug("debug Level Log.")
    log.info("info Level Log.")
    log.warn("warn Level Log.")
    log.error("error Level Log.")
    log.critical("critical Level Log.")

    assert log.get_debug() is True, "[test_logger] FAILED: log.get_debug() is not True."
    print("[test_logger] SUCCESS: log.get_debug() is True.")
    res["success"] += 1

    assert log.set_debug(True) is True, "[test_logger] FAILED: log.set_debug(True)."
    print("[test_logger] SUCCESS: log.set_debug(True).")
    res["success"] += 1
    assert log.set_debug(False) is True, "[test_logger] FAILED: log.set_debug(False)."
    print("[test_logger] SUCCESS: log.set_debug(False).")
    res["success"] += 1

    assert log.get_level() == "debug", "[test_logger] FAILED: log.get_level() is not debug."
    print("[test_logger] SUCCESS: log.get_level() is debug.")
    res["success"] += 1

    for level in ("debug", "info", "warn", "error", "critical"):
        assert log.set_level(level) is True and log.get_level() == level, "[test_logger] FAILED: log.set_level(%s)." % level
        print("[test_logger] SUCCESS: log.set_level(%s)." % level)
        res["success"] += 1

    res["all"] = res["success"] + res["failed"]
    print("[test_logger] ALL: %s SUCCESS: %s, FAILED: %s." % (res["all"], res["success"], res["failed"]))


if __name__ == "__main__":
    test_logger()
