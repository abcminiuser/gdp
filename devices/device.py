'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from abc import ABCMeta, abstractmethod


class DeviceError(Exception):
    pass


class Device(object):
    __metaclass__ = ABCMeta


    @abstractmethod
    def get_name(self):
        pass


    @abstractmethod
    def get_vcc_range(self):
        pass


    @abstractmethod
    def get_supported_interfaces(self):
        pass


    @abstractmethod
    def get_param(self, group, param):
        pass


    @abstractmethod
    def get_signature(self, interface):
        pass
