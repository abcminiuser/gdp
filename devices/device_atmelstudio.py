'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

import xml.etree.ElementTree as ET

from devices import *


class DeviceAtmelStudio(Device):
    def __init__(self, part=None):
        if part is None:
            raise DeviceError("Device part name must be specified.")

        try:
            self.device_tree = ET.parse("devicefiles/%s.xml" % part)
        except IOError:
            raise DeviceError("Could not open the specified part file.")


    def get_name(self):
        return self.device_tree.find("devices/device[1]").get("name")


    def get_vcc_range(self):
        dev_variant = self.device_tree.find("variants/variant[1]")
        return (float(dev_variant.get("vccmin")), float(dev_variant.get("vccmax")))


    def get_supported_interfaces(self):
        dev_interfaces = self.device_tree.findall("devices/device[1]/interfaces/interface")
        return [i.get("name").lower() for i in dev_interfaces]


    def get_param(self, group, param):
        param_group = self.device_tree.find("devices/device[1]/property-groups/property-group[@name='%s']" % group.upper())
        if param_group is None:
            raise DeviceError("Property group \"%s\" not found in the selected device." % group)

        param_info = param_group.find("property[@name='%s']" % param)
        if param_info is None:
            raise DeviceError("Device group \"%s\" parameter \"%s\" not found in the selected device." % (group, param))

        param_value = param_info.get("value")

        if param_value[0 : 2] == "0x":
            return int(param_value, 16)
        else:
            return int(param_value, 10)


    def get_signature(self, interface):
        if interface == "jtag":
            return self.get_param("signatures", "JTAGID")
        else:
            dev_signature = 0

            try:
                dev_signature = []
                while True:
                    dev_signature.append(self.get_param("signatures",
                                         "SIGNATURE%d" % len(dev_signature)))
            finally:
                return dev_signature
