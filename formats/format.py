'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from abc import ABCMeta, abstractmethod


class FormatError(Exception):
    pass


class Format(object):
    __metaclass__ = ABCMeta


    @abstractmethod
    def get_sections(self):
        pass


    @abstractmethod
    def get_name():
        pass


    @abstractmethod
    def get_extensions():
        pass
