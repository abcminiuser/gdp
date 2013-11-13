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


class TransportDFUUSB(Transport):
    DFU_REQUEST_DNLOAD = 1
    DFU_REQUEST_UPLOAD = 2


    def __init__(self, vid=0x03eb, pid=None, serial=None):
        self.dev_handle = None
        self.vid        = vid
        self.pid        = pid
        self.serial     = serial

        self.sequence   = 0


    @staticmethod
    def _get_device_serial(device):
        return "%s:%s" % (device.bus, device.address)


    @staticmethod
    def _get_connected_devices(vid, pid):
        handles = usb.core.find(idVendor=vid, idProduct=pid, find_all=True)
        serials = [TransportDFUUSB._get_device_serial(d) for d in handles]
        return dict(zip(handles, serials))


    def _find_device(self):
        found_devices = TransportDFUUSB._get_connected_devices(vid=self.vid,
                                                               pid=self.pid)

        if self.serial is None:
            if len(found_devices) > 1:
                raise TransportMultipleMatchError(found_devices.itervalues())
            else:
                return found_devices.iterkeys()[0]

        for device, serial in found_devices.iteritems():
            if self.serial in serial:
                return device

        return None


    @staticmethod
    def find_connected(vid=0x03eb, pid=None):
        found_devices = TransportDFUUSB._get_connected_devices(vid=vid,
                                                               pid=pid)
        return found_devices.itervalues()


    def open(self):
        if self.vid is None or self.pid is None:
            raise TransportMissingParamError("VID or PID")

        self.dev_handle = self._find_device()
        if self.dev_handle is None:
            raise TransportError("Specified tool was not found on the USB bus.")

        self.dev_handle.set_configuration()


    def close(self):
        pass


    def read(self, request, length):
        bmRequestType = usb.util.build_request_type(
                        usb.util.CTRL_IN,
                        usb.util.CTRL_TYPE_CLASS,
                        usb.util.CTRL_RECIPIENT_INTERFACE
                    )

        if request == TransportDFUUSB.DFU_REQUEST_UPLOAD:
            value = self.sequence
            self.sequence += 1
        else:
            value = 0

        return self.dev_handle.ctrl_transfer(bmRequestType=bmRequestType,
                                             bRequest=request,
                                             wValue=value,
                                             wIndex=0,
                                             data_or_wLength=length,
                                             timeout=5000)


    def write(self, request, data):
        bmRequestType = usb.util.build_request_type(
                        usb.util.CTRL_OUT,
                        usb.util.CTRL_TYPE_CLASS,
                        usb.util.CTRL_RECIPIENT_INTERFACE
                    )

        if request == TransportDFUUSB.DFU_REQUEST_DNLOAD:
            value = self.sequence
            self.sequence += 1
        else:
            value = 0

        self.dev_handle.ctrl_transfer(bmRequestType=bmRequestType,
                                      bRequest=request,
                                      wValue=value,
                                      wIndex=0,
                                      data_or_wLength=data,
                                      timeout=5000)
