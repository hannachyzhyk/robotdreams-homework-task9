# 1.2. Smoke-тести — 3 бали
# У файлі tests/smoke/test_smoke.py реалізуйте три перевірки базової працездатності пристрою.

import time
import pytest

@pytest.mark.smoke
def test_device_reboot(device):
    assert device.reboot(), "FAIL: Device did not reboot successfully"

@pytest.mark.smoke
def test_device_register(rebooted_device):
    assert rebooted_device.register("user", "correctpass"), "FAIL: Device did not register successfully"

@pytest.mark.smoke
def test_device_login(registered_device):
    assert registered_device.login("user", "correctpass"), "FAIL: Device did not login successfully"

@pytest.mark.smoke
def test_sensor_history(logged_device):
    # Запуск збору даних
    logged_device.send_command("sensor start")
    time.sleep(5)  # Витримка для накопичення понад 8 показань
    logged_device.send_command("sensor stop")

    # Запит історії
    logged_device.send_command("sensor history")
    response = logged_device.read_lines(timeout=5)
    sensor_lines = [l for l in response if "[Sensor]" in l and "] temp:" in l]

    # Перевірка кількості записів
    assert len(sensor_lines) <= 100, f"FAIL: Expected 10 records, but got {len(sensor_lines)}"
    