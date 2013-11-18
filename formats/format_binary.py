'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from formats.format import *
from formats.format_intelhex import *


class FormatBinary(FormatIntelHex):
    @staticmethod
    def get_name():
        return "Binary File Parser"


    @staticmethod
    def get_extensions():
        return ["bin"]
