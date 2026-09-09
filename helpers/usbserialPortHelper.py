def getUsbserialPort() -> str:
    """
    Повертає порт USB-Serial, до якого підключено пристрій.
    Використовує бібліотеку pyserial для пошуку доступних портів.
    """
    import serial.tools.list_ports
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if ('usbserial' in port.device) :
                return port.device
    raise Exception("USB-Serial device not found")