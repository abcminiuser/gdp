'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from abc import ABCMeta, abstractmethod


class TransportError(Exception):
    pass


class TransportMissingParamError(TransportError):
    def __init__(self, paramtype):
        self.message = "Transport %s not specified." % paramtype


class Transport(object):
    __metaclass__ = ABCMeta


    @abstractmethod
    def find_connected():
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
