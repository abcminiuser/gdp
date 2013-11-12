'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from core import *
from tools import *
from transports import *
from protocols import *


class ToolAtmelSTK500(Tool):
    STK500_PACKET_START = 0x1B
    STK500_PACKET_TOKEN = 0x0E


    @staticmethod
    def _calc_checksum(data):
        checksum = 0x00

        for byte in data:
            checksum ^= byte

        return checksum


    def __init__(self, device, port=None, interface="isp"):
        if port is None:
            raise ToolError("Unsupported port for the specified tool.")
        else:
            self.transport = TransportSerial(port=port, baud=115200)

        if not interface in device.get_supported_interfaces():
            raise ToolError("Unsupported interface \"%s\" for the specified device." % interface)
        elif not interface in self.get_supported_interfaces():
            raise ToolError("Unsupported interface \"%s\" for the specified tool." % interface)
        else:
            self.interface = interface

        self.protocol = ProtocolAtmelSTKV2(self, device, interface)
        self.sequence = 0x00


    @staticmethod
    def get_name():
        return "Atmel STK500"


    @staticmethod
    def get_supported_interfaces():
        return ["isp", "pdi", "tpi", "hvpp", "hvsp"]


    def get_protocol(self):
        return self.protocol


    def open(self):
        self.transport.open()
        self.protocol.open()


    def close(self):
        self.protocol.close()
        self.transport.close()


    def read(self):
        packet = self.transport.read()

        if len(packet) < 6:
            return None

        if packet[0] != ToolAtmelSTK500.STK500_PACKET_START:
            return None

        rec_sequence = packet[1]
        if rec_sequence != self.sequence:
            self.sequence = rec_sequence
            return None

        if packet[4] != ToolAtmelSTK500.STK500_PACKET_TOKEN:
            return None

        checksum = packet[-1]
        checksum_expected = self._calc_checksum(packet[0 : -1])
        if (checksum != checksum_expected):
            return None

        return packet[5 : -1]


    def write(self, data):
        self.sequence += 1

        packet = []
        packet.append(ToolAtmelSTK500.STK500_PACKET_START)
        packet.append(self.sequence)
        packet.extend(Util.array_encode(len(data), 2, "big"))
        packet.append(ToolAtmelSTK500.STK500_PACKET_TOKEN)
        packet.extend(data)
        packet.append(self._calc_checksum(packet))

        self.transport.write(packet)
