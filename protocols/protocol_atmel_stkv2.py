'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

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
			sck_dur = 0;

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
					sck_dur = ceil(1 / (2 * B * target_frequency * 271.27e-9) - 10 / 12);
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
					sck_dur = ceil(1 / (2 * B * target_frequency * 135.63e-9) - 10 / 12);

			self._trancieve([AtmelSTKV2Defs.CMD_SET_PARAMETER, AtmelSTKV2Defs.PARAM_SCK_DURATION, sck_dur])
		else:
			raise NotImplementedError()


	def enter_session(self):
		if self.interface == "isp":
			packet = [AtmelSTKV2Defs.CMD_ENTER_PROGMODE_ISP]
			packet.append(self.device.get_interface_param("isp", "IspEnterProgMode_timeout"))
			packet.append(self.device.get_interface_param("isp", "IspEnterProgMode_stabDelay"))
			packet.append(self.device.get_interface_param("isp", "IspEnterProgMode_cmdexeDelay"))
			packet.append(self.device.get_interface_param("isp", "IspEnterProgMode_synchLoops"))
			packet.append(self.device.get_interface_param("isp", "IspEnterProgMode_byteDelay"))
			packet.append(self.device.get_interface_param("isp", "IspEnterProgMode_pollValue"))
			packet.append(self.device.get_interface_param("isp", "IspEnterProgMode_pollIndex"))
			packet.extend([0xAC, 0x53, 0x00, 0x00])
		else:
			raise NotImplementedError()

		self._trancieve(packet)


	def exit_session(self):
		if self.interface == "isp":
			packet = [AtmelSTKV2Defs.CMD_LEAVE_PROGMODE_ISP]
			packet.append(self.device.get_interface_param("isp", "IspLeaveProgMode_preDelay"))
			packet.append(self.device.get_interface_param("isp", "IspLeaveProgMode_postDelay"))
		else:
			raise NotImplementedError()

		self._trancieve(packet)


	def open(self):
		self._sign_on()
		self._set_reset_polarity(1)
		self._reset_protection()


	def close(self):
		pass
