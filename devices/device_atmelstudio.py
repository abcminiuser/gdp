'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from lxml import etree
from devices import *


class DeviceAtmelStudio(Device):
	def __init__(self, part=None):
		if part is None:
			raise ValueError("Device part name must be specified.")

		self.name = part
		self._parse_studio_device_file(part)


	def _find_vtarget_range(self, device_tree):
		dev_variant = device_tree.find("variants/variant[1]")
		return (float(dev_variant.get("vccmin")), float(dev_variant.get("vccmax")))


	def _parse_studio_device_file(self, name):
		device_tree = etree.parse("devices/devicefiles/%s.xml" % name)

		self.vtarget_range = self._find_vtarget_range(device_tree)
