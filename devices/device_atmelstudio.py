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

        param_ints = []
        for p in param_info.get("value").split():
            if p[0 : 2] == "0x":
                param_ints.append(int(p, 16))
            else:
                param_ints.append(int(p, 10))

        return param_ints[0] if len(param_ints) == 1 else param_ints


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


    def get_page_size(self, memory_type):
        mem_segment = self.device_tree.find("devices/device[1]/address-spaces/address-space/memory-segment[@type='%s']" % memory_type.lower())
        if mem_segment is None:
            raise DeviceError("Memory segment type \"%s\" not found in the selected device." % memory_type)

        page_size_value = mem_segment.get("pagesize")

        if page_size_value is None:
            return 1
        else:
            return int(page_size_value, 16)
