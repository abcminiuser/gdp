'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from core import *
from protocols import *
from protocols.protocol_atmel_stkv2.atmel_stkv2_base import *

import math


class ProtocolAtmelSTKV2_ISP(ProtocolAtmelSTKV2_Base):
    def set_interface_frequency(self, target_frequency):
        if not target_frequency:
            raise ProtocolError("Target communication frequency not specified.")

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


    def enter_session(self):
        packet = [AtmelSTKV2Defs.commands["ENTER_PROGMODE_ISP"]]
        packet.append(self.device.get_property("isp_interface", "IspEnterProgMode_timeout"))
        packet.append(self.device.get_property("isp_interface", "IspEnterProgMode_stabDelay"))
        packet.append(self.device.get_property("isp_interface", "IspEnterProgMode_cmdexeDelay"))
        packet.append(self.device.get_property("isp_interface", "IspEnterProgMode_synchLoops"))
        packet.append(self.device.get_property("isp_interface", "IspEnterProgMode_byteDelay"))
        packet.append(self.device.get_property("isp_interface", "IspEnterProgMode_pollValue"))
        packet.append(self.device.get_property("isp_interface", "IspEnterProgMode_pollIndex"))
        packet.extend([0xAC, 0x53, 0x00, 0x00])
        self._trancieve(packet)


    def exit_session(self):
        packet = [AtmelSTKV2Defs.commands["LEAVE_PROGMODE_ISP"]]
        packet.append(self.device.get_property("isp_interface", "IspLeaveProgMode_preDelay"))
        packet.append(self.device.get_property("isp_interface", "IspLeaveProgMode_postDelay"))
        self._trancieve(packet)


    def erase_memory(self, memory_space, offset):
        if memory_space is None:
            packet = [AtmelSTKV2Defs.commands["CHIP_ERASE_ISP"]]
            packet.append(self.device.get_property("isp_interface", "IspChipErase_eraseDelay"))
            packet.append(self.device.get_property("isp_interface", "IspChipErase_pollMethod"))
            packet.extend([0xAC, 0x80, 0x00, 0x00])
            self._trancieve(packet)
        else:
            raise ProtocolError("The specified tool cannot erase the requested memory space.")


    def read_memory(self, memory_space, offset, length):
        mem_contents = []

        if memory_space is None:
            raise ProtocolError("Read failed as memory space not set.")
        elif memory_space == "signature":
            for x in xrange(length):
                packet = [AtmelSTKV2Defs.commands["READ_SIGNATURE_ISP"]]
                packet.append(self.device.get_property("isp_interface", "IspReadSign_pollIndex"))
                packet.extend([0x30, 0x80, offset + x, 0x00])
                resp = self._trancieve(packet)

                mem_contents.append(resp[2])
        elif memory_space == "lockbits":
            packet = [AtmelSTKV2Defs.commands["READ_LOCK_ISP"]]
            packet.append(self.device.get_property("isp_interface", "IspReadLock_pollIndex"))
            packet.extend([0x58, 0x00, 0x00, 0x00])
            resp = self._trancieve(packet)

            mem_contents.append(resp[2])
        elif memory_space == "fuses":
            fuse_commands = {
                    0 : [0x50, 0x00, 0x00, 0x00],
                    1 : [0x50, 0x08, 0x00, 0x00],
                    2 : [0x58, 0x00, 0x00, 0x00]
                }

            for x in xrange(length):
                packet = [AtmelSTKV2Defs.commands["READ_FUSE_ISP"]]
                packet.append(self.device.get_property("isp_interface", "IspReadFuse_pollIndex"))
                packet.extend(fuse_commands[offset + x])
                resp = self._trancieve(packet)

                mem_contents.append(resp[2])
        elif memory_space in ["eeprom", "flash"]:
            blocksize = self.device.get_property("isp_interface", "IspRead%s_blockSize" % memory_space.capitalize())

            for (address, chunklen) in Util.chunk_address(length, blocksize, offset):
                if memory_space == "eeprom":
                    self._set_address(address)

                    packet = [AtmelSTKV2Defs.commands["READ_EEPROM_ISP"]]
                    packet.extend([chunklen >> 8, chunklen & 0xFF])
                    packet.append(0xA0)
                else:
                    self._set_address(address >> 1)

                    packet = [AtmelSTKV2Defs.commands["READ_FLASH_ISP"]]
                    packet.extend([chunklen >> 8, chunklen & 0xFF])
                    packet.append(0x20)

                resp = self._trancieve(packet)

                page_data = resp[2 : -1]
                mem_contents.extend(page_data[0 : chunklen])

            mem_contents = mem_contents[0 : length]
        else:
            raise NotImplementedError()

        return mem_contents


    def write_memory(self, memory_space, offset, data):
        if memory_space is None:
            raise ProtocolError("Write failed as memory space not set.")
        elif memory_space == "lockbits":
            packet = [AtmelSTKV2Defs.commands["PROGRAM_LOCK_ISP"]]
            packet.extend([0xAC, 0xE0, 0x00, 0xC0 | data[0]])
            self._trancieve(packet)
        elif memory_space == "fuses":
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
        elif memory_space in ["eeprom", "flash"]:
            blocksize = self.device.get_property("isp_interface", "IspProgram%s_blockSize" % memory_space.capitalize())

            for (address, chunk) in Util.chunk_data(data, blocksize, offset):
                if memory_space == "eeprom":
                    self._set_address(address)
                    packet = [AtmelSTKV2Defs.commands["PROGRAM_EEPROM_ISP"]]
                else:
                    self._set_address(address >> 1)
                    packet = [AtmelSTKV2Defs.commands["PROGRAM_FLASH_ISP"]]

                packet.extend([blocksize >> 8, blocksize & 0xFF])
                packet.append(self.device.get_property("isp_interface", "IspProgram%s_mode" % memory_space.capitalize()) | 0x80)
                packet.append(self.device.get_property("isp_interface", "IspProgram%s_delay" % memory_space.capitalize()))
                packet.append(self.device.get_property("isp_interface", "IspProgram%s_cmd1" % memory_space.capitalize()))
                packet.append(self.device.get_property("isp_interface", "IspProgram%s_cmd2" % memory_space.capitalize()))
                packet.append(self.device.get_property("isp_interface", "IspProgram%s_cmd3" % memory_space.capitalize()))
                packet.append(self.device.get_property("isp_interface", "IspProgram%s_pollVal1" % memory_space.capitalize()))
                packet.append(self.device.get_property("isp_interface", "IspProgram%s_pollVal2" % memory_space.capitalize()))
                packet.extend(chunk)

                self._trancieve(packet)
        else:
            raise NotImplementedError()
