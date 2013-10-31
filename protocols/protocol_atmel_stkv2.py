'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from protocols import *


V2_CMD_SIGN_ON                 = 0x01
V2_CMD_SET_PARAMETER           = 0x02
V2_CMD_GET_PARAMETER           = 0x03
V2_CMD_OSCCAL                  = 0x05
V2_CMD_LOAD_ADDRESS            = 0x06
V2_CMD_FIRMWARE_UPGRADE        = 0x07
V2_CMD_RESET_PROTECTION        = 0x0A
V2_CMD_ENTER_PROGMODE_ISP      = 0x10
V2_CMD_LEAVE_PROGMODE_ISP      = 0x11
V2_CMD_CHIP_ERASE_ISP          = 0x12
V2_CMD_PROGRAM_FLASH_ISP       = 0x13
V2_CMD_READ_FLASH_ISP          = 0x14
V2_CMD_PROGRAM_EEPROM_ISP      = 0x15
V2_CMD_READ_EEPROM_ISP         = 0x16
V2_CMD_PROGRAM_FUSE_ISP        = 0x17
V2_CMD_READ_FUSE_ISP           = 0x18
V2_CMD_PROGRAM_LOCK_ISP        = 0x19
V2_CMD_READ_LOCK_ISP           = 0x1A
V2_CMD_READ_SIGNATURE_ISP      = 0x1B
V2_CMD_READ_OSCCAL_ISP         = 0x1C
V2_CMD_SPI_MULTI               = 0x1D
V2_CMD_XPROG                   = 0x50
V2_CMD_XPROG_SETMODE           = 0x51

V2_STATUS_CMD_OK               = 0x00
V2_STATUS_CMD_TOUT             = 0x80
V2_STATUS_RDY_BSY_TOUT         = 0x81
V2_STATUS_SET_PARAM_MISSING    = 0x82
V2_STATUS_CMD_FAILED           = 0xC0
V2_STATUS_CMD_UNKNOWN          = 0xC9
V2_STATUS_ISP_READY            = 0x00
V2_STATUS_CONN_FAIL_MOSI       = 0x01
V2_STATUS_CONN_FAIL_RST        = 0x02
V2_STATUS_CONN_FAIL_SCK        = 0x04
V2_STATUS_TGT_NOT_DETECTED     = 0x10
V2_STATUS_TGT_REVERSE_INSERTED = 0x20

V2_PARAM_BUILD_NUMBER_LOW      = 0x80
V2_PARAM_BUILD_NUMBER_HIGH     = 0x81
V2_PARAM_HW_VER                = 0x90
V2_PARAM_SW_MAJOR              = 0x91
V2_PARAM_SW_MINOR              = 0x92
V2_PARAM_VTARGET               = 0x94
V2_PARAM_SCK_DURATION          = 0x98
V2_PARAM_RESET_POLARITY        = 0x9E
V2_PARAM_STATUS_TGT_CONN       = 0xA1
V2_PARAM_DISCHARGEDELAY        = 0xA4


class ProtocolAtmelSTKV2(Protocol):
	tool      = None
	device    = None
	interface = None


	tool_sign_on_string = None


	def __init__(self, tool, device, interface):
		self.tool      = tool
		self.device    = device
		self.interface = interface


	def _trancieve(self, packet_out):
		self.tool.write(packet_out)
		packet_in = self.tool.read()

		if packet_in[0] != packet_out[0]:
			raise ValueError("Invalid response received from tool.")

		if packet_in[1] != V2_STATUS_CMD_OK:
			raise ValueError("Command failed with status %d." % packet_in[1])

		return packet_in


	def _sign_off(self):
		self._trancieve([V2_CMD_SIGN_OFF])


	def _sign_on(self):
		resp = self._trancieve([V2_CMD_SIGN_ON])
		self.tool_sign_on_string = ''.join([chr(c) for c in resp[3 : ]])


	def _reset_protection(self):
		self._trancieve([V2_CMD_RESET_PROTECTION])


	def _set_reset_polarity(self, idle_level):
		self._trancieve([V2_CMD_SET_PARAMETER, V2_PARAM_RESET_POLARITY, idle_level])


	def get_vtarget(self):
		resp = self._trancieve([V2_CMD_GET_PARAMETER, V2_PARAM_VTARGET])

		measured_vtarget = (float(resp[2]) / 10)
		return measured_vtarget


	def set_interface_frequency(self, target_frequency):
		if not target_frequency:
			raise ValueError("Target communication frequency not specified.")

		if self.interface == "isp":
			sck_dur = 0;

			if self.tool_sign_on_string == "AVRISP_MK2":
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

			self._trancieve([V2_CMD_SET_PARAMETER, V2_PARAM_SCK_DURATION, sck_dur])
		elif self.interface == "pdi":
			raise NotImplementedError()
		elif self.interface == "tpi":
			raise NotImplementedError()


	def open(self):
		self._sign_on()
		self._set_reset_polarity(1)
		self._reset_protection()


	def close(self):
		pass
