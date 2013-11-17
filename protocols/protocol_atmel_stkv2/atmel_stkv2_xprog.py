'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from core import *
from protocols import *
from protocols.protocol_atmel_stkv2.atmel_stkv2_base import *


class ProtocolAtmelSTKV2_XPROG(ProtocolAtmelSTKV2_Base):
    MEMORY_MODE_FLAG_ERASE   = 0x01
    MEMORY_MODE_FLAG_PROGRAM = 0x02


    def set_interface_frequency(self, target_frequency):
        pass


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


    def _set_interface_mode_xprog(self):
        interface_map = {
            "pdi"  : 0,
            "jtag" : 1,
            "tpi"  : 2
        }

        packet = [AtmelSTKV2Defs.commands["XPROG_SETMODE"]]
        packet.append(interface_map[self.interface])
        self._trancieve(packet)


    def _set_param_xprog(self, param, value, length):
        packet = [AtmelSTKV2Defs.xprog_commands["SET_PARAMETER"]]
        packet.append(param)
        packet.extend(Util.array_encode(value, length, "big"))
        self._trancieve_xprog(packet)


    def _get_memory_base_offset(self, memory_space):
        pdi_memory_baseaddr_map = {
            "application"         : 0x00800000,
            "eeprom"              : 0x008C0000,
            "fuses"               : 0x008F0020,
            "user_signature"      : 0x008E0400,
            "user_signature"      : 0x008E0400,

            "flash"               : 0x00800000,
            "signature"           : 0x01000090
        }

        if not memory_space in pdi_memory_baseaddr_map:
            raise NotImplementedError()

        return pdi_memory_baseaddr_map[memory_space]


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
            raise ProtocolMemoryActionError("erasing", memory_space)

        packet = [AtmelSTKV2Defs.xprog_commands["ERASE"]]
        packet.append(erase_type)
        packet.extend(Util.array_encode(offset, 4, "big"))
        self._trancieve_xprog(packet)


    def read_memory(self, memory_space, offset, length):
        mem_contents = []

        offset += self._get_memory_base_offset(memory_space)

        if memory_space == "flash":
            memory_space = "application"
        elif memory_space == "signature":
            memory_space = "factory_calibration"

        try:
            memory_type = AtmelSTKV2Defs.xprog_memory_types[memory_space.upper()]
        except KeyError:
            raise ProtocolMemoryActionError("reading", memory_space)

        for (address, chunklen) in Util.chunk_address(length, min(length, 256), offset):
            packet = [AtmelSTKV2Defs.xprog_commands["READ_MEMORY"]]
            packet.append(memory_type)
            packet.extend(Util.array_encode(address, 4, "big"))
            packet.extend(Util.array_encode(chunklen, 2, "big"))
            resp = self._trancieve_xprog(packet)

            mem_contents.extend(resp[2 : ])

        return mem_contents[0 : length]


    def write_memory(self, memory_space, offset, data):
        offset += self._get_memory_base_offset(memory_space)

        if memory_space == "flash":
            memory_space = "application"

        try:
            memory_type = AtmelSTKV2Defs.xprog_memory_types[memory_space.upper()]
        except KeyError:
            raise ProtocolMemoryActionError("writing", memory_space)

        start_address = offset
        end_address   = start_address + len(data)

        for (address, chunk) in Util.chunk_data(data, 256, offset):
            memory_mode = 0

            if address == start_address:
                memory_mode |= ProtocolAtmelSTKV2_XPROG.MEMORY_MODE_FLAG_ERASE

            if address == end_address - len(chunk):
                memory_mode |= ProtocolAtmelSTKV2_XPROG.MEMORY_MODE_FLAG_PROGRAM

            packet = [AtmelSTKV2Defs.xprog_commands["WRITE_MEMORY"]]
            packet.append(memory_type)
            packet.append(memory_mode)
            packet.extend(Util.array_encode(address, 4, "big"))
            packet.extend(Util.array_encode(len(chunk), 2, "big"))
            packet.extend(chunk)
            self._trancieve_xprog(packet)
