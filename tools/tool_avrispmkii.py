'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from tools import *
from transports import *


class ToolAVRISPMKII(Tool):
	transport = TransportUSB(vid=0x03EB, pid=0x2104, read_ep=2, write_ep=2)


	def open(self):
		if self.transport.open() == False:
			return False


	def close(self):
		return self.transport.close()


	def read(self, length):
		return self.transport.read(length, 100)


	def write(self, data):
		self.transport.write(data, 100)
