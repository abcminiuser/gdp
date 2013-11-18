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


class FormatReader(Format):
    __metaclass__ = ABCMeta


    @abstractmethod
    def load_file(self, filename):
        pass


class FormatWriter(Format):
    __metaclass__ = ABCMeta


    @abstractmethod
    def add_section(self, name, data):
        pass


    @abstractmethod
    def save_file(self, filename):
        pass
