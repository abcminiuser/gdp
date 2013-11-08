'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from protocols import *


class AtmelSTKV2Defs(object):
    commands = {
        "SIGN_ON"              : 0x01,
        "SET_PARAMETER"        : 0x02,
        "GET_PARAMETER"        : 0x03,
        "OSCCAL"               : 0x05,
        "LOAD_ADDRESS"         : 0x06,
        "FIRMWARE_UPGRADE"     : 0x07,
        "RESET_PROTECTION"     : 0x0A,
        "ENTER_PROGMODE_ISP"   : 0x10,
        "LEAVE_PROGMODE_ISP"   : 0x11,
        "CHIP_ERASE_ISP"       : 0x12,
        "PROGRAM_FLASH_ISP"    : 0x13,
        "READ_FLASH_ISP"       : 0x14,
        "PROGRAM_EEPROM_ISP"   : 0x15,
        "READ_EEPROM_ISP"      : 0x16,
        "PROGRAM_FUSE_ISP"     : 0x17,
        "READ_FUSE_ISP"        : 0x18,
        "PROGRAM_LOCK_ISP"     : 0x19,
        "READ_LOCK_ISP"        : 0x1A,
        "READ_SIGNATURE_ISP"   : 0x1B,
        "READ_OSCCAL_ISP"      : 0x1C,
        "SPI_MULTI"            : 0x1D,
        "XPROG"                : 0x50,
        "XPROG_SETMODE"        : 0x51
    }

    status_codes = {
        "CMD_OK"               : 0x00,
        "CMD_TOUT"             : 0x80,
        "RDY_BSY_TOUT"         : 0x81,
        "SET_PARAM_MISSING"    : 0x82,
        "CMD_FAILED"           : 0xC0,
        "CMD_UNKNOWN"          : 0xC9,
        "ISP_READY"            : 0x00,
        "CONN_FAIL_MOSI"       : 0x01,
        "CONN_FAIL_RST"        : 0x02,
        "CONN_FAIL_SCK"        : 0x04,
        "TGT_NOT_DETECTED"     : 0x10,
        "TGT_REVERSE_INSERTED" : 0x20
    }

    params = {
        "BUILD_NUMBER_LOW"     : 0x80,
        "BUILD_NUMBER_HIGH"    : 0x81,
        "HW_VER"               : 0x90,
        "SW_MAJOR"             : 0x91,
        "SW_MINOR"             : 0x92,
        "VTARGET"              : 0x94,
        "SCK_DURATION"         : 0x98,
        "RESET_POLARITY"       : 0x9E,
        "STATUS_TGT_CONN"      : 0xA1,
        "DISCHARGEDELAY"       : 0xA4
    }


    @staticmethod
    def find(dictionary, find_value):
        for key, value in dictionary.iteritems():
            if value == find_value:
                return key

        return None


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
