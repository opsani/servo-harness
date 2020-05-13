import pytest

import sys
import io

from adjust_driver import HarnessDriver, DESC, HAS_CANCEL, VERSION

adjust_json_stdin = '''\
{
    "application": {
        "components": {
            "canary": {
                "settings": {
                    "cpu": {"value": 0.5},
                    "mem": {"value": 0.5}
                }
            }
        }
    }
}
'''

def test_version(monkeypatch):
    with monkeypatch.context() as m:
        # replicate command line arguments fed in by servo
        m.setattr(sys, 'argv', ['', '--version', '1234'])
        driver = HarnessDriver(cli_desc=DESC, supports_cancel=HAS_CANCEL, version=VERSION)
        with pytest.raises(SystemExit) as exit_exception:
            driver.run()
        assert exit_exception.type == SystemExit
        assert exit_exception.value.code == 0

def test_info(monkeypatch):
    with monkeypatch.context() as m:
        # replicate command line arguments fed in by servo
        m.setattr(sys, 'argv', ['', '--info', '1234'])
        driver = HarnessDriver(cli_desc=DESC, supports_cancel=HAS_CANCEL, version=VERSION)
        with pytest.raises(SystemExit) as exit_exception:
            driver.run()
        assert exit_exception.type == SystemExit
        assert exit_exception.value.code == 0

def test_query(monkeypatch):
    with monkeypatch.context() as m:
        # replicate command line arguments fed in by servo
        m.setattr(sys, 'argv', ['', '--query', '1234'])
        driver = HarnessDriver(cli_desc=DESC, supports_cancel=HAS_CANCEL, version=VERSION)
        with pytest.raises(SystemExit) as exit_exception:
            driver.run()
        assert exit_exception.type == SystemExit
        assert exit_exception.value.code == 0

def test_adjust(monkeypatch):
    with monkeypatch.context() as m:
        # replicate command line arguments fed in by servo
        m.setattr(sys, 'argv', ['', '1234'])
        m.setattr(sys, 'stdin', io.StringIO(adjust_json_stdin))
        driver = HarnessDriver(cli_desc=DESC, supports_cancel=HAS_CANCEL, version=VERSION)
        driver.run()
        assert True
