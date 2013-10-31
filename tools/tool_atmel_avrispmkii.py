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

		if not interface in device.get_supported_interfaces():
			raise LookupError("Unsupported interface for the specified device.")
		elif not interface in self.get_supported_interfaces():
			raise LookupError("Unsupported interface for the specified tool.")
		else:
			self.interface = interface

		self.protocol = ProtocolAtmelSTKV2(self, device, interface)


	def get_name(self):
		return "Atmel AVRISP-MKII"


	def get_supported_interfaces(self):
		return ["isp", "pdi", "tpi"]


	def open(self, target_frequency):
		self.transport.open()
		self.protocol.open(target_frequency)


	def close(self):
		self.transport.close()
		self.protocol.close()


	def read(self):
		return self.transport.read()


	def write(self, data):
		self.transport.write(data)
