'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from abc import ABCMeta, abstractmethod


class CommandParserError(Exception):
    def __init__(self, command, reason):
        self.message = "%s command invalid: %s" % (command, reason)


class CommandParser(object):
    __metaclass__ = ABCMeta


    @abstractmethod
    def parse_arguments(self, args):
        pass


    @abstractmethod
    def can_execute(self):
        pass


    @abstractmethod
    def execute(self, session):
        pass
