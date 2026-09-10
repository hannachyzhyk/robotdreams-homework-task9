# 1.3. Функціональні тести з параметризацією — 4 бали

# У файлі tests/functional/test_alarm.py реалізуйте параметризовані тести.

import pytest

@pytest.mark.functional
@pytest.mark.parametrize("command", ["alarm arm", "alarm disarm", "alarm status", "alarm clear"])
def test_alarm_with_unauthorized_user(rebooted_device, command):
    rebooted_device.send_command(command)
    assert rebooted_device.wait_for("Access denied", timeout=5), \
        f"FAIL: Expected 'Access denied' message for command '{command}'"
