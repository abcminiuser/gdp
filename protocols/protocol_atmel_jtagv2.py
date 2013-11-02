'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from protocols import *


class AtmelJTAGV2Defs(object):
	CMD_SIGN_OFF                = 0x00
	CMD_SIGN_ON                 = 0x01

	STATUS_CMD_OK               = 0x00


class ProtocolAtmelJTAGV2(Protocol):
	def __init__(self, tool, device, interface):
		self.tool      = tool
		self.device    = device
		self.interface = interface


	def _trancieve(self, packet_out):
		self.tool.write(packet_out)
		packet_in = self.tool.read()

		if packet_in is None:
			raise ValueError("No response received from tool.")

		if packet_in[0] != packet_out[0]:
			raise ValueError("Invalid response received from tool.")

		if packet_in[1] != AtmelJTAGV2Defs.V2_STATUS_CMD_OK:
			raise ValueError("Command failed with status %d." % packet_in[1])

		return packet_in


	def _sign_on(self):
		self._trancieve([AtmelJTAGV2Defs.CMD_SIGN_ON])


	def _sign_off(self):
		self._trancieve([AtmelJTAGV2Defs.CMD_SIGN_OFF])


	def get_vtarget(self):
		raise NotImplementedError


	def set_interface_frequency(self, target_frequency):
		raise NotImplementedError


	def enter_session(self):
		raise NotImplementedError


	def exit_session(self):
		raise NotImplementedError


	def erase_memory(self, memory_space):
		raise NotImplementedError()


	def read_memory(self, memory_space, offset, length):
		raise NotImplementedError()


	def write_memory(self, memory_space, offset, data):
		raise NotImplementedError()


	def open(self):
		self._sign_on()
		raise NotImplementedError()


	def close(self):
		self._sign_off()
		raise NotImplementedError()
