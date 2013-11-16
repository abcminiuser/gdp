'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

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


    def get_vtarget(self):
        return None


    def set_interface_frequency(self, target_frequency):
        pass


    def enter_session(self):
        packet = [AtmelAVR109Defs.commands["ENTER_PROG_MODE"]]
        self._send_command(packet, returns_data=False)


    def exit_session(self):
        pass


    def erase_memory(self, memory_space, offset):
        if memory_space is None:
            packet = [AtmelAVR109Defs.commands["CHIP_ERASE"]]
            self._send_command(packet, returns_data=False)
        else:
            raise ProtocolError("The specified tool cannot erase the requested memory space.")


    def read_memory(self, memory_space, offset, length):
        if memory_space == "signature":
            packet = [AtmelAVR109Defs.commands["READ_SIGNATURE"]]
            resp = self._send_command(packet, returns_data=True)
            return resp[offset : offset + length : -1]
        raise NotImplementedError()


    def write_memory(self, memory_space, offset, data):
        raise NotImplementedError()


    def open(self):
        packet = [AtmelAVR109Defs.commands["SET_LED"]]
        packet.append(1)
        self._send_command(packet, returns_data=False)


    def close(self):
        packet = [AtmelAVR109Defs.commands["CLEAR_LED"]]
        packet.append(1)
        self._send_command(packet, returns_data=False)
