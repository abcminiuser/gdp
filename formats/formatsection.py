'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from abc import ABCMeta, abstractmethod

from formats.format import *


class FormatSection(object):
    __metaclass__ = ABCMeta


    @abstractmethod
    def get_bounds(self):
        pass


    @abstractmethod
    def get_data(self):
        pass
