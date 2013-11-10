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

        return xprog_packet_in[1 : ]


    def _set_param_xprog(self, param, value, length):
        packet = [AtmelSTKV2Defs.xprog_commands["SET_PARAMETER"]]
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
        self._set_interface_mode_xprog()

        packet = [AtmelSTKV2Defs.xprog_commands["ENTER_PROGMODE"]]
        self._trancieve_xprog(packet)

        if self.interface == "tpi":
            nvmcmd      = 0x33
            nvmcsr      = 0x32
            self._set_param_xprog(AtmelSTKV2Defs.xprog_params["NVMCMD_REG"], nvmcmd, 1)
            self._set_param_xprog(AtmelSTKV2Defs.xprog_params["NVMCSR_REG"], nvmcsr, 1)
        else:
            nvmbase     = 0x010001C0
            eeppagesize = 32
            self._set_param_xprog(AtmelSTKV2Defs.xprog_params["NVMBASE"], nvmbase, 4)
            self._set_param_xprog(AtmelSTKV2Defs.xprog_params["EEPPAGESIZE"], eeppagesize, 2)


    def exit_session(self):
        packet = [AtmelSTKV2Defs.xprog_commands["LEAVE_PROGMODE"]]
        self._trancieve_xprog(packet)


    def erase_memory(self, memory_space, offset):
        if memory_space is None:
            memory_space = "chip"

        try:
            erase_type = AtmelSTKV2Defs.xprog_erase_types[memory_space.upper()]
        except KeyError:
            raise NotImplementedError()

        packet = [AtmelSTKV2Defs.xprog_commands["ERASE"]]
        packet.append(erase_type)
        packet.append((offset >> 24) & 0xFF)
        packet.append((offset >> 16) & 0xFF)
        packet.append((offset >> 8) & 0xFF)
        packet.append(offset & 0xFF)
        self._trancieve_xprog(packet)


    def read_memory(self, memory_space, offset, length):
        mem_contents = []

        if memory_space == "signature":
            memory_space = "factory_calibration"
            offset += 0x01000090

        try:
            memory_type = AtmelSTKV2Defs.xprog_memory_types[memory_space.upper()]
        except KeyError:
            raise NotImplementedError()

        for (address, chunklen) in Util.chunk_address(length, min(length, 256), offset):
            packet = [AtmelSTKV2Defs.xprog_commands["READ_MEMORY"]]
            packet.append(memory_type)
            packet.append((address >> 24) & 0xFF)
            packet.append((address >> 16) & 0xFF)
            packet.append((address >> 8) & 0xFF)
            packet.append(address & 0xFF)
            packet.append((chunklen >> 8) & 0xFF)
            packet.append(chunklen & 0xFF)
            resp = self._trancieve_xprog(packet)

            mem_contents.extend(resp[2 : ])

        return mem_contents[0 : length]


    def write_memory(self, memory_space, offset, data):
        try:
            memory_type = AtmelSTKV2Defs.xprog_memory_types[memory_space.upper()]
        except KeyError:
            raise NotImplementedError()

        return NotImplementedError()
