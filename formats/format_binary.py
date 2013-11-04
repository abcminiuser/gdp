'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from formats.format import *
from formats.format_intelhex import *


class FormatBinary(FormatIntelHex):
    def __init__(self, filename=None):
        super(FormatBinary, self).__init__(filename)


    def get_sections(self):
        return super(FormatBinary, self).get_sections()


    def get_name():
        return "Binary File Parser"
