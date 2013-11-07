'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

import math

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


class ProtocolAtmelSTKV2(Protocol):
    def __init__(self, tool, device, interface):
        self.tool      = tool
        self.device    = device
        self.interface = interface

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


    def set_interface_frequency(self, target_frequency):
        if not target_frequency:
            raise ProtocolError("Target communication frequency not specified.")

        if self.interface == "isp":
            sck_dur = 0

            if "AVRISP" in self.tool_sign_on_string:
                if target_frequency >= 921600:
                    sck_dur = 0;
                elif target_frequency >= 230400:
                    sck_dur = 1;
                elif target_frequency >= 57600:
                    sck_dur = 2;
                elif target_frequency >= 28800:
                    sck_dur = 3;
                else:
                    sck_dur = math.ceil(1.0 / (2 * 12.0 * target_frequency * 271.27e-9) - 10 / 12)
            else:
                if target_frequency >= 1843200:
                    sck_dur = 0;
                elif target_frequency >= 460800:
                    sck_dur = 1;
                elif target_frequency >= 115200:
                    sck_dur = 2;
                elif target_frequency >= 57600:
                    sck_dur = 3;
                else:
                    sck_dur = math.ceil(1.0 / (2 * 12.0 * target_frequency * 135.63e-9) - 10 / 12)

            if sck_dur > 0xFF:
                raise ProtocolError("Specified ISP frequency is not obtainable for the current tool.")

            self._set_param(AtmelSTKV2Defs.params["SCK_DURATION"], int(sck_dur))
        else:
            raise NotImplementedError()


    def enter_session(self):
        if self.interface == "isp":
            packet = [AtmelSTKV2Defs.commands["ENTER_PROGMODE_ISP"]]
            packet.append(self.device.get_param("isp_interface", "IspEnterProgMode_timeout"))
            packet.append(self.device.get_param("isp_interface", "IspEnterProgMode_stabDelay"))
            packet.append(self.device.get_param("isp_interface", "IspEnterProgMode_cmdexeDelay"))
            packet.append(self.device.get_param("isp_interface", "IspEnterProgMode_synchLoops"))
            packet.append(self.device.get_param("isp_interface", "IspEnterProgMode_byteDelay"))
            packet.append(self.device.get_param("isp_interface", "IspEnterProgMode_pollValue"))
            packet.append(self.device.get_param("isp_interface", "IspEnterProgMode_pollIndex"))
            packet.extend([0xAC, 0x53, 0x00, 0x00])
        else:
            raise NotImplementedError()

        self._trancieve(packet)


    def exit_session(self):
        if self.interface == "isp":
            packet = [AtmelSTKV2Defs.commands["LEAVE_PROGMODE_ISP"]]
            packet.append(self.device.get_param("isp_interface", "IspLeaveProgMode_preDelay"))
            packet.append(self.device.get_param("isp_interface", "IspLeaveProgMode_postDelay"))
        else:
            raise NotImplementedError()

        self._trancieve(packet)


    def erase_memory(self, memory_space):
        if memory_space is None:
            if self.interface == "isp":
                packet = [AtmelSTKV2Defs.commands["CHIP_ERASE_ISP"]]
                packet.append(self.device.get_param("isp_interface", "IspChipErase_eraseDelay"))
                packet.append(self.device.get_param("isp_interface", "IspChipErase_pollMethod"))
                packet.extend([0xAC, 0x80, 0x00, 0x00])
            else:
                raise NotImplementedError()
        else:
            raise ProtocolError("The specified tool cannot erase the requested memory space.")

        self._trancieve(packet)


    def read_memory(self, memory_space, offset, length):
        mem_contents = []

        if memory_space is None:
            return ProtocolError("Read failed as memory space not set.")
        elif memory_space == "signature":
            if self.interface == "isp":
                for x in xrange(length):
                    packet = [AtmelSTKV2Defs.commands["READ_SIGNATURE_ISP"]]
                    packet.append(self.device.get_param("isp_interface", "IspReadSign_pollIndex"))
                    packet.extend([0x30, 0x80, offset + x, 0x00])
                    resp = self._trancieve(packet)

                    mem_contents.append(resp[2])
            else:
                raise NotImplementedError()
        elif memory_space == "lockbits":
            if self.interface == "isp":
                packet = [AtmelSTKV2Defs.commands["READ_LOCK_ISP"]]
                packet.append(self.device.get_param("isp_interface", "IspReadLock_pollIndex"))
                packet.extend([0x58, 0x00, 0x00, 0x00])
                resp = self._trancieve(packet)
                mem_contents.append(resp[2])
            else:
                raise NotImplementedError()
        elif memory_space == "fuses":
            if self.interface == "isp":
                fuse_commands = {
                        0 : [0x50, 0x00, 0x00, 0x00],
                        1 : [0x50, 0x08, 0x00, 0x00],
                        2 : [0x58, 0x00, 0x00, 0x00]
                    }

                for x in xrange(length):
                    packet = [AtmelSTKV2Defs.commands["READ_FUSE_ISP"]]
                    packet.append(self.device.get_param("isp_interface", "IspReadFuse_pollIndex"))
                    packet.extend(fuse_commands[offset + x])
                    resp = self._trancieve(packet)
                    mem_contents.append(resp[2])
            else:
                raise NotImplementedError()
        elif memory_space in ["eeprom", "flash"]:
            if self.interface == "isp":
                blocksize = self.device.get_param("isp_interface", "IspRead%s_blockSize" % memory_space.capitalize())

                alignment_bytes = offset % blocksize
                start_address = offset - alignment_bytes

                blocks_to_read = int(math.ceil(length / float(blocksize)))

                for block in xrange(blocks_to_read):
                    page_address = start_address + (block * blocksize)

                    if memory_space == "eeprom":
                        self._set_address(page_address)

                        packet = [AtmelSTKV2Defs.commands["READ_EEPROM_ISP"]]
                        packet.extend([blocksize >> 8, blocksize & 0xFF])
                        packet.append(0xA0)
                    else:
                        self._set_address(page_address >> 1)

                        packet = [AtmelSTKV2Defs.commands["READ_FLASH_ISP"]]
                        packet.extend([blocksize >> 8, blocksize & 0xFF])
                        packet.append(0x20)

                    resp = self._trancieve(packet)

                    page_data = resp[2 : -1]

                    if length < blocksize:
                        mem_contents.extend(page_data[alignment_bytes : alignment_bytes + length])
                        length = 0
                    else:
                        mem_contents.extend(page_data[alignment_bytes : ])
                        length -= blocksize - alignment_bytes

                    alignment_bytes = 0
            else:
                raise NotImplementedError()
        else:
            raise NotImplementedError()

        return mem_contents


    def write_memory(self, memory_space, offset, data):
        if memory_space is None:
            return ProtocolError("Write failed as memory space not set.")
        elif memory_space == "lockbits":
            if self.interface == "isp":
                packet = [AtmelSTKV2Defs.commands["PROGRAM_LOCK_ISP"]]
                packet.extend([0xAC, 0xE0, 0x00, 0xC0 | data[0]])
                self._trancieve(packet)
            else:
                raise NotImplementedError()
        elif memory_space == "fuses":
            if self.interface == "isp":
                fuse_commands = {
                        0 : [0xAC, 0xA0, 0x00, 0x00],
                        1 : [0xAC, 0xA8, 0x00, 0x00],
                        2 : [0xAC, 0xA4, 0x00, 0x00]
                    }

                for x in xrange(length):
                    packet = [AtmelSTKV2Defs.commands["PROGRAM_FUSE_ISP"]]
                    packet.extend(fuse_commands[offset + x])
                    packet[-1] = data[offset + x]
                    self._trancieve(packet)
            else:
                raise NotImplementedError()
        elif memory_space in ["eeprom", "flash"]:
            if self.interface == "isp":
                blocksize = self.device.get_param("isp_interface", "IspProgram%s_blockSize" % memory_space.capitalize())

                alignment_bytes = offset % blocksize
                start_address = offset - alignment_bytes

                blocks_to_write = int(math.ceil(len(data) / float(blocksize)))

                for block in xrange(blocks_to_write):
                    page_address = start_address + (block * blocksize)
                    page_data = []

                    if alignment_bytes > 0:
                        page_data.extend(self.read_memory(memory_space, page_address, alignment_bytes))
                        alignment_bytes = 0

                    page_data.extend(data[block * blocksize : (block + 1) * blocksize])

                    if (len(page_data) < blocksize):
                        page_data.extend(self.read_memory(memory_space, page_address + len(page_data), blocksize - len(page_data)))

                    if memory_space == "eeprom":
                        self._set_address(page_address)

                        packet = [AtmelSTKV2Defs.commands["PROGRAM_EEPROM_ISP"]]
                    else:
                        self._set_address(page_address >> 1)

                        packet = [AtmelSTKV2Defs.commands["PROGRAM_FLASH_ISP"]]
                    packet.extend([blocksize >> 8, blocksize & 0xFF])
                    packet.append(self.device.get_param("isp_interface", "IspProgram%s_mode" % memory_space.capitalize()) | 0x80)
                    packet.append(self.device.get_param("isp_interface", "IspProgram%s_delay" % memory_space.capitalize()))
                    packet.append(self.device.get_param("isp_interface", "IspProgram%s_cmd1" % memory_space.capitalize()))
                    packet.append(self.device.get_param("isp_interface", "IspProgram%s_cmd2" % memory_space.capitalize()))
                    packet.append(self.device.get_param("isp_interface", "IspProgram%s_cmd3" % memory_space.capitalize()))
                    packet.append(self.device.get_param("isp_interface", "IspProgram%s_pollVal1" % memory_space.capitalize()))
                    packet.append(self.device.get_param("isp_interface", "IspProgram%s_pollVal2" % memory_space.capitalize()))
                    packet.extend(page_data)

                    self._trancieve(packet)
            else:
                raise NotImplementedError()
        else:
            raise NotImplementedError()


    def open(self):
        self._sign_on()
        self._set_param(AtmelSTKV2Defs.params["RESET_POLARITY"], 1)
        self._reset_protection()


    def close(self):
        pass
