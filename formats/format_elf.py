'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

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
        return (self.instance["sh_addr"],
                self.instance["sh_addr"] + self.instance["sh_size"])


    def get_data(self):
        return [ord(x) for x in self.instance.data()]


class FormatELF(Format):
    SHF_ALLOC = 0x02


    def __init__(self, filename=None):
        if filename is None:
            raise FormatError("Filename not specified.")

        self.sections = dict()

        try:
            elffile = ELFFile(open(filename, 'rb'))

            for section in elffile.iter_sections():
                if section["sh_type"] != "SHT_PROGBITS":
                    continue

                if section["sh_flags"] & FormatELF.SHF_ALLOC:
                    new_section = FormatELF_Section(section)
                    self.sections[new_section.get_name()] = new_section
        except:
            raise FormatError("Could not open ELF file \"%s\"." % filename)


    def get_name():
        return "ELF File Parser"


    def get_sections(self):
        return self.sections
