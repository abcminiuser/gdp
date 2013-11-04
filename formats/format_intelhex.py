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
    def __init__(self, format_instance=None):
        self.instance = format_instance


    def get_name(self):
        return None


    def get_address_space(self):
        return None


    def get_address_bounds(self):
        return (self.instance.minaddr(), self.instance.maxaddr())


    def get_data(self):
        return self.instance


class FormatIntelHex(Format):
    def __init__(self, filename=None):
        if filename is None:
            raise FormatError("Filename not specified.")

        file_extension = os.path.splitext(filename)[1][1:].lower()

        try:
            section_data = IntelHex()

            if file_extension == "bin":
                section_data.loadbin(filename)
            else:
                section_data.loadhex(filename)
        except:
            raise FormatError("Could not open the specified %s file." %
                              file_extension.upper())

        self.sections = [FormatIntelHex_Section(section_data)]


    def get_sections(self):
        return self.sections
