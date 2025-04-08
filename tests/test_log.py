import pytest
from crawler.log import log_info, log_warn, log_error

def test_log_info(caplog):
    with caplog.at_level("INFO"):
        log_info("info test")
    assert any("info test" in message for message in caplog.messages)

def test_log_warn(caplog):
    with caplog.at_level("WARNING"):
        log_warn("warn test")
    assert any("warn test" in message for message in caplog.messages)

def test_log_error(caplog):
    with caplog.at_level("ERROR"):
        log_error("error test")
    assert any("error test" in message for message in caplog.messages)

