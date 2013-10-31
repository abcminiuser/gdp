'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from tools import *
from transports import *


class ToolAtmelAVRISPMKII(Tool):
	transport = None


	def __init__(self, port=None):
		if port is None:
			self.transport = TransportJungoUSB(vid=0x03EB, pid=0x2104, read_ep=2, write_ep=2)
		else:
			raise LookupError("Unsupported port for the specified tool.")


	def open(self):
		return self.transport.open()


	def close(self):
		return self.transport.close()


	def read(self):
		return self.transport.read()


	def write(self, data):
		self.transport.write(data)
