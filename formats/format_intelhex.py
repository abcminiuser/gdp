'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

import os
import sys
try:
	from intelhex import IntelHex
except ImportError:
    print("The IntelHex library is not installed.")
    sys.exit(1)


from formats.format import *
from formats.formatsection import *


class FormatIntelHex_Section(FormatSection):
    def __init__(self, instance=None):
        self.instance = instance


    def get_name(self):
        return None


    def get_bounds(self):
        return (self.instance.minaddr(), self.instance.maxaddr())


    def get_data(self):
        return self.instance.tobinarray()


class FormatIntelHex(Format):
    def __init__(self, filename=None):
        if filename is None:
            raise FormatError("Filename not specified.")

        self.sections = dict()

        file_extension = os.path.splitext(filename)[1][1:].lower()

        try:
            hexfile = IntelHex()

            if file_extension == "bin":
                hexfile.loadbin(filename)
            else:
                hexfile.loadhex(filename)
        except:
            raise FormatError("Could not open %s file \"%s\"." %
                              (file_extension.upper(), filename))

        self.sections[None] = FormatIntelHex_Section(hexfile)


    def get_name():
        return "Intel HEX File Parser"


    def get_sections(self):
        return self.sections
