# 1.4. Тест збереження конфігурації (Persistence) — 3 бали

# Реалізуйте у файлі tests/functional/test_config.py.

import pytest

@pytest.mark.functional
@pytest.mark.parametrize(("key", "set_value1", "set_value2"), 
                         [("sensor_interval", "4000", "5000"), 
                          ("alarm_threshold", "90", "100"),
                          ("dist_threshold", "100", "150")])
def test_config_load_without_reboot(logged_device, key, set_value1, set_value2):
     # Встановлення нового значення
    logged_device.send_command(f"config set {key} {set_value1}")
    assert logged_device.wait_for(f"[Config] {key} = {set_value1}", timeout=5), \
        f"FAIL: Expected confirmation message for setting key '{key}' to '{set_value1}'"
    # Перевірка нового значення
    logged_device.send_command(f"config get {key}")
    assert logged_device.wait_for(f"[Config] {key} = {set_value1}", timeout=5), \
        f"FAIL: Expected set value '{set_value1}' for key '{key}'"

    # Збереження конфігурації
    logged_device.send_command("config save")
    assert logged_device.wait_for(f"[Config] Saved successfully.", timeout=5), \
        f"FAIL: Expected confirmation message for saving config"

    # Встановлення нового значення
    logged_device.send_command(f"config set {key} {set_value2}")
    assert logged_device.wait_for(f"[Config] {key} = {set_value2}", timeout=5), \
        f"FAIL: Expected confirmation message for setting key '{key}' to '{set_value2}'"
    # Перевірка нового значення
    logged_device.send_command(f"config get {key}")
    assert logged_device.wait_for(f"[Config] {key} = {set_value2}", timeout=5), \
        f"FAIL: Expected set value '{set_value2}' for key '{key}'"
    
    # Перевірка завантаження конфігурації встановлює значення, що було збережене коммандою config save
    logged_device.send_command(f"config load")
    assert logged_device.wait_for(f"[Config] Config applied successfully.", timeout=5), \
        f"FAIL: Expected confirmation message for loading config"
    logged_device.send_command(f"config get {key}")
    response = logged_device.read_lines(timeout=5)
    assert any(f"[Config] {key} = {set_value1}" in line for line in response), \
        f"FAIL: Expected loaded value '{set_value1}' for key '{key}', but got: \n{response}"
        
@pytest.mark.xfail(reason="This test fails due to a bug in the device firmware. The device does not persist configuration after reboot.", strict=True)
@pytest.mark.functional
@pytest.mark.parametrize(("key", "set_value"), 
                         [("sensor_interval", "4000"), 
                          ("alarm_threshold", "90"),
                          ("dist_threshold", "100")])
def test_saved_config_load_after_reboot(logged_device, key, set_value):
    # Встановлення нового значення
    logged_device.send_command(f"config set {key} {set_value}")
    assert logged_device.wait_for(f"[Config] {key} = {set_value}", timeout=5), \
        f"FAIL: Expected confirmation message for setting key '{key}' to '{set_value}'"
    # Перевірка нового значення
    logged_device.send_command(f"config get {key}")
    assert logged_device.wait_for(f"[Config] {key} = {set_value}", timeout=5), \
        f"FAIL: Expected set value '{set_value}' for key '{key}'"

    # Збереження конфігурації та перезавантаження пристрою
    logged_device.send_command("config save")
    assert logged_device.wait_for(f"[Config] Saved successfully.", timeout=5), \
        f"FAIL: Expected confirmation message for saving config"
    logged_device.reboot()
    logged_device.register("user", "correctpass")
    logged_device.login("user", "correctpass")
    
    # Перевірка завантаження конфігурації встановлює значення, що було збережене коммандою config save
    logged_device.send_command(f"config load")
    assert logged_device.wait_for(f"[Config] Config applied successfully.", timeout=5), \
        f"FAIL: Expected confirmation message for loading config"
    logged_device.send_command(f"config get {key}")
    response = logged_device.read_lines(timeout=5)
    assert any(f"[Config] {key} = {set_value}" in line for line in response), (
        f"FAIL: Expected loaded value '{set_value}' for key '{key}' after reboot, "
        f"but got: \n{response}"
    )