'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from abc import ABCMeta, abstractmethod


class CommandParser(object):
    __metaclass__ = ABCMeta


    @abstractmethod
    def parse_arguments(self, args):
        pass


    @abstractmethod
    def execute(self, session):
        pass
