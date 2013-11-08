'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from optparse import OptionParser
import os

from core import *
from core.commandparser import *
from core.commandparser_cli_program import *
from formats import *


class CommandParserCLIVerify(CommandParserCLIProgram):
    def parse_arguments(self, args):
        parser = OptionParser(description="VERIFY command")
        parser.disable_interspersed_args()

        parser.add_option("-m", "--memory",
                          action="store", dest="memory_type", metavar="TYPE",
                          default="flash",
                          help="verify target address space TYPE")
        parser.add_option("-f", "--file", metavar="FILE",
                          action="store", type="string", dest="filename",
                          help="file to verify against the device")
        parser.add_option("", "--format",
                          action="store", type="string", dest="format",
                          help="format to interpret the input file as")
        parser.add_option("-o", "--offset",
                          action="store", type="int", dest="offset", default=0,
                          help="offset in the target address space to read from")
        (self.options, args) = parser.parse_args(args=args)


        if self.options.filename is None:
            raise SessionError("No filename specified for VERIFY command.")


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


    def execute(self, session):
        protocol = session.get_protocol()
        device = session.get_device()

        memory_type = self.options.memory_type.lower()

        section = self._get_file_section(memory_type)
        section_data  = section.get_data()
        section_start = section.get_bounds()[0] + self.options.offset

        print(" - Verifying memory type \"%s\" (%d bytes, offset %d)..." %
              (memory_type, len(section_data), self.options.offset))

        read_data = self._read_data(protocol, device,
                                    memory_type,
                                    section_start, len(section_data))

        for x in xrange(len(section_data)):
            if section_data[x] != read_data[x]:
                raise SessionError("Verify failed at address 0x%08x, "
                                   "expected 0x%02x got 0x%02x." %
                                   (x, section_data[x], read_data[x]))
