'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

import math

from protocols import *


class AtmelSTKV2Defs(object):
	CMD_SIGN_ON                 = 0x01
	CMD_SET_PARAMETER           = 0x02
	CMD_GET_PARAMETER           = 0x03
	CMD_OSCCAL                  = 0x05
	CMD_LOAD_ADDRESS            = 0x06
	CMD_FIRMWARE_UPGRADE        = 0x07
	CMD_RESET_PROTECTION        = 0x0A
	CMD_ENTER_PROGMODE_ISP      = 0x10
	CMD_LEAVE_PROGMODE_ISP      = 0x11
	CMD_CHIP_ERASE_ISP          = 0x12
	CMD_PROGRAM_FLASH_ISP       = 0x13
	CMD_READ_FLASH_ISP          = 0x14
	CMD_PROGRAM_EEPROM_ISP      = 0x15
	CMD_READ_EEPROM_ISP         = 0x16
	CMD_PROGRAM_FUSE_ISP        = 0x17
	CMD_READ_FUSE_ISP           = 0x18
	CMD_PROGRAM_LOCK_ISP        = 0x19
	CMD_READ_LOCK_ISP           = 0x1A
	CMD_READ_SIGNATURE_ISP      = 0x1B
	CMD_READ_OSCCAL_ISP         = 0x1C
	CMD_SPI_MULTI               = 0x1D
	CMD_XPROG                   = 0x50
	CMD_XPROG_SETMODE           = 0x51

	STATUS_CMD_OK               = 0x00
	STATUS_CMD_TOUT             = 0x80
	STATUS_RDY_BSY_TOUT         = 0x81
	STATUS_SET_PARAM_MISSING    = 0x82
	STATUS_CMD_FAILED           = 0xC0
	STATUS_CMD_UNKNOWN          = 0xC9
	STATUS_ISP_READY            = 0x00
	STATUS_CONN_FAIL_MOSI       = 0x01
	STATUS_CONN_FAIL_RST        = 0x02
	STATUS_CONN_FAIL_SCK        = 0x04
	STATUS_TGT_NOT_DETECTED     = 0x10
	STATUS_TGT_REVERSE_INSERTED = 0x20

	PARAM_BUILD_NUMBER_LOW      = 0x80
	PARAM_BUILD_NUMBER_HIGH     = 0x81
	PARAM_HW_VER                = 0x90
	PARAM_SW_MAJOR              = 0x91
	PARAM_SW_MINOR              = 0x92
	PARAM_VTARGET               = 0x94
	PARAM_SCK_DURATION          = 0x98
	PARAM_RESET_POLARITY        = 0x9E
	PARAM_STATUS_TGT_CONN       = 0xA1
	PARAM_DISCHARGEDELAY        = 0xA4


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
			raise ValueError("No response received from tool.")

		if packet_in[0] != packet_out[0]:
			raise ValueError("Invalid response received from tool.")

		if packet_in[1] != AtmelSTKV2Defs.STATUS_CMD_OK:
			raise ValueError("Command 0x%x failed with status 0x%x." % (packet_out[0], packet_in[1]))

		return packet_in


	def _set_address(self, address):
		packet = [AtmelSTKV2Defs.CMD_LOAD_ADDRESS]
		packet.extend([address >> (8 * x) & 0xFF for x in xrange(4)])
		self._trancieve(packet)


	def _sign_on(self):
		resp = self._trancieve([AtmelSTKV2Defs.CMD_SIGN_ON])
		self.tool_sign_on_string = ''.join([chr(c) for c in resp[3 : ]])


	def _reset_protection(self):
		if "AVRISP" in self.tool_sign_on_string:
			self._trancieve([AtmelSTKV2Defs.CMD_RESET_PROTECTION])


	def _set_reset_polarity(self, idle_level):
		self._trancieve([AtmelSTKV2Defs.CMD_SET_PARAMETER, AtmelSTKV2Defs.PARAM_RESET_POLARITY, idle_level])


	def get_vtarget(self):
		resp = self._trancieve([AtmelSTKV2Defs.CMD_GET_PARAMETER, AtmelSTKV2Defs.PARAM_VTARGET])

		measured_vtarget = (float(resp[2]) / 10)
		return measured_vtarget


	def set_interface_frequency(self, target_frequency):
		if not target_frequency:
			raise ValueError("Target communication frequency not specified.")

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
				raise ValueError("Specified ISP frequency is not obtainable for the current tool.")

			self._trancieve([AtmelSTKV2Defs.CMD_SET_PARAMETER, AtmelSTKV2Defs.PARAM_SCK_DURATION, int(sck_dur)])
		else:
			raise NotImplementedError()


	def enter_session(self):
		if self.interface == "isp":
			packet = [AtmelSTKV2Defs.CMD_ENTER_PROGMODE_ISP]
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
			packet = [AtmelSTKV2Defs.CMD_LEAVE_PROGMODE_ISP]
			packet.append(self.device.get_param("isp_interface", "IspLeaveProgMode_preDelay"))
			packet.append(self.device.get_param("isp_interface", "IspLeaveProgMode_postDelay"))
		else:
			raise NotImplementedError()

		self._trancieve(packet)


	def erase_memory(self, memory_space):
		if memory_space is None:
			if self.interface == "isp":
				packet = [AtmelSTKV2Defs.CMD_CHIP_ERASE_ISP]
				packet.append(self.device.get_param("isp_interface", "IspChipErase_eraseDelay"))
				packet.append(self.device.get_param("isp_interface", "IspChipErase_pollMethod"))
				packet.extend([0xAC, 0x80, 0x00, 0x00])
			else:
				raise NotImplementedError()
		else:
			raise ValueError("The specified tool cannot erase the requested memory space.")

		self._trancieve(packet)


	def read_memory(self, memory_space, offset, length):
		mem_contents = []

		if memory_space is None:
			return ValueError("Read failed as memory space not set.")
		elif memory_space == "signature":
			if self.interface == "isp":
				for x in xrange(length):
					packet = [AtmelSTKV2Defs.CMD_READ_SIGNATURE_ISP]
					packet.append(self.device.get_param("isp_interface", "IspReadSign_pollIndex"))
					packet.extend([0x30, 0x80, offset + x, 0x00])
					resp = self._trancieve(packet)

					mem_contents.append(resp[2])
			else:
				raise NotImplementedError()
		elif memory_space == "lockbits":
			if self.interface == "isp":
				packet = [AtmelSTKV2Defs.CMD_READ_LOCK_ISP]
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
					packet = [AtmelSTKV2Defs.CMD_READ_FUSE_ISP]
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
					if memory_space == "eeprom":
						packet = [AtmelSTKV2Defs.CMD_READ_EEPROM_ISP]
						packet.extend([blocksize >> 8, blocksize & 0xFF])
						packet.append(0xA0)
					else:
						packet = [AtmelSTKV2Defs.CMD_READ_FLASH_ISP]
						packet.extend([blocksize >> 8, blocksize & 0xFF])
						packet.append(0x20)

					page_address = start_address + (block * blocksize)

					self._set_address(page_address)
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
			return ValueError("Write failed as memory space not set.")
		elif memory_space == "lockbits":
			if self.interface == "isp":
				packet = [AtmelSTKV2Defs.CMD_PROGRAM_LOCK_ISP]
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
					packet = [AtmelSTKV2Defs.CMD_PROGRAM_FUSE_ISP]
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
					if memory_space == "flash":
						packet = [AtmelSTKV2Defs.CMD_PROGRAM_FLASH_ISP]
					else:
						packet = [AtmelSTKV2Defs.CMD_PROGRAM_EEPROM_ISP]

					packet.extend([blocksize >> 8, blocksize & 0xFF])
					packet.append(self.device.get_param("isp_interface", "IspProgram%s_mode" % memory_space.capitalize()) | 0x80)
					packet.append(self.device.get_param("isp_interface", "IspProgram%s_delay" % memory_space.capitalize()))
					packet.append(self.device.get_param("isp_interface", "IspProgram%s_cmd1" % memory_space.capitalize()))
					packet.append(self.device.get_param("isp_interface", "IspProgram%s_cmd2" % memory_space.capitalize()))
					packet.append(self.device.get_param("isp_interface", "IspProgram%s_cmd3" % memory_space.capitalize()))
					packet.append(self.device.get_param("isp_interface", "IspProgram%s_pollVal1" % memory_space.capitalize()))
					packet.append(self.device.get_param("isp_interface", "IspProgram%s_pollVal2" % memory_space.capitalize()))

					page_address = start_address + (block * blocksize)
					page_data = []

					if alignment_bytes > 0:
						page_data.extend(self.read_memory(memory_space, page_address, alignment_bytes))
						alignment_bytes = 0

					page_data.extend(data[block * blocksize : (block + 1) * blocksize])

					if (len(page_data) < blocksize):
						page_data.extend(self.read_memory(memory_space, page_address + len(page_data), blocksize - len(page_data)))

					packet.extend(page_data)

					self._set_address(page_address)
					self._trancieve(packet)
			else:
				raise NotImplementedError()
		else:
			raise NotImplementedError()


	def open(self):
		self._sign_on()
		self._set_reset_polarity(1)
		self._reset_protection()


	def close(self):
		pass
