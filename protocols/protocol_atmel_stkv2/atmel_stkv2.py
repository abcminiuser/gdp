'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from protocols import *
from protocols.protocol_atmel_stkv2.atmel_stkv2_isp import *
from protocols.protocol_atmel_stkv2.atmel_stkv2_hvpp import *
from protocols.protocol_atmel_stkv2.atmel_stkv2_hvsp import *
from protocols.protocol_atmel_stkv2.atmel_stkv2_xprog import *


class ProtocolAtmelSTKV2(Protocol):
    def __init__(self, parent, device, interface):
        interface_implementations = {
            "isp"  : ProtocolAtmelSTKV2_ISP,
            "hvsp" : ProtocolAtmelSTKV2_HVSP,
            "hvpp" : ProtocolAtmelSTKV2_HVPP,
            "pdi"  : ProtocolAtmelSTKV2_XPROG,
            "tpi"  : ProtocolAtmelSTKV2_XPROG
        }

        if "xmega" in device.get_architecture():
            interface_implementations["jtag"] = ProtocolAtmelSTKV2_XPROG

        try:
            self.handler = interface_implementations[interface](parent, device, interface)
        except KeyError:
            raise NotImplementedError


    def reset_target(self, address):
        self.handler.reset_target(address)


    def get_vtarget(self):
        return self.handler.get_vtarget()


    def set_interface_frequency(self, target_frequency):
        self.handler.set_interface_frequency(target_frequency)


    def enter_session(self):
        self.handler.enter_session()


    def exit_session(self):
        self.handler.exit_session()


    def erase_memory(self, memory_space, offset):
        self.handler.erase_memory(memory_space, offset)


    def read_memory(self, memory_space, offset, length):
        return self.handler.read_memory(memory_space, offset, length)


    def write_memory(self, memory_space, offset, data):
        self.handler.write_memory(memory_space, offset, data)


    def open(self):
        self.handler.open()


    def close(self):
        self.handler.close()


    def read(self):
        return self.handler.read()


    def write(self, data):
        self.handler.write(data)
