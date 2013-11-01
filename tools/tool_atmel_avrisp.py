'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from tools import *
from transports import *
from protocols import *

from tools.tool_atmel_stk500 import ToolAtmelSTK500


class ToolAtmelAVRISP(ToolAtmelSTK500):
	def __init__(self, device, port=None, interface="isp"):
		super(ToolAtmelAVRISP, self).__init__(device, port=port, interface=interface)


	@staticmethod
	def get_name():
		return "Atmel AVRISP"


	@staticmethod
	def get_supported_interfaces():
		return ["isp"]


	def get_protocol(self):
		return self.protocol


	def open(self):
		super(ToolAtmelAVRISP, self).open()


	def close(self):
		super(ToolAtmelAVRISP, self).close()


	def read(self):
		return super(ToolAtmelAVRISP, self).read()


	def write(self, data):
		super(ToolAtmelAVRISP, self).write(data)
