'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from protocols import *


class ProtocolAtmelJTAGV2(Protocol):
	tool      = None
	device    = None
	interface = None


	def __init__(self, tool, device, interface):
		self.tool      = tool
		self.device    = device
		self.interface = interface


	def _trancieve(self, packet_out):
		raise NotImplementedError()


	def _protocol_sign_off(self):
		raise NotImplementedError()


	def _protocol_sign_on(self):
		raise NotImplementedError()


	def _protocol_reset_protection(self):
		raise NotImplementedError()


	def _protocol_set_reset_polarity(self, idle_level):
		raise NotImplementedError()


	def _protocol_verify_vtarget(self):
		raise NotImplementedError()


	def open(self, target_frequency):
		raise NotImplementedError()


	def close(self):
		raise NotImplementedError()
