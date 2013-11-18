'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from formats.format import *
from formats.format_intelhex import *


class FormatBinary(FormatIntelHex):
    def __init__(self):
        self.sections = dict()


    def load_file(self, filename=None):
        super(FormatBinary, self).load_file(filename)


    def get_sections(self):
        return super(FormatBinary, self).get_sections()


    @staticmethod
    def get_name():
        return "Binary File Parser"


    @staticmethod
    def get_extensions():
        return ["bin"]
