'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from core.util import *
from protocols import *
from protocols.protocol_atmel_avr109.atmel_avr109_defs import *


class ProtocolAtmelAVR109(Protocol):
    def __init__(self, tool, device, interface):
        self.tool      = tool
        self.device    = device
        self.interface = interface


    def _transcieve(self, packet, has_terminator):
        self.tool.write(packet)
        resp = self.tool.read()

        if has_terminator is True:
            if resp[-1] != AtmelAVR109Defs.RESP_TERMINATOR_CHAR:
                raise ProtocolError("Invalid %s response from device." %
                                    AtmelAVR109Defs.find(AtmelAVR109Defs.commands,
                                                         packet[0]))
            return resp[0 : -1]

        return resp


    def _set_address(self, address):
        packet = [AtmelAVR109Defs.commands["SET_ADDRESS"]]
        packet.extend(Util.array_encode(address, 2, "big"))
        self._transcieve(packet, has_terminator=True)


    def get_vtarget(self):
        return None


    def set_interface_frequency(self, target_frequency):
        pass


    def enter_session(self):
        packet = [AtmelAVR109Defs.commands["ENTER_PROG_MODE"]]
        self._transcieve(packet, has_terminator=True)

        packet = [AtmelAVR109Defs.commands["ADDRESS_AUTO_INCREMENT"]]
        resp = self._transcieve(packet, has_terminator=False)
        self.auto_address_increment = resp[0] == ord('Y')

        packet = [AtmelAVR109Defs.commands["CHECK_BLOCK_SUPPORT"]]
        resp = self._transcieve(packet, has_terminator=False)
        self.block_support = resp[0] == ord('Y')

        if self.block_support is True:
            self.block_length = Util.array_decode(resp[1 : 3], "big")


    def exit_session(self):
        packet = [AtmelAVR109Defs.commands["LEAVE_PROG_MODE"]]
        self._transcieve(packet, has_terminator=True)


    def erase_memory(self, memory_space, offset):
        if memory_space is None:
            packet = [AtmelAVR109Defs.commands["CHIP_ERASE"]]
            self._transcieve(packet, has_terminator=True)
        else:
            raise ProtocolMemoryActionError("erasing", memory_space)


    def read_memory(self, memory_space, offset, length):
        mem_contents = []

        if memory_space == "signature":
            packet = [AtmelAVR109Defs.commands["READ_SIGNATURE"]]
            resp = self._transcieve(packet, has_terminator=False)
            mem_contents.extend(resp[offset : offset + length : -1])
        elif memory_space == "fuses":
            raise NotImplementedError()
        elif memory_space == "lockbits":
            raise NotImplementedError()
        elif memory_space in ["flash", "eeprom"]:
            if self.block_support is True:
                read_len = self.block_length
            else:
                read_len = 2 if memory_space == "flash" else 1

            for (address, chunklen) in Util.chunk_address(length, read_len, offset):
                if self.auto_address_increment is False or address == offset:
                    if memory_space == "flash":
                        self._set_address(address >> 1)
                    else:
                        self._set_address(address)

                if self.block_support is True:
                    packet = [AtmelAVR109Defs.commands["READ_BLOCK"]]
                    packet.extend(Util.array_encode(chunklen, 2, "big"))
                    packet.append(ord('F') if memory_space == "flash" else ord('E'))
                else:
                    if memory_space == "flash":
                        packet = [AtmelAVR109Defs.commands["READ_FLASH_WORD"]]
                    else:
                        packet = [AtmelAVR109Defs.commands["READ_EEPROM_BYTE"]]

                resp = self._transcieve(packet, has_terminator=False)
                mem_contents.extend(resp)
        else:
            raise ProtocolMemoryActionError("reading", memory_space)

        return mem_contents


    def write_memory(self, memory_space, offset, data):
        if memory_space == "fuses":
            raise NotImplementedError()
        elif memory_space == "lockbits":
            raise NotImplementedError()
        elif memory_space in ["flash", "eeprom"]:
            if self.block_support is True:
                write_len = self.block_length
            else:
                write_len = 1

            for (address, chunk) in Util.chunk_data(data, write_len, offset):
                if self.auto_address_increment is False or address == offset:
                    if memory_space == "flash":
                        self._set_address(address >> 1)
                    else:
                        self._set_address(address)

                if self.block_support is True:
                    packet = [AtmelAVR109Defs.commands["WRITE_BLOCK"]]
                    packet.extend(Util.array_encode(len(chunk), 2, "big"))
                    packet.append(ord('F') if memory_space == "flash" else ord('E'))
                else:
                    if memory_space == "flash":
                        packet = [AtmelAVR109Defs.commands["WRITE_FLASH_WORD_HIGH"
                                                           if address & 1 else
                                                           "WRITE_FLASH_WORD_LOW"]]
                    else:
                        packet = [AtmelAVR109Defs.commands["WRITE_EEPROM_BYTE"]]

                packet.extend(chunk)
                self._transcieve(packet, has_terminator=True)


            if memory_space == "flash" and self.block_support is False:
                packet = [AtmelAVR109Defs.commands["PAGE_WRITE"]]
                self._transcieve(packet, has_terminator=True)
        else:
            raise ProtocolMemoryActionError("writing", memory_space)


    def open(self):
        try:
            packet = [AtmelAVR109Defs.commands["SET_LED"]]
            packet.append(1)
            self._transcieve(packet, has_terminator=True)
        finally:
            pass


    def close(self):
        try:
            packet = [AtmelAVR109Defs.commands["CLEAR_LED"]]
            packet.append(1)
            self._transcieve(packet, has_terminator=True)
        finally:
            pass
