'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from tools import *
from transports import *
from protocols import *

from tools.tool_atmel_stk500 import ToolAtmelSTK500


class ToolAtmelAVRISP(ToolAtmelSTK500):
    def __init__(self, device, serial, baud, port, interface):
        if baud is None:
            baud = 115200

        if port is None:
           raise ToolSupportError("tool", "port", port)
        else:
            self.transport = TransportSerial(port=port, baud=baud)

        if not interface in device.get_supported_interfaces():
            raise ToolSupportError("device", "interface", interface,
                                   device.get_supported_interfaces())
        elif not interface in self.get_supported_interfaces():
            raise ToolSupportError("tool", "interface", interface,
                                   self.get_supported_interfaces())
        else:
            self.interface = interface

        self.protocol = ProtocolAtmelSTKV2(self, device, interface)
        self.sequence = 0x00


    @staticmethod
    def find_connected():
        return []


    @staticmethod
    def get_name():
        return "Atmel AVRISP"


    @staticmethod
    def get_aliases():
        return ["avrisp"]


    @staticmethod
    def get_supported_interfaces():
        return ["isp"]


    def get_protocol(self):
        return self.protocol
