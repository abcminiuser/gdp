'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

import os
import sys
try:
	from elftools.elf.elffile import ELFFile
except ImportError:
    print("The PyELFTools library is not installed.")
    sys.exit(1)


from formats.format import *
from formats.formatsection import *


class FormatELF_Section(FormatSection):
    def __init__(self, instance=None):
        self.instance = instance


    def get_name(self):
        return self.instance.name[1 : ]


    def get_bounds(self):
        return NotImplementedError


    def get_data(self):
        return self.instance.data


class FormatELF(Format):
    def __init__(self, filename=None):
        if filename is None:
            raise FormatError("Filename not specified.")

        self.sections = []

        try:
            with open(filename, 'rb') as f:
                elffile = ELFFile(f)

                for section in elffile.iter_sections():
                    if not section.name.startswith(".debug"):
                        self.sections.append(FormatELF_Section(section))
        except:
            raise FormatError("Could not open the specified ELF file.")


    def get_sections(self):
        return self.sections
