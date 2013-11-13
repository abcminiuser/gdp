'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

import sys
try:
    import usb.core
    import usb.util
except ImportError:
    print("The PyUSB 1.x library is not installed.")
    sys.exit(1)

from transports import *


class TransportJungoUSB(Transport):
    def __init__(self, vid=0x03eb, pid=None, read_ep=2, write_ep=2):
        self.dev_handle = None
        self.vid = vid
        self.pid = pid
        self.read_ep = read_ep
        self.write_ep = write_ep


    @staticmethod
    def find_connected(vid=0x03eb, pid=None):
        found_devices = usb.core.find(idVendor=vid, idProduct=pid, find_all=True)
        for device in found_devices:
            yield usb.util.get_string(device, 256, device.iSerialNumber)


    def open(self):
        if self.vid is None or self.pid is None:
            raise TransportMissingParamError("VID or PID")

        if self.read_ep is None or self.write_ep is None:
            raise TransportMissingParamError("read/write endpoint")

        self.dev_handle = usb.core.find(idVendor=self.vid, idProduct=self.pid)
        if self.dev_handle is None:
            raise TransportError("Specified tool was not found on the USB bus.")

        self.dev_handle.set_configuration()


    def close(self):
        pass


    def read(self):
        data = []

        while len(data) % 64 == 0:
            data.extend(self.dev_handle.read(usb.util.ENDPOINT_IN | self.read_ep, 64, 0, 1000))

        return data


    def write(self, data):
        self.dev_handle.write(usb.util.ENDPOINT_OUT | self.write_ep, data, 0, 1000)
