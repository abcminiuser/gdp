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
    def __init__(self, vid=0x03eb, pid=None, serial=None, read_ep=2, write_ep=2):
        self.dev_handle = None
        self.vid        = vid
        self.pid        = pid
        self.read_ep    = usb.util.ENDPOINT_IN | read_ep
        self.write_ep   = usb.util.ENDPOINT_OUT | write_ep
        self.serial     = serial


    @staticmethod
    def _get_device_serial(device):
        return usb.util.get_string(device, 256, device.iSerialNumber)


    @staticmethod
    def _get_connected_devices(vid, pid):
        handles = usb.core.find(idVendor=vid, idProduct=pid, find_all=True)
        serials = [TransportJungoUSB._get_device_serial(d) for d in handles]
        return dict(zip(handles, serials))


    def _find_device(self):
        found_devices = TransportJungoUSB._get_connected_devices(vid=self.vid,
                                                                 pid=self.pid)

        if self.serial is None:
            if len(found_devices) > 1:
                raise TransportMultipleMatchError(found_devices.itervalues())
            elif len(found_devices) != 0:
                return found_devices.keys()[0]
            else:
                return None

        for device, serial in found_devices.iteritems():
            if self.serial in serial:
                return device

        return None


    @staticmethod
    def find_connected(vid=0x03eb, pid=None):
        found_devices = TransportJungoUSB._get_connected_devices(vid=vid,
                                                                 pid=pid)
        return found_devices.itervalues()


    def open(self):
        if self.vid is None or self.pid is None:
            raise TransportMissingParamError("VID or PID")

        if self.read_ep is None or self.write_ep is None:
            raise TransportMissingParamError("read/write endpoint")

        self.dev_handle = self._find_device()
        if self.dev_handle is None:
            raise TransportError("Specified tool was not found on the USB bus.")

        self.dev_handle.set_configuration()


    def close(self):
        pass


    def read(self):
        data = []

        while len(data) % 64 == 0:
            chunk = self.dev_handle.read(self.read_ep, 64, 0, 1000)
            data.extend(chunk)

        return data


    def write(self, data):
        self.dev_handle.write(self.write_ep, data, 0, 1000)
