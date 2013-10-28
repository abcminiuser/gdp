'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from tools.tool import *
from transports.transport_usb import *

AVRISP_MKII_WRITE_ENDPOINT = 2
AVRISP_MKII_READ_ENDPOINT  = 2


class ToolAVRISPMKII(Tool):
	transport = TransportUSB(vid=0x03EB, pid=0x2104)


	def open(self):
		if self.transport.open() == False:
			return False

	def close(self):
		return self.transport.close()


	def read(self, length):
		return self.transport.read(AVRISP_MKII_READ_ENDPOINT, length, 100)


	def write(self, data):
		self.transport.write(AVRISP_MKII_WRITE_ENDPOINT, data, 100)
