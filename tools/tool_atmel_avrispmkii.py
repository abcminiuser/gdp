'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from tools import *
from transports import *
from protocols import *


class ToolAtmelAVRISPMKII(Tool):
    def __init__(self, device, serial=None, port=None, interface="isp"):
        if port is None:
            self.transport = TransportJungoUSB(vid=0x03EB, pid=0x2104, serial=serial)
        else:
            raise ToolSupportError("tool", "port", port)

        if not interface in device.get_supported_interfaces():
            raise ToolSupportError("device", "interface", interface,
                                   device.get_supported_interfaces())
        elif not interface in self.get_supported_interfaces():
            raise ToolSupportError("tool", "interface", interface,
                                   self.get_supported_interfaces())
        else:
            self.interface = interface

        self.protocol = ProtocolAtmelSTKV2(self, device, interface)


    @staticmethod
    def find_connected():
        return TransportJungoUSB.find_connected(vid=0x03EB, pid=0x2104)


    @staticmethod
    def get_name():
        return "Atmel AVRISP-MKII"


    @staticmethod
    def get_supported_interfaces():
        return ["isp", "pdi", "tpi"]


    def get_protocol(self):
        return self.protocol


    def open(self):
        self.transport.open()
        self.protocol.open()


    def close(self):
        self.protocol.close()
        self.transport.close()


    def read(self):
        return self.transport.read()


    def write(self, data):
        self.transport.write(data)
