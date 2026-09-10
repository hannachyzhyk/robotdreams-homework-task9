# Частина 2. Додаткове завдання: тест стабільності датчика — 5 балів
# У файлі tests/functional/test_distance_stability.py реалізуйте тест test_distance_readings_are_stable.

import pytest

from helpers.distanceLogHelper import get_distance_logs, parse_distance_values, is_within_range

@pytest.mark.functional
def test_distance_readings_are_stable(logged_device):
    # Start distance logging, accumulate readings for a specified duration, and then stop the logging
    distance_logs = get_distance_logs(logged_device, log_duration=5)

    # Parse the distance values from the distance log lines
    distance_values, calibrated_distance_values = parse_distance_values(distance_logs)

    # Check if all distance values are within a specified relative tolerance of the target value
    assert is_within_range(distance_values, tolerance=0.05), \
        f"FAIL: Distance readings are not stable. Readings: {distance_values}"
    assert is_within_range(calibrated_distance_values, tolerance=0.05), \
        f"FAIL: Calibrated distance readings are not stable. Readings: {calibrated_distance_values}"
