'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from protocols.protocol import *

class ProtocolAtmelV2(Protocol):
	transport = None


	def __init__(self, transport):
		self.transport = transport


	def init(self):
		self.transport.write(2, [0x01], 100)
		rsp = self.transport.read(2, 64, 100)
		print(''.join([chr(x) for x in rsp]))
