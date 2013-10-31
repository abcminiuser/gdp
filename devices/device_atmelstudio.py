'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from lxml import etree
from devices import *


class DeviceAtmelStudio(Device):
	device_tree = None


	def __init__(self, part=None):
		if part is None:
			raise ValueError("Device part name must be specified.")

		self.device_tree = etree.parse("devices/devicefiles/%s.xml" % part)


	def get_name(self):
		return self.device_tree.find("devices/device[1]").get("name")


	def get_vcc_range(self):
		dev_variant = self.device_tree.find("variants/variant[1]")
		return (float(dev_variant.get("vccmin")), float(dev_variant.get("vccmax")))


	def get_supported_interfaces(self):
		dev_interfaces = self.device_tree.findall("devices/device[1]/interfaces/interface")
		return [i.get("type") for i in dev_interfaces]
