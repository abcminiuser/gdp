'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)

   Release under a MIT license; see LICENSE.txt for details.
'''

from abc import ABCMeta, abstractmethod


class TransportError(Exception):
    pass


class TransportMissingParamError(TransportError):
    def __init__(self, paramtype):
        self.message = "Transport %s not specified." % paramtype


class TransportMultipleMatchError(TransportError):
    def __init__(self, matchlist=None):
        self.message = "Multiple identical tools are connected, please " \
                       "specify the tool serial number."

        if not matchlist is None:
            self.message += "\n\nMatching connected tool serial numbers:"

            for t in matchlist:
                self.message += "\n  - %s" % t


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
