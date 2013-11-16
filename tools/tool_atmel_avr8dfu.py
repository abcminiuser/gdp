'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from tools import *
from transports import *
from protocols import *


class ToolAtmelAVR8DFU(Tool):
    device_to_pid = {
        "at90usb1287" : 0x2FFB,
        "at90usb647"  : 0x2FF9,
        "at90usb1286" : 0x2FFB,
        "at90usb646"  : 0x2FF9,
        "atmega32u4"  : 0x2FF4,
        "atmega16u4"  : 0x2FF3,
        "atmega32u2"  : 0x2FF0,
        "atmega16u2"  : 0x2FEF,
        "at90usb162"  : 0x2FFA,
        "atmega8u2"   : 0x2FEE,
        "at90usb82"   : 0x2FF7,
    }


    def __init__(self, device, serial=None, port=None, interface="dfu"):
        try:
            pid = ToolAtmelAVR8DFU.device_to_pid[device.get_name().lower()]
        except KeyError:
            raise ToolSupportError("tool", "device", device.get_name().lower(),
                                   ToolAtmelAVR8DFU.device_to_pid.iterkeys())

        if port is None:
            self.transport = TransportDFUUSB(vid=0x03EB, pid=pid, serial=serial)
        else:
            raise ToolSupportError("tool", "port", port)

        if not interface in self.get_supported_interfaces():
            raise ToolSupportError("tool", "interface", interface,
                                   self.get_supported_interfaces())
        else:
            self.interface = interface

        self.protocol = ProtocolAtmelDFUV1(self, device, interface)
        self.sequence = 0x00


    @staticmethod
    def find_connected():
        for pid in ToolAtmelAVR8DFU.device_to_pid.itervalues():
            found_serials = TransportDFUUSB.find_connected(vid=0x03EB, pid=pid)

            for serial in found_serials:
                yield serial


    @staticmethod
    def get_name():
        return "Atmel DFU Bootloader (AVR8)"


    @staticmethod
    def get_aliases():
        return ["dfu8avr8"]


    @staticmethod
    def get_supported_interfaces():
        return ["dfu"]


    def get_protocol(self):
        return self.protocol


    def open(self):
        self.transport.open()
        self.protocol.open()


    def close(self):
        self.protocol.close()
        self.transport.close()


    def read(self, read_type, length):
        return self.transport.read(read_type, length)


    def write(self, write_type, data):
        self.transport.write(write_type, data)
