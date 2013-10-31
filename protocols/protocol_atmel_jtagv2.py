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


	def get_vtarget(self):
		raise NotImplementedError


	def set_interface_frequency(self, target_frequency):
		raise NotImplementedError


	def enter_session(self):
		raise NotImplementedError


	def exit_session(self):
		raise NotImplementedError


	def open(self, target_frequency):
		raise NotImplementedError()


	def close(self):
		raise NotImplementedError()
