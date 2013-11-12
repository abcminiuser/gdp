'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from abc import ABCMeta, abstractmethod


class DeviceError(Exception):
    pass


class DeviceMissingInfoError(DeviceError):
    def __init__(self, paramtype, requested):
        self.message = "Device %s \"%s\" not found in the selected device." % \
                       (paramtype, requested)


class Device(object):
    __metaclass__ = ABCMeta


    @abstractmethod
    def get_name(self):
        pass


    @abstractmethod
    def get_family(self):
        pass


    @abstractmethod
    def get_architecture(self):
        pass


    @abstractmethod
    def get_vcc_range(self):
        pass


    @abstractmethod
    def get_supported_interfaces(self):
        pass


    @abstractmethod
    def get_property(self, group, param):
        pass


    @abstractmethod
    def get_signature(self, interface):
        pass


    @abstractmethod
    def get_section_bounds(self, memory_type):
        pass


    @abstractmethod
    def get_page_size(self, memory_type):
        pass
