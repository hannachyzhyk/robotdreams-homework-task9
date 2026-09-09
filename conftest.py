import pytest
from drivers.device_driver import DeviceDriver
from helpers.usbserialPortHelper import getUsbserialPort

@pytest.fixture(scope="session")
def device():
    device = DeviceDriver(port=getUsbserialPort())
    device.open()

    yield device

    device.close()
    
@pytest.fixture(scope="function")
def rebooted_device(device):
    device.reboot()
    return device
    
@pytest.fixture(scope="function")
def registered_device(rebooted_device):
    rebooted_device.register("user", "correctpass")
    return rebooted_device
    
@pytest.fixture(scope="function")
def logged_device(registered_device):
    registered_device.login("user", "correctpass")
    return registered_device
