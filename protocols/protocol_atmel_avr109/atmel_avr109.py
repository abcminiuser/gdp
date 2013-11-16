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


    def _send_command(self, packet, returns_data):
        self.tool.write(packet)
        resp = self.tool.read()

        if returns_data is True:
            return resp

        if resp[0] != AtmelAVR109Defs.RESP_TERMINATOR_CHAR:
            raise ProtocolError("Invalid %s response from device." %
                                AtmelAVR109Defs.find(AtmelAVR109Defs.commands,
                                                     packet[0]))


    def _set_address(self, address):
        packet = [AtmelAVR109Defs.commands["SET_ADDRESS"]]
        packet.extend(Util.array_encode(address, 2, "big"))
        self._send_command(packet, returns_data=False)


    def _mem_read_block(self, memory_space, offset, length):
        mem_contents = []

        for (address, chunklen) in Util.chunk_address(length, self.block_length, offset):
            packet = [AtmelAVR109Defs.commands["READ_BLOCK"]]
            packet.extend(Util.array_encode(self.block_length, 2, "big"))
            packet.append(ord('F') if memory_space == "flash" else ord('E'))

            resp = self._send_command(packet, returns_data=True)
            mem_contents.extend(resp)

        return mem_contents


    def _mem_read(self, memory_space, offset, length):
        mem_contents = []

        read_length  = 2 if memory_space is "flash" else 1
        read_command = "READ_FLASH_WORD" if memory_space is "flash" else "READ_EEPROM_BYTE"

        for (address, chunklen) in Util.chunk_address(length, read_length, offset):
            if self.auto_address_increment == False:
                self._set_address(address)

            packet = [AtmelAVR109Defs.commands[read_command]]
            resp = self._send_command(packet, returns_data=True)
            mem_contents.extend(resp)

        return mem_contents


    def _mem_write_block(self, memory_space, offset, data):
        for (address, chunk) in Util.chunk_data(data, self.block_length, offset):
            packet = [AtmelAVR109Defs.commands["WRITE_BLOCK"]]
            packet.extend(Util.array_encode(self.block_length, 2, "big"))
            packet.append(ord('F') if memory_space == "flash" else ord('E'))
            packet.extend(chunk)

            self._send_command(packet, returns_data=False)


    def _mem_write(self, memory_space, offset, data):
        raise NotImplementedError()


    def get_vtarget(self):
        return None


    def set_interface_frequency(self, target_frequency):
        pass


    def enter_session(self):
        packet = [AtmelAVR109Defs.commands["ENTER_PROG_MODE"]]
        self._send_command(packet, returns_data=False)

        packet = [AtmelAVR109Defs.commands["ADDRESS_AUTO_INCREMENT"]]
        resp = self._send_command(packet, returns_data=True)
        self.auto_address_increment = resp[0] == ord('Y')

        packet = [AtmelAVR109Defs.commands["CHECK_BLOCK_SUPPORT"]]
        resp = self._send_command(packet, returns_data=True)
        self.block_support = resp[0] == ord('Y')

        if self.block_support is True:
            self.block_length = Util.array_decode(resp[1 : 3], "big")


    def exit_session(self):
        pass


    def erase_memory(self, memory_space, offset):
        if memory_space is None:
            packet = [AtmelAVR109Defs.commands["CHIP_ERASE"]]
            self._send_command(packet, returns_data=False)
        else:
            raise ProtocolError("The specified tool cannot erase the requested memory space.")


    def read_memory(self, memory_space, offset, length):
        mem_contents = []

        if memory_space == "signature":
            packet = [AtmelAVR109Defs.commands["READ_SIGNATURE"]]
            resp = self._send_command(packet, returns_data=True)
            mem_contents.extend(resp[offset : offset + length : -1])
        elif memory_space in ["flash", "eeprom"]:
            self._set_address(offset)

            if self.block_support == True:
                mem_contents.extend(self._mem_read_block(memory_space, offset, length))
            else:
                mem_contents.extend(self._mem_read(memory_space, offset, length))
        else:
            raise NotImplementedError()

        return mem_contents


    def write_memory(self, memory_space, offset, data):
        if memory_space in ["flash", "eeprom"]:
            self._set_address(offset)

            if self.block_support == True:
                self._mem_write_block(memory_space, offset, data)
            else:
                self._mem_write(memory_space, offset, data)
        else:
            raise NotImplementedError()


    def open(self):
        packet = [AtmelAVR109Defs.commands["SET_LED"]]
        packet.append(1)
        self._send_command(packet, returns_data=False)


    def close(self):
        packet = [AtmelAVR109Defs.commands["CLEAR_LED"]]
        packet.append(1)
        self._send_command(packet, returns_data=False)
