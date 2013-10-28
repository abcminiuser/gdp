'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from protocols.protocol import *

V2_CMD_SIGN_OFF           = 0x00
V2_CMD_SIGN_ON            = 0x01
V2_CMD_SET_PARAMETER      = 0x02
V2_CMD_GET_PARAMETER      = 0x03
V2_CMD_OSCCAL             = 0x05
V2_CMD_LOAD_ADDRESS       = 0x06
V2_CMD_FIRMWARE_UPGRADE   = 0x07
V2_CMD_RESET_PROTECTION   = 0x0A
V2_CMD_ENTER_PROGMODE_ISP = 0x10
V2_CMD_LEAVE_PROGMODE_ISP = 0x11
V2_CMD_CHIP_ERASE_ISP     = 0x12
V2_CMD_PROGRAM_FLASH_ISP  = 0x13
V2_CMD_READ_FLASH_ISP     = 0x14
V2_CMD_PROGRAM_EEPROM_ISP = 0x15
V2_CMD_READ_EEPROM_ISP    = 0x16
V2_CMD_PROGRAM_FUSE_ISP   = 0x17
V2_CMD_READ_FUSE_ISP      = 0x18
V2_CMD_PROGRAM_LOCK_ISP   = 0x19
V2_CMD_READ_LOCK_ISP      = 0x1A
V2_CMD_READ_SIGNATURE_ISP = 0x1B
V2_CMD_READ_OSCCAL_ISP    = 0x1C
V2_CMD_SPI_MULTI          = 0x1D
V2_CMD_XPROG              = 0x50
V2_CMD_XPROG_SETMODE      = 0x51

class ProtocolAtmelV2(Protocol):
	tool   = None
	device = None


	def __init__(self, tool, device):
		self.tool = tool
		self.device = device


	def open(self):
		self.tool.open()

		self.tool.write([V2_CMD_SIGN_ON])
		rsp = self.tool.read(64)
		print(''.join([chr(x) for x in rsp]))


	def close(self):
		self.tool.close()
