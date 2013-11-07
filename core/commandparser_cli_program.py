'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from optparse import OptionParser
import os

from core import *
from core.commandparser import *
from formats import *


class CommandParserCLIProgram(CommandParser):
    def parse_arguments(self, args):
        parser = OptionParser(description="PROGRAM command")
        parser.disable_interspersed_args()

        parser.add_option("-m", "--memory",
                          action="store", dest="memory_type", metavar="TYPE",
                          default="flash",
                          help="program target address space TYPE")
        parser.add_option("-f", "--file", metavar="FILE",
                          action="store", type="string", dest="filename",
                          help="file to program into the device")
        parser.add_option("", "--format",
                          action="store", type="string", dest="format",
                          help="format to interpret the input file as")
        parser.add_option("-o", "--offset",
                          action="store", type="int", dest="offset", default=0,
                          help="offset in the target address space to write from")
        parser.add_option("-c", "--chiperase",
                          action="store_true", dest="chiperase",
                          help="perform chip erase before programming")
        parser.add_option("-v", "--verify",
                          action="store_true", dest="verify",
                          help="verify result after programming")
        (self.options, args) = parser.parse_args(args=args)

        try:
            file_name = self.options.filename

            if self.options.format:
                file_ext = self.options.format
            else:
                file_ext = os.path.splitext(file_name)[1][1 : ].lower()

            self.format_reader = gdp_formats[file_ext](file_name)
        except KeyError:
            raise SessionError("Unrecognized input file type \"%s\"." % file_name)

        return args


    def _get_file_section(self, memory_type):
        file_sections = self.format_reader.get_sections()

        if len(file_sections) == 1:
            return file_sections[None]

        if memory_type in file_sections:
            return file_sections[section_name]

        try:
            section_name_override_map = {
                "flash" : "text",
            }

            section_name = section_name_override_map[memory_type]
            return file_sections[section_name]
        except KeyError:
            raise SessionError("Specified memory type \"%s\" was not "
                               "found in the source file." % memory_type)


    def execute(self, session):
        protocol = session.get_protocol()

        memory_type = self.options.memory_type.lower()

        section = self._get_file_section(memory_type)
        section_data  = section.get_data()
        section_start = section.get_bounds()[0]

        if self.options.chiperase is True:
            print(" - Erasing chip...")
            protocol.erase_memory(None)

        print(" - Programming memory type \"%s\"..." % memory_type)
        protocol.write_memory(memory_type,
                              self.options.offset + section_start,
                              section_data)

        if self.options.verify is True:
            print(" - Verifying written memory...")
            read_data = protocol.read_memory(memory_type,
                                             self.options.offset + section_start,
                                             len(section_data))

            for x in xrange(len(section_data)):
                if section_data[x] != read_data[x]:
                    raise SessionError("Verify failed at address 0x%08x, "
                                       "expected 0x%02x got 0x%02x." %
                                       (x, section_data[x], read_data[x]))
