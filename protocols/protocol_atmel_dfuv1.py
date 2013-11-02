'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from protocols import *


class AtmelDFUV1Defs(object):
	DFU_REQ_DETATCH                         = 0
	DFU_REQ_DNLOAD                          = 1
	DFU_REQ_UPLOAD                          = 2
	DFU_REQ_GETSTATUS                       = 3
	DFU_REQ_CLRSTATUS                       = 4
	DFU_REQ_GETSTATE                        = 5
	DFU_REQ_ABORT                           = 6

	DFU_STATE_APP_IDLE                      = 0,
	DFU_STATE_APP_DETACH                    = 1,
	DFU_STATE_DFU_IDLE                      = 2,
	DFU_STATE_DFU_DNLOAD_SYNC               = 3,
	DFU_STATE_DFU_DNBUSY                    = 4,
	DFU_STATE_DFU_DNLOAD_IDLE               = 5,
	DFU_STATE_DFU_MANIFEST_SYNC             = 6,
	DFU_STATE_DFU_MANIFEST                  = 7,
	DFU_STATE_DFU_MANIFEST_WAIT_RESET       = 8,
	DFU_STATE_DFU_UPLOAD_IDLE               = 9,
	DFU_STATE_DFU_ERROR                     = 10


class ProtocolAtmelDFUV1(Protocol):
	def __init__(self, tool, device, interface):
		self.tool      = tool
		self.device    = device
		self.interface = interface


	def _getstate(self):
		return self.tool.read(AtmelDFUV1Defs.DFU_REQ_GETSTATE, 0, 1)[0]


	def _getstatus(self):
		return self.tool.read(AtmelDFUV1Defs.DFU_REQ_GETSTATUS, 0, 1)[0]


	def get_vtarget(self):
		return None


	def set_interface_frequency(self, target_frequency):
		pass


	def enter_session(self):
		if self._getstate() != AtmelDFUV1Defs.DFU_STATE_APP_IDLE:
			self.tool.write(AtmelDFUV1Defs.DFU_REQ_ABORT, 0, None)

		self.tool.write(AtmelDFUV1Defs.DFU_REQ_CLRSTATUS, 0, None)


	def exit_session(self):
		pass


	def erase_memory(self, memory_space):
		self.tool.write(AtmelDFUV1Defs.DFU_REQ_DNLOAD, 0, [0x04, 0x00, 0xFF])


	def read_memory(self, memory_space, offset, length):
		mem_contents = []

		if memory_space == "signature":
			for x in xrange(min(length, 2)):
				packet = [0x05, 0x01]
				packet.append(0x30 + offset + x)

				self.tool.write(AtmelDFUV1Defs.DFU_REQ_DNLOAD, 0, packet)
				resp = self.tool.read(AtmelDFUV1Defs.DFU_REQ_UPLOAD, 0, 1)

				mem_contents.append(resp[0])
		elif memory_space in ["fuses", "lockbits"]:
			return None
		elif memory_space in ["flash", "eeprom"]:
			packet = [0x03]
			packet.append(0x00 if memory_space == "flash" else 0x02)
			packet.extend([offset & 0xFF, offset >> 8])
			packet.extend([(offset + length) & 0xFF, (offset + length) >> 8])

			self.tool.write(AtmelDFUV1Defs.DFU_REQ_DNLOAD, 0, packet)
			resp = self.tool.read(AtmelDFUV1Defs.DFU_REQ_UPLOAD, 0, length)

			mem_contents.extend(resp)
		else:
			raise NotImplementedError()


		return mem_contents

	def write_memory(self, memory_space, offset, data):
		if memory_space in ["flash", "eeprom"]:
			packet = [0x01]
			packet.append(0x00 if memory_space == "flash" else 0x01)
			packet.extend([offset & 0xFF, offset >> 8])
			packet.extend([(offset + len(data)) & 0xFF, (offset + len(data)) >> 8])
			self.tool.write(AtmelDFUV1Defs.DFU_REQ_DNLOAD, 0, packet)

			print packet
			print self._getstate()

			packet = []
			packet.extend([0x00] * 26)
			packet.extend([0x00] * (offset % 32))
			packet.extend(data)
			packet.extend([0x00] * 16)
			self.tool.write(AtmelDFUV1Defs.DFU_REQ_DNLOAD, 0, packet)
		elif memory_space in ["signature", "fuses", "lockbits"]:
			pass
		else:
			raise NotImplementedError()


	def open(self):
		pass


	def close(self):
		pass
