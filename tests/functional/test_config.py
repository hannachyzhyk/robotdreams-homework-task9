# 1.4. Тест збереження конфігурації (Persistence) — 3 бали

# Реалізуйте у файлі tests/functional/test_config.py.

import pytest

# Ключ	Тип	Діапазон	За замовчуванням	Опис
# sensor_interval	int (мс)	500..60000	3000	Інтервал між показаннями сенсора
# alarm_threshold	int	0..10000	80	Поріг спрацювання сигналізації (temp mode)
# dist_threshold	int (см)	1..400	50	Поріг відстані для датчика HC-SR04
@pytest.mark.functional
@pytest.mark.parametrize(("key", "default_value", "set_value1", "set_value2"), 
                         [("sensor_interval", "3000", "4000", "5000"), 
                          ("alarm_threshold", "80", "90", "100"),
                          ("dist_threshold", "50", "100", "150")])
def test_config_load(logged_device, key, default_value, set_value1, set_value2):
    # Перевірка значення за замовчуванням
    logged_device.send_command(f"config get {key}")
    assert logged_device.wait_for(f"[Config] {key} = {default_value}", timeout=5), f"FAIL: Expected default value '{default_value}' for key '{key}'"
    # Встановлення нового значення
    logged_device.send_command(f"config set {key} {set_value1}")
    assert logged_device.wait_for(f"[Config] {key} = {set_value1}", timeout=5), f"FAIL: Expected confirmation message for setting key '{key}' to '{set_value1}'"
    # Перевірка нового значення
    logged_device.send_command(f"config get {key}")
    assert logged_device.wait_for(f"[Config] {key} = {set_value1}", timeout=5), f"FAIL: Expected set value '{set_value1}' for key '{key}'"

    # Збереження конфігурації та перезавантаження пристрою
    logged_device.send_command("config save")
    assert logged_device.wait_for(f"[Config] Saved successfully.", timeout=5), f"FAIL: Expected confirmation message for saving config"

    # Встановлення нового значення
    logged_device.send_command(f"config set {key} {set_value2}")
    assert logged_device.wait_for(f"[Config] {key} = {set_value2}", timeout=5), f"FAIL: Expected confirmation message for setting key '{key}' to '{set_value2}'"
    # Перевірка нового значення
    logged_device.send_command(f"config get {key}")
    assert logged_device.wait_for(f"[Config] {key} = {set_value2}", timeout=5), f"FAIL: Expected set value '{set_value2}' for key '{key}'"
    
    # Перевірка завантаження конфігурації встановлює значення, що було збережене коммандою config save
    logged_device.send_command(f"config load")
    assert logged_device.wait_for(f"[Config] Config applied successfully.", timeout=5), f"FAIL: Expected confirmation message for loading config"
    logged_device.send_command(f"config get {key}")
    assert logged_device.wait_for(f"[Config] {key} = {set_value1}", timeout=5), f"FAIL: Expected loaded value '{set_value1}' for key '{key}' after reboot"
