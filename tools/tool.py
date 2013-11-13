'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from abc import ABCMeta, abstractmethod


class ToolError(Exception):
    pass


class ToolSupportError(ToolError):
    def __init__(self, target, paramtype, requested, supportlist=None):
        self.message = "Unsupported %s \"%s\" for the specified %s." % \
                       (paramtype, requested, target)

        if not supportlist is None:
            self.message += "\n\nSupported %s %ss are:" % (target, paramtype)

            for s in supportlist:
                self.message += "\n  - %s" % s


class Tool(object):
    __metaclass__ = ABCMeta


    @abstractmethod
    def find_connected():
        pass


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

