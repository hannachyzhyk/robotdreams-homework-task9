# Частина 2. Додаткове завдання: тест стабільності датчика — 5 балів
# У файлі tests/functional/test_distance_stability.py реалізуйте тест test_distance_readings_are_stable.
import math
import time
import pytest
import re

@pytest.mark.functional
def test_distance_readings_are_stable(logged_device):
    # Реалізуйте тест, який перевіряє стабільність показників датчика відстані.
    # Тест повинен зчитувати значення відстані кілька разів і перевіряти, що вони не відрізняються більше ніж на 5%.
    logged_device.send_command(f"distance log 500")
    assert logged_device.wait_for(f"Log started.", timeout=5), f"FAIL: Expected confirmation message for starting distance log"

    # Accumulate distance log readings for a specified duration 
    time_for_distance_log_run = 5  # seconds
    deadline = time.time() + time_for_distance_log_run
    responses = []
    while time.time() < deadline:
        response = logged_device.read_lines(timeout=1)
        if response:
            responses.extend([l for l in response if f"DistLog" in l])

    # Stop the distance log
    logged_device.send_command(f"distance log stop")
    assert logged_device.wait_for(f"Log stopped.", timeout=5), f"FAIL: Expected confirmation message for stopping distance log"

    # Get only first float value from each line
    # I (19731) DIST: [Distance] #1 2.8 cm (calibrated: 2.8 cm) -> [2.8, 2.8]
    distance_values = [re.findall(r"\b\d+\.\d+\b", l)[0] for l in responses]
    target = distance_values[0]

    # Math method using math.isclose (rel_tol=0.05 is 5%)
    is_within_range = all(
        math.isclose(float(val), float(target), rel_tol=0.05) for val in distance_values
    )
    assert is_within_range, f"FAIL: Distance readings are not stable. Readings: {distance_values}"
