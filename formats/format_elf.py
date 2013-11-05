'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

import sys
try:
    from elftools.elf.elffile import ELFFile
    from elftools.elf.constants import SH_FLAGS
except ImportError:
    print("The PyELFTools library is not installed.")
    sys.exit(1)


from formats.format import *
from formats.formatsection import *


class FormatELF_Section(FormatSection):
    def __init__(self, instance=None):
        self.instance = instance


    def get_bounds(self):
        return (self.instance["sh_addr"],
                self.instance["sh_addr"] + self.instance["sh_size"])


    def get_data(self):
        return [ord(x) for x in self.instance.data()]


class FormatELF(Format):
    def __init__(self, filename=None):
        if filename is None:
            raise FormatError("Filename not specified.")

        self.sections = dict()

        try:
            elffile = ELFFile(open(filename, 'rb'))
        except:
            raise FormatError("Could not open ELF file \"%s\"." % filename)

        for section in elffile.iter_sections():
            if section["sh_type"] != "SHT_PROGBITS":
                continue

            if section["sh_flags"] & SH_FLAGS.SHF_ALLOC:
                new_section = FormatELF_Section(section)

                section_name = section.name[1 : ]
                self.sections[section_name] = new_section


    def get_name():
        return "ELF File Parser"


    def get_sections(self):
        return self.sections
