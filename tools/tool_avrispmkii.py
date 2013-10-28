'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from tools.tool import *
from transports.transport_usb import *

class ToolAVRISPMKII(Tool):
	transport = TransportUSB(vid=0x03EB, pid=0x2104)

	def open(self):
		return self.transport.open()

	def close(self):
		return self.transport.close()
