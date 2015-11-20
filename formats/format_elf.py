'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)

   Release under a MIT license; see LICENSE.txt for details.
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
    def __init__(self, instance=None, segment_offset=0):
        self.instance = instance
        self.lma  = segment_offset
        self.size = self.instance["sh_size"]


    def get_bounds(self):
        return (self.lma, self.lma + self.size)


    def get_data(self):
        return [ord(x) for x in self.instance.data()]


class FormatELF(FormatReader):
    def __init__(self):
        self.sections = dict()


    def load_file(self, filename=None):
        if filename is None:
            raise FormatError("Filename not specified.")

        try:
            elffile = ELFFile(open(filename, 'rb'))
        except:
            raise FormatError("Could not open ELF file \"%s\"." % filename)

        section_lma_map = dict()

        for section in elffile.iter_sections():
            if section["sh_type"] != "SHT_PROGBITS":
                continue

            if section["sh_flags"] & SH_FLAGS.SHF_ALLOC:
                for segment in elffile.iter_segments():
                    if segment.section_in_segment(section):
                        if not segment in section_lma_map:
                            section_lma_map[segment] = segment["p_paddr"]

                        segment_offset = section_lma_map[segment]

                        section_lma_map[segment] += section["sh_size"]
                        break

                new_section = FormatELF_Section(section, segment_offset)

                section_name = section.name[1 : ]
                self.sections[section_name] = new_section


        if len(self.sections) == 0:
            raise FormatError("ELF file \"%s\" contains no data." % filename)


    def get_sections(self):
        return self.sections


    @staticmethod
    def get_name():
        return "ELF File Parser"


    @staticmethod
    def get_extensions():
        return ["elf"]
