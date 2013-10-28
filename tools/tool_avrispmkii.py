'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from tools.tool import *
from transports.transport_usb import *

class ToolAVRISPMKII(Tool):
	transport = TransportUSB(vid=0x03EB, pid=0x2104)

	def open(self):
		if self.transport.open() == False:
			return False

		self.transport.write(2, [0x01], 100)
		rsp = self.transport.read(2, 64, 100)
		print ''.join([chr(x) for x in rsp])

	def close(self):
		return self.transport.close()
