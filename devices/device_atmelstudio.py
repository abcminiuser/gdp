'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

import lxml
from devices.device import *

class DeviceAtmelStudio(Device):
	def __init__(self, part=None):
		if part is None:
			raise ValueError("Device part name must be specified.")

		self._parse_studio_device_file(part)


	def _parse_studio_device_file(self, name):
		pass
