'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)

   Release under a MIT license; see LICENSE.txt for details.
'''

from tools import *
from transports import *
from protocols import *

from tools.tool_atmel_jtagicemkii import ToolAtmelJTAGICEMKII


class ToolAtmelDragon(ToolAtmelJTAGICEMKII):
    def __init__(self, device, serial, baud, port, interface):
        if port is None:
            self.transport = TransportJungoUSB(vid=0x03EB, pid=0x2107, serial=serial)
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

        self.protocol = ProtocolAtmelJTAGV2(self, device, interface)
        self.sequence = 0x0000


    @staticmethod
    def find_connected():
        return TransportJungoUSB.find_connected(vid=0x03EB, pid=0x2107)


    @staticmethod
    def get_name():
        return "Atmel AVR Dragon"


    @staticmethod
    def get_aliases():
        return ["dragon", "avrdragon"]


    @staticmethod
    def get_supported_interfaces():
        return ["jtag", "isp", "pdi", "debugwire", "hvpp", "hvsp"]


    def get_protocol(self):
        return self.protocol


    def open(self):
        super(ToolAtmelDragon, self).open()


    def close(self):
        super(ToolAtmelDragon, self).close()


    def read(self):
        return super(ToolAtmelDragon, self).read()


    def write(self, data):
        super(ToolAtmelDragon, self).write(data)
