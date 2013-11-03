'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from protocols import *


class AtmelDFUV1Defs(object):
	requests = {
		"DETATCH"                     : 0,
		"DNLOAD"                      : 1,
		"UPLOAD"                      : 2,
		"GETSTATUS"                   : 3,
		"CLRSTATUS"                   : 4,
		"GETSTATE"                    : 5,
		"ABORT"                       : 6
	}

	DFU_STATE_APP_IDLE                      = 0
	DFU_STATE_APP_DETACH                    = 1
	DFU_STATE_DFU_IDLE                      = 2
	DFU_STATE_DFU_DNLOAD_SYNC               = 3
	DFU_STATE_DFU_DNBUSY                    = 4
	DFU_STATE_DFU_DNLOAD_IDLE               = 5
	DFU_STATE_DFU_MANIFEST_SYNC             = 6
	DFU_STATE_DFU_MANIFEST                  = 7
	DFU_STATE_DFU_MANIFEST_WAIT_RESET       = 8
	DFU_STATE_DFU_UPLOAD_IDLE               = 9
	DFU_STATE_DFU_ERROR                     = 10


class ProtocolAtmelDFUV1(Protocol):
	def __init__(self, tool, device, interface):
		self.tool      = tool
		self.device    = device
		self.interface = interface


	def _getstate(self):
		return self.tool.read(AtmelDFUV1Defs.requests["GETSTATE"], 0, 1)[0]


	def _getstatus(self):
		return self.tool.read(AtmelDFUV1Defs.requests["GETSTATUS"], 0, 1)[0]


	def _select_64kb_bank(self, bank):
		self.tool.write(AtmelDFUV1Defs.requests["DNLOAD"], 0, [0x03, 0x00, bank])


	def get_vtarget(self):
		return None


	def set_interface_frequency(self, target_frequency):
		pass


	def enter_session(self):
		if self._getstate() != AtmelDFUV1Defs.DFU_STATE_APP_IDLE:
			self.tool.write(AtmelDFUV1Defs.requests["ABORT"], 0, None)

		self.tool.write(AtmelDFUV1Defs.requests["CLRSTATUS"], 0, None)


	def exit_session(self):
		pass


	def erase_memory(self, memory_space):
		self.tool.write(AtmelDFUV1Defs.requests["DNLOAD"], 0, [0x04, 0x00, 0xFF])


	def read_memory(self, memory_space, offset, length):
		mem_contents = []

		if memory_space == "signature":
			for x in xrange(min(length, 2)):
				packet = [0x05, 0x01]
				packet.append(0x30 + offset + x)

				self.tool.write(AtmelDFUV1Defs.requests["DNLOAD"], 0, packet)
				resp = self.tool.read(AtmelDFUV1Defs.requests["UPLOAD"], 0, 1)

				mem_contents.append(resp[0])
		elif memory_space in ["fuses", "lockbits"]:
			raise ProtocolError("Protocol does not support reading from memory \"%s\"." % memory_space)
		elif memory_space in ["flash", "eeprom"]:
			self._select_64kb_bank(offset >> 16)

			packet = [0x03]
			packet.append(0x00 if memory_space == "flash" else 0x02)
			packet.extend([offset >> 8, offset & 0xFF])
			packet.extend([(offset + length - 1) >> 8, (offset + length - 1) & 0xFF])

			self.tool.write(AtmelDFUV1Defs.requests["DNLOAD"], 0, packet)
			resp = self.tool.read(AtmelDFUV1Defs.requests["UPLOAD"], 0, length)

			mem_contents.extend(resp)
		else:
			raise NotImplementedError()

		return mem_contents


	def write_memory(self, memory_space, offset, data):
		if memory_space in ["flash", "eeprom"]:
			self._select_64kb_bank(offset >> 16)

			packet = [0x01]
			packet.append(0x00 if memory_space == "flash" else 0x01)
			packet.extend([offset >> 8, offset & 0xFF])
			packet.extend([(offset + len(data) - 1) >> 8, (offset + len(data) - 1) & 0xFF])
			packet.extend([0x00] * 26)
			packet.extend([0x00] * (offset % 32))
			packet.extend(data)
			packet.extend([0xFF] * 16)

			self.tool.write(AtmelDFUV1Defs.requests["DNLOAD"], 0, packet)
		elif memory_space in ["signature", "fuses", "lockbits"]:
			raise ProtocolError("Protocol does not support writing to memory \"%s\"." % memory_space)
		else:
			raise NotImplementedError()


	def open(self):
		pass


	def close(self):
		pass
