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
        return "Atmel STK500"


    @staticmethod
    def get_aliases():
        return ["stk500"]


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
