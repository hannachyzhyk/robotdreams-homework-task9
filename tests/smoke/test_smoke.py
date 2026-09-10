# 1.2. Smoke-тести — 3 бали
# У файлі tests/smoke/test_smoke.py реалізуйте три перевірки базової працездатності пристрою.

import time
import pytest

@pytest.mark.smoke
def test_device_reboot(device):
    assert device.reboot(), "FAIL: Device did not reboot successfully"

@pytest.mark.smoke
def test_device_register(rebooted_device):
    assert rebooted_device.register("user", "correctpass"), \
        "FAIL: Device did not register successfully"

@pytest.mark.smoke
def test_device_login(registered_device):
    assert registered_device.login("user", "correctpass"), \
        "FAIL: Device did not login successfully"

@pytest.mark.smoke
@pytest.mark.xfail(reason="This test fails due to a bug in the device firmware: sensor history returnes 5 row instead of 10", strict=True)
def test_sensor_history(logged_device):
    # Запуск збору даних (очікуємо, що сенссор збере більше 10ти записів)
    logged_device.send_command("config set sensor_interval 500") 
    assert logged_device.wait_for(f"[Config] sensor_interval = 500", timeout=5), \
        f"FAIL: Expected confirmation message for setting key 'sensor_interval' to '500'"
    logged_device.send_command("sensor start")
    assert logged_device.wait_for(f"[Sensor] #11", timeout=7), \
        f"FAIL: Expected at least 11 sensor readings, but did not receive them in time"
    logged_device.send_command("sensor stop")

    # Запит історії
    logged_device.send_command("sensor history")
    response = logged_device.read_lines(timeout=5)
    assert 'History (last 10 readings)' in response, \
        f"FAIL: Expected 'History (last 10 readings)' message in response, but got: \n{response}"

    sensor_lines = [l for l in response if "[Sensor]" in l and "] temp:" in l]
    # Перевірка кількості записів
    assert len(sensor_lines) == 10, f"FAIL: Expected 10 records, but got {len(sensor_lines)}"
    