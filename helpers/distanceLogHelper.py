import time
import re
import math

def get_distance_logs(logged_device, log_duration=5) -> list[str]:
    """
    Helper function to start distance logging, accumulate readings for a specified duration,
    and then stop the logging. Returns the list of distance log readings.
    """
    # Start the distance log
    logged_device.send_command(f"distance log 500")
    assert logged_device.wait_for(f"Log started.", timeout=5), f"FAIL: Expected confirmation message for starting distance log"
    
    # Accumulate distance log readings for a specified duration 
    time.sleep(log_duration)  # Wait a moment for the log to start
    response = logged_device.read_lines(timeout=log_duration)
    responses = [l for l in response if f"DistLog" in l]
    
    # Stop the distance log
    logged_device.send_command(f"distance log stop")
    assert logged_device.wait_for(f"Log stopped.", timeout=5), f"FAIL: Expected confirmation message for stopping distance log"
    
    return responses

def parse_distance_values(distance_logs) -> tuple[list[float], list[float]]:
    """
    Helper function to parse distance values from the distance log lines.
    Returns a list of float values extracted from the logs.
    """
    distance_values = []
    calibrated_distance_values = []
    for l in distance_logs:
        # I (19731) DIST: [Distance] #1 2.8 cm (calibrated: 2.8 cm) -> [2.8, 2.8]
        match = re.findall(r"\b\d+\.\d+\b", l)
        if not match or len(match) < 2:
            raise ValueError(f"Unexpected log format: {l}")
        distance_values.append(float(match[0]))
        calibrated_distance_values.append(float(match[1]))
    return distance_values, calibrated_distance_values

def is_within_range(values, target=None, tolerance=0.05) -> bool:
    """
    Helper function to check if all values are within a specified relative tolerance of the target value.
    Returns True if all values are within range, otherwise False.
    """
    if target is None:
        target = values[0]
    return all(
        math.isclose(float(val), float(target), rel_tol=tolerance) for val in values
    )