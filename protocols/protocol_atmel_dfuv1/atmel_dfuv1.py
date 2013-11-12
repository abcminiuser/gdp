'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from core import *
from protocols import *
from protocols.protocol_atmel_dfuv1.atmel_dfuv1_defs import *


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
        try:
            self.tool.write(AtmelDFUV1Defs.requests["DNLOAD"], command)
        except:
            pass

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
        self._abort()
        self._clearstatus()


    def exit_session(self):
        pass


    def erase_memory(self, memory_space, offset):
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
            for (address, chunklen) in Util.chunk_address(length, 512, offset):
                self._select_64kb_bank(address >> 16)

                packet = [0x03]
                packet.append(0x00 if memory_space == "flash" else 0x02)
                packet.extend(Util.array_encode(address, 2, "big"))
                packet.extend(Util.array_encode((address + chunklen - 1), 2, "big"))

                resp = self._upload(packet, chunklen)
                mem_contents.extend(resp)
        else:
            raise NotImplementedError()

        return mem_contents


    def write_memory(self, memory_space, offset, data):
        if memory_space in ["flash", "eeprom"]:
            for (address, chunk) in Util.chunk_data(data, 512, offset):
                self._select_64kb_bank(address >> 16)

                packet = [0x01]
                packet.append(0x00 if memory_space == "flash" else 0x01)
                packet.extend(Util.array_encode(address, 2, "big"))
                packet.extend(Util.array_encode((address + len(chunk) - 1), 2, "big"))
                packet.extend([0x00] * AtmelDFUV1Defs.DFU_DNLOAD_ALIGNMENT_LENGTH)
                packet.extend([0x00] * (address % 32))
                packet.extend(chunk)
                packet.extend([0xFF] * AtmelDFUV1Defs.DFU_DNLOAD_SUFFIX_LENGTH)

                self._download(packet)
        elif memory_space in ["signature", "fuses", "lockbits"]:
            raise ProtocolError("Protocol does not support writing to memory \"%s\"." % memory_space)
        else:
            raise NotImplementedError()


    def open(self):
        pass


    def close(self):
        pass
