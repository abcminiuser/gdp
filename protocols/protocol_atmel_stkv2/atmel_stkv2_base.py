'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from protocols import *
from protocols.protocol_atmel_stkv2.atmel_stkv2_defs import *


class ProtocolAtmelSTKV2_Base(object):
    def __init__(self, tool, device):
        self.tool = tool
        self.device = device

        self.tool_sign_on_string = None


    def _trancieve(self, packet_out):
        self.tool.write(packet_out)
        packet_in = self.tool.read()

        if packet_in is None:
            raise ProtocolError("No response received from tool.")

        if packet_in[0] != packet_out[0]:
            raise ProtocolError("Invalid response received from tool.")

        if packet_in[1] != AtmelSTKV2Defs.status_codes["CMD_OK"]:
            raise ProtocolError("Command %s failed with status %s." %
                                (AtmelSTKV2Defs.find(AtmelSTKV2Defs.commands, packet_out[0]),
                                 AtmelSTKV2Defs.find(AtmelSTKV2Defs.status_codes, packet_in[0])))

        return packet_in


    def _set_address(self, address):
        packet = [AtmelSTKV2Defs.commands["LOAD_ADDRESS"]]
        packet.append(address >> 24)
        packet.append(address >> 16)
        packet.append(address >> 8)
        packet.append(address & 0xFF)
        self._trancieve(packet)


    def _set_param(self, param, value):
        packet = [AtmelSTKV2Defs.commands["SET_PARAMETER"]]
        packet.append(param)
        packet.append(value)
        self._trancieve(packet)


    def _get_param(self, param):
        packet = [AtmelSTKV2Defs.commands["GET_PARAMETER"]]
        packet.append(param)
        return self._trancieve(packet)[2]


    def _sign_on(self):
        resp = self._trancieve([AtmelSTKV2Defs.commands["SIGN_ON"]])
        self.tool_sign_on_string = ''.join([chr(c) for c in resp[3 : ]])


    def _reset_protection(self):
        if "AVRISP" in self.tool_sign_on_string:
            self._trancieve([AtmelSTKV2Defs.commands["RESET_PROTECTION"]])


    def get_vtarget(self):
        vtarget_raw = self._get_param(AtmelSTKV2Defs.params["VTARGET"])

        measured_vtarget = (float(vtarget_raw) / 10)
        return measured_vtarget


    def open(self):
        self._sign_on()
        self._set_param(AtmelSTKV2Defs.params["RESET_POLARITY"], 1)
        self._reset_protection()


    def close(self):
        pass
