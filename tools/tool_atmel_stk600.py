'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from tools import *
from transports import *
from protocols import *


class ToolAtmelSTK600(Tool):
    def __init__(self, device, port=None, interface="isp"):
        if port is None:
            self.transport = TransportJungoUSB(vid=0x03EB, pid=0x2106, read_ep=2, write_ep=2)
        else:
            raise ToolError("Unsupported port \"%s\" for the specified tool." % port)

        if not interface in device.get_supported_interfaces():
            raise ToolError("Unsupported interface \"%s\" for the specified device." % interface)
        elif not interface in self.get_supported_interfaces():
            raise ToolError("Unsupported interface \"%s\" for the specified tool." % interface)
        else:
            self.interface = interface

        self.protocol = ProtocolAtmelSTKV2(self, device, interface)


    @staticmethod
    def get_name():
        return "Atmel STK600"


    @staticmethod
    def get_supported_interfaces():
        return ["isp", "pdi", "tpi", "hvpp", "hvsp", "jtag"]


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
