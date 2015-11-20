'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)

   Release under a MIT license; see LICENSE.txt for details.
'''

from tools import *
from transports import *
from protocols import *


class ToolAtmelAVR109(Tool):
    def __init__(self, device, serial, baud, port, interface):
        if baud is None:
            baud = 9600

        if port is None:
           raise ToolSupportError("tool", "port", port)
        else:
            self.transport = TransportSerial(port=port, baud=baud)

        if not interface in self.get_supported_interfaces():
            raise ToolSupportError("tool", "interface", interface,
                                   self.get_supported_interfaces())
        else:
            self.interface = interface

        self.protocol = ProtocolAtmelAVR109(self, device, interface)


    @staticmethod
    def find_connected():
        return []


    @staticmethod
    def get_name():
        return "Atmel AVR109 Bootloader"


    @staticmethod
    def get_aliases():
        return ["avr109"]


    @staticmethod
    def get_supported_interfaces():
        return ["avr109"]


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
