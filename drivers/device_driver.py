import serial

import time
import re

class DeviceDriver:
    def __init__(self, port, timeout=2):
        self.port = port
        self.timeout = timeout
        self.ser = None

    def open(self):
        self.ser = serial.Serial(self.port, baudrate=115200, bytesize=8,
                                 parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                                 timeout=self.timeout)
        time.sleep(3)  # Wait for the serial port to initialize
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()

    def close(self):
        if self.ser:
            self.ser.close()
            self.ser = None

    def send_command(self, command):
        if not self.ser:
            raise Exception("Serial connection is not open.")
        self.ser.write((command + '\r\n').encode())

    def read_lines(self, timeout):
        if not self.ser:
            raise Exception("Serial connection is not open.")
        old_timeout = self.ser.timeout
        deadline = time.monotonic() + timeout
        lines = []
        try:
            while True:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    break
                self.ser.timeout = remaining
                line = self.ser.readline().decode("utf-8", errors="replace").strip()
                if not line:
                    break
                # Remove ANSI escape codes
                line = re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', line)
                lines.append(line)
        finally:
            self.ser.timeout = old_timeout
        print("Debug lines:", lines)
        return lines

    def wait_for(self, pattern, timeout):
        start_time = time.time()
        while time.time() - start_time < timeout:
            lines = self.read_lines(timeout - (time.time() - start_time))
            for line in lines:
                if pattern in line:
                    return True
        return False

    def reboot(self) -> bool:
        self.send_command("reboot")
        print("Waiting for device to reboot...")
        return self.wait_for("Device ready.", 10)

    def register(self, login, password) -> bool:
        self.send_command(f"register {login} {password}")
        print("Waiting for profile creation...")
        return self.wait_for("Profile Created", 5)

    def login(self, login, password) -> bool:
        self.send_command(f"login {login} {password}")
        print("Waiting for login...")
        return self.wait_for("Session Started", 5)