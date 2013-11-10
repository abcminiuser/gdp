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

        self.tool.write(xprog_packet_out)
        xprog_packet_in = self.tool.read()

        if xprog_packet_in[1] != xprog_packet_out[1]:
            raise ProtocolError("Invalid XPROG response received from tool.")

        if xprog_packet_in[2] != AtmelSTKV2Defs.xprog_status_codes["OK"]:
            raise ProtocolError("XPROG Command %s failed with status %s." %
                                (AtmelSTKV2Defs.find(AtmelSTKV2Defs.xprog_commands, xprog_packet_out[1]),
                                 AtmelSTKV2Defs.find(AtmelSTKV2Defs.xprog_status_codes, xprog_packet_in[2])))


    def _set_param_xprog(self, param, value, length):
        packet = [AtmelSTKV2Defs.xprog_commands["SET_PARAM"]]
        packet.append(param)
        for x in range(length):
            packet.append((value >> (8 * (length - x - 1))) & 0xFF)
        self._trancieve_xprog(packet)


    def _set_interface_mode_xprog(self):
        interface_map = {
            "pdi"  : 0,
            "jtag" : 1,
            "tpi"  : 2
        }

        packet = [AtmelSTKV2Defs.commands["XPROG_SETMODE"]]
        packet.append(interface_map[self.interface])
        self._trancieve(packet)


    def set_interface_frequency(self, target_frequency):
        pass


    def enter_session(self):
        nvmbase     = 0x000001C0
        eeppagesize = 32
        nvmcmd      = 0x33
        nvmcsr      = 0x32

        self._set_interface_mode_xprog()
        self._set_param_xprog(AtmelSTKV2Defs.xprog_params["NVMBASE"], nvmbase, 4)
        self._set_param_xprog(AtmelSTKV2Defs.xprog_params["EEPPAGESIZE"], eeppagesize, 2)
        self._set_param_xprog(AtmelSTKV2Defs.xprog_params["NVMCMD_REG"], nvmcmd, 1)
        self._set_param_xprog(AtmelSTKV2Defs.xprog_params["NVMCSR_REG"], nvmcsr, 1)
        self._set_param_xprog(AtmelSTKV2Defs.xprog_params["UNKNOWN_1"], 0, 2)

        packet = [AtmelSTKV2Defs.xprog_commands["ENTER_PROGMODE"]]
        self._xprog_trancieve(packet)


    def exit_session(self):
        packet = [AtmelSTKV2Defs.xprog_commands["LEAVE_PROGMODE"]]
        self._xprog_trancieve(packet)


    def erase_memory(self, memory_space):
        raise NotImplementedError()


    def read_memory(self, memory_space, offset, length):
        raise NotImplementedError()


    def write_memory(self, memory_space, offset, data):
        raise NotImplementedError()
