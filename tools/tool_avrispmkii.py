'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from tools.tool import *
from transports.transport_usb import *
from protocols.protocol_atmelv2 import *

class ToolAVRISPMKII(Tool):
	transport = TransportUSB(vid=0x03EB, pid=0x2104)
	protocol  = ProtocolAtmelV2(transport)

	AVRISP_MKII_WRITE_ENDPOINT = 2
	AVRISP_MKII_READ_ENDPOINT  = 2


	def open(self):
		if self.transport.open() == False:
			return False

		return self.protocol.init()


	def close(self):
		return self.transport.close()


	def read(self, length):
		return self.transport.read(self.AVRISP_MKII_READ_ENDPOINT, length, 0, 100)


	def write(self, data):
		self.transport.write(self.AVRISP_MKII_WRITE_ENDPOINT, data, 0, 100)
