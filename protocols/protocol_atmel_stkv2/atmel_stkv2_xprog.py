'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from core import *
from protocols import *
from protocols.protocol_atmel_stkv2.atmel_stkv2_base import *


class ProtocolAtmelSTKV2_XPROG(ProtocolAtmelSTKV2_Base):
    def _trancieve_xprog(self, packet_out):
        xprog_packet_out = [AtmelSTKV2Defs.commands["XPROG"]]
        xprog_packet_out.extend(packet_out)

        xprog_packet_in = self._trancieve(xprog_packet_out)

        if xprog_packet_in[1] != packet_out[0]:
            raise ProtocolError("Invalid XPROG response received from tool.")

        if packet_in[2] != AtmelSTKV2Defs.status_codes["CMD_OK"]:
            raise ProtocolError("Command %s failed with status %s." %
                                (AtmelSTKV2Defs.find(AtmelSTKV2Defs.commands, xprog_packet_out[1]),
                                 AtmelSTKV2Defs.find(AtmelSTKV2Defs.status_codes, xprog_packet_in[2])))

    def _set_interface_mode(self):
        interface_map = {
            "pdi"  : 0,
            "jtag" : 1,
            "tpi"  : 2
        }

        packet = [AtmelSTKV2Defs.commands["XPROG_SETMODE"]]
        packet.append(interface_map[self.interface])
        self._trancieve(packet)


    def set_interface_frequency(self, target_frequency):
        raise NotImplementedError()


    def enter_session(self):
        self._set_interface_mode()

        packet = [AtmelSTKV2Defs.commands["XPROG_ENTER_PROGMODE"]]
        self._xprog_trancieve(packet)


    def exit_session(self):
        raise NotImplementedError()


    def erase_memory(self, memory_space):
        raise NotImplementedError()


    def read_memory(self, memory_space, offset, length):
        raise NotImplementedError()


    def write_memory(self, memory_space, offset, data):
        raise NotImplementedError()
