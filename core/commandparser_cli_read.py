'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from optparse import OptionParser

from core import *
from core.commandparser import *
from core.commandparser_cli_program import *
from formats import *


class CommandParserCLIRead(CommandParserCLIProgram):
    def _parser_error(self, message):
        raise CommandParserError("READ", message)


    def parse_arguments(self, args):
        description = "READ command: reads the contents of an attached " \
                      "device's memory section."

        parser = OptionParser(description=description, usage="")
        parser.error = self._parser_error
        parser.disable_interspersed_args()

        parser.add_option("-m", "--memory",
                          action="store", dest="memory_type", metavar="TYPE",
                          default="flash",
                          help="read target address space TYPE")
        parser.add_option("-o", "--offset",
                          action="store", type="int", dest="offset", default=0,
                          help="offset in the target address space to read from")
        (self.options, args) = parser.parse_args(args=args)

        return args


    def can_execute(self):
        return True


    def execute(self, session):
        protocol = session.get_protocol()
        device = session.get_device()

        memory_type = self.options.memory_type.lower()

        device_segments = device.get_section_bounds(memory_type)
        if len(device_segments) == 0:
            raise SessionError("Memory type \"%s\" does not exist in the selected device." % memory_type)

        for segment_bounds in device_segments:
            section_start  = segment_bounds[0] + self.options.offset
            section_length = segment_bounds[1] - segment_bounds[0]

            memory_info_string = "type \"%s\" (%d bytes, offset 0x%08x)" % \
                                 (memory_type, section_length, section_start)


            print(" - Reading memory %s..." % memory_info_string)
            read_data = self._read_data(protocol, device,
                                        memory_type,
                                        section_start, section_length)

            print(", ".join(["%02X" % x for x in read_data]))
