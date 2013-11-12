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
    def _parser_error(self, message):
        raise CommandParserError("VERIFY", message)


    def parse_arguments(self, args):
        parser = OptionParser(description="VERIFY command")
        parser.error = self._parser_error
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
            self._parser_error("no input filename specified")


        try:
            file_name = self.options.filename

            if self.options.format:
                file_ext = self.options.format
            else:
                file_ext = os.path.splitext(file_name)[1][1 : ].lower()

            self.format_reader = gdp_formats[file_ext]
        except KeyError:
            self._parser_error("unrecognized input file type \"%s\"." % file_name)

        return args


    def execute(self, session):
        protocol = session.get_protocol()
        device = session.get_device()

        memory_type = self.options.memory_type.lower()

        try:
            file_data = self.format_reader(self.options.filename)
        except:
            raise SessionError("Unable to parse input file \"%s\"." % self.options.filename)


        for section_name, section in self._get_file_sections(file_data, device, memory_type):
            section_data   = section.get_data()
            section_bounds = self._apply_arch_offsets(device, memory_type, section.get_bounds())
            section_start  = section_bounds[0] + self.options.offset

            memory_info_string = "\"%s\" type \"%s\" (%d bytes, offset 0x%08x)" % \
                                 (section_name, memory_type,
                                  len(section_data), section_start)


            print(" - Verifying memory %s..." % memory_info_string)
            read_data = self._read_data(protocol, device,
                                        memory_type,
                                        section_start, len(section_data))

            for x in xrange(len(section_data)):
                if section_data[x] != read_data[x]:
                    raise SessionError("Verify failed at address 0x%08x, "
                                       "expected 0x%02x got 0x%02x." %
                                       (x, section_data[x], read_data[x]))

