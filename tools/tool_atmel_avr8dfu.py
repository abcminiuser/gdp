'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from tools import *
from transports import *
from protocols import *


class ToolAtmelAVR8DFU(Tool):
	device_to_pid = {
		"at90usb1287" : 0x2FFB,
		"at90usb647"  : 0x2FF9,
		"at90usb1286" : 0x2FFB,
		"at90usb646"  : 0x2FF9,
		"atmega32U4"  : 0x2FF4,
		"atmega16U4"  : 0x2FF3,
		"atmega32U2"  : 0x2FF0,
		"atmega16U2"  : 0x2FEF,
		"at90usb162"  : 0x2FFA,
		"atmega8U2"	  : 0x2FEE,
		"at90usb82"	  : 0x2FF7,
		}


	def __init__(self, device, port=None, interface="dfu"):
		try:
			pid = ToolAtmelAVR8DFU.device_to_pid[device.get_name().lower()]
		except KeyError:
			raise LookupError("Unsupported device for the specified tool.")

		if port is None:
			self.transport = TransportDFUUSB(vid=0x03EB, pid=pid)
		else:
			raise LookupError("Unsupported port for the specified tool.")

		if not interface in self.get_supported_interfaces():
			raise LookupError("Unsupported interface \"%s\" for the specified tool." % interface)
		else:
			self.interface = interface

		self.protocol = ProtocolAtmelDFUV1(self, device, interface)
		self.sequence = 0x00


	@staticmethod
	def get_name():
		return "Atmel DFU Bootloader (AVR8)"


	@staticmethod
	def get_supported_interfaces():
		return ["dfu"]


	def get_protocol(self):
		return self.protocol


	def open(self):
		self.transport.open()
		self.protocol.open()


	def close(self):
		self.protocol.close()
		self.transport.close()


	def read(self, read_type, wValue, wLength):
		return self.transport.read(read_type, wValue, wLength)


	def write(self, write_type, wValue, data):
		self.transport.write(write_type, wValue, data)
