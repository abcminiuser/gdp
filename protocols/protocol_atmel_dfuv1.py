'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from protocols import *


class AtmelDFUV1Defs(object):
	requests = {
		"DETATCH"             : 0,
		"DNLOAD"              : 1,
		"UPLOAD"              : 2,
		"GETSTATUS"           : 3,
		"CLRSTATUS"           : 4,
		"GETSTATE"            : 5,
		"ABORT"               : 6
	}

	states = {
		"APP_IDLE"            : 0,
		"APP_DETATCH"         : 1,
		"IDLE"                : 2,
		"IDLE"                : 2,
		"DNLOAD_SYNC"         : 3,
		"DNBUSY"              : 4,
		"DNLOAD_IDLE"         : 5,
		"MANIFEST_SYNC"       : 6,
		"MANIFEST"            : 7,
		"MANIFEST_WAIT_RESET" : 8,
		"UPLOAD_IDLE"         : 9,
		"ERROR"               : 10
	}

	status_codes = {
		"OK"                  : 0x00,
		"ERROR_TARGET"        : 0x01,
		"ERROR_FILE"          : 0x02,
		"ERROR_WRITE"         : 0x03,
		"ERROR_ERASE"         : 0x04,
		"ERROR_CHECK_ERASED"  : 0x05,
		"ERROR_PROG"          : 0x06,
		"ERROR_VERIFY"        : 0x07,
		"ERROR_ADDRESS"       : 0x08,
		"ERROR_NOTDONE"       : 0x09,
		"ERROR_FIRMWARE"      : 0x0a,
		"ERROR_VENDOR"        : 0x0b,
		"ERROR_USBR"          : 0x0c,
		"ERROR_POR"           : 0x0d,
		"ERROR_UNKNOWN"       : 0x0e,
		"ERROR_STALLEDPKT"    : 0x0f,
	}


	@staticmethod
	def find(dictionary, find_value):
		for key, value in dictionary.iteritems():
			if value == find_value:
				return key

		return None


class ProtocolAtmelDFUV1(Protocol):
	def __init__(self, tool, device, interface):
		self.tool      = tool
		self.device    = device
		self.interface = interface


	def _abort(self):
		self.tool.write(AtmelDFUV1Defs.requests["ABORT"], None)


	def _getstate(self):
		return self.tool.read(AtmelDFUV1Defs.requests["GETSTATE"], 1)[0]


	def _clearstatus(self):
		self.tool.write(AtmelDFUV1Defs.requests["CLRSTATUS"], None)


	def _getstatus(self):
		return self.tool.read(AtmelDFUV1Defs.requests["GETSTATUS"], 6)[0]


	def _download(self, command):
		self.tool.write(AtmelDFUV1Defs.requests["DNLOAD"], command)

		status = self._getstatus()
		if status != AtmelDFUV1Defs.status_codes["OK"]:
			raise ProtocolError("DFU write request failed, error code %s." %
			                    AtmelDFUV1Defs.find(AtmelDFUV1Defs.status_codes, status))


	def _upload(self, command, read_length):
		self.tool.write(AtmelDFUV1Defs.requests["DNLOAD"], command)

		status = self._getstatus()
		if status != AtmelDFUV1Defs.status_codes["OK"]:
			raise ProtocolError("DFU read request failed, error code %s." %
			                    AtmelDFUV1Defs.find(AtmelDFUV1Defs.status_codes, status))

		return self.tool.read(AtmelDFUV1Defs.requests["UPLOAD"], read_length)


	def _select_64kb_bank(self, bank):
		self._download([0x03, 0x00, bank])


	def get_vtarget(self):
		return None


	def set_interface_frequency(self, target_frequency):
		pass


	def enter_session(self):
		if self._getstate() != AtmelDFUV1Defs.states["IDLE"]:
			self._abort()

		self._clearstatus()


	def exit_session(self):
		pass


	def erase_memory(self, memory_space):
		self._download([0x04, 0x00, 0xFF])


	def read_memory(self, memory_space, offset, length):
		mem_contents = []

		if memory_space == "signature":
			sig_byte_addresses = [0x31, 0x60, 0x61]

			for x in xrange(min(length, 3)):
				packet = [0x05, 0x01]
				packet.append(sig_byte_addresses[offset + x])

				resp = self._upload(packet, 1)
				mem_contents.append(resp[0])
		elif memory_space in ["fuses", "lockbits"]:
			raise ProtocolError("Protocol does not support reading from memory \"%s\"." % memory_space)
		elif memory_space in ["flash", "eeprom"]:
			self._select_64kb_bank(offset >> 16)

			packet = [0x03]
			packet.append(0x00 if memory_space == "flash" else 0x02)
			packet.extend([offset >> 8, offset & 0xFF])
			packet.extend([(offset + length - 1) >> 8, (offset + length - 1) & 0xFF])

			resp = self._upload(packet, length)
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

			self._download(packet)
		elif memory_space in ["signature", "fuses", "lockbits"]:
			raise ProtocolError("Protocol does not support writing to memory \"%s\"." % memory_space)
		else:
			raise NotImplementedError()


	def open(self):
		pass


	def close(self):
		pass
