'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)

   Release under a MIT license; see LICENSE.txt for details.
'''

from protocols import *
from protocols.protocol_atmel_jtagv2.atmel_jtagv2_defs import *


class ProtocolAtmelJTAGV2(Protocol):
    def __init__(self, parent, device, interface):
        self.parent    = parent
        self.device    = device
        self.interface = interface


    def _trancieve(self, packet_out):
        self.write(packet_out)
        packet_in = self.read()

        if packet_in is None:
            raise ProtocolError("No response received from tool.")

        return packet_in


    def _sign_on(self):
        self._trancieve([AtmelJTAGV2Defs.commands["SIGN_ON"]])


    def _sign_off(self):
        self._trancieve([AtmelJTAGV2Defs.commands["SIGN_OFF"]])


    def reset_target(self, address):
        raise NotImplementedError


    def get_vtarget(self):
        raise NotImplementedError


    def set_interface_frequency(self, target_frequency):
        raise NotImplementedError


    def enter_session(self):
        raise NotImplementedError


    def exit_session(self):
        raise NotImplementedError


    def erase_memory(self, memory_space, offset):
        raise NotImplementedError()


    def read_memory(self, memory_space, offset, length):
        raise NotImplementedError()


    def write_memory(self, memory_space, offset, data):
        raise NotImplementedError()


    def open(self):
        self._sign_on()
        raise NotImplementedError()


    def close(self):
        self._sign_off()
        raise NotImplementedError()


    def read(self):
        return self.parent.read()


    def write(self, data):
        self.parent.write(data)
