'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from tools import *
from transports import *
from protocols import *


class ToolAtmelAVRISPMKII(Tool):
	transport = None
	protocol  = None
	interface = None

	def __init__(self, device, port=None, interface="isp"):
		if port is None:
			self.transport = TransportJungoUSB(vid=0x03EB, pid=0x2104, read_ep=2, write_ep=2)
		else:
			raise LookupError("Unsupported port for the specified tool.")

		if interface in ["isp", "pdi", "tpi"]:
			self.interface = interface
		else:
			raise LookupError("Unsupported interface for the specified tool.")

		self.protocol = ProtocolAtmelSTKV2(self, device, interface)


	def open(self):
		self.transport.open()
		self.protocol.open()


	def close(self):
		self.transport.close()
		self.protocol.close()


	def read(self):
		return self.transport.read()


	def write(self, data):
		self.transport.write(data)
