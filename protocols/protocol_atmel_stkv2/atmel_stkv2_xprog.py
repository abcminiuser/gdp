'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from core import *
from protocols import *
from protocols.protocol_atmel_stkv2.atmel_stkv2_base import *


class ProtocolAtmelSTKV2_XPROG(ProtocolAtmelSTKV2_Base):
    def set_interface_frequency(self, target_frequency):
        raise NotImplementedError()


    def enter_session(self):
        raise NotImplementedError()


    def exit_session(self):
        raise NotImplementedError()


    def erase_memory(self, memory_space):
        raise NotImplementedError()


    def read_memory(self, memory_space, offset, length):
        raise NotImplementedError()


    def write_memory(self, memory_space, offset, data):
        raise NotImplementedError()
