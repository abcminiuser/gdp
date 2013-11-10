'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from abc import ABCMeta, abstractmethod


class ToolError(Exception):
    pass


class Tool(object):
    __metaclass__ = ABCMeta


    @abstractmethod
    def get_name():
        pass


    @abstractmethod
    def get_supported_interfaces():
        pass


    @abstractmethod
    def open(self):
        pass


    @abstractmethod
    def close(self):
        pass


    @abstractmethod
    def read(self):
        pass


    @abstractmethod
    def write(self, data):
        pass

