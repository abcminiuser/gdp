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
        parser.add_option("-f", "--file", metavar="FILE",
                          action="store", type="string", dest="filename",
                          help="file to store the read data from the device")
        parser.add_option("", "--format",
                          action="store", type="string", dest="format",
                          help="format to save the output file as")
        parser.add_option("-o", "--offset",
                          action="store", type="int", dest="offset", default=0,
                          help="offset in the target address space to read from")
        (self.options, args) = parser.parse_args(args=args)

        try:
            file_name = self.options.filename

            if not file_name is None:
                if self.options.format:
                    file_ext = self.options.format
                else:
                    file_ext = os.path.splitext(file_name)[1][1 : ].lower()

                self.format_writer = get_gdp_format_writer(file_ext)
            else:
                self.format_writer = None
        except KeyError:
            self._parser_error("unrecognized output file type \"%s\"." % file_name)

        return args


    def can_execute(self):
        return True


    def execute(self, session):
        protocol = session.get_protocol()
        device = session.get_device()

        if not self.format_writer is None:
            file_data = self.format_writer()


        memory_type = self.options.memory_type.lower()

        device_segments = device.get_section_bounds(memory_type, memory_type)
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

            if self.format_writer is None:
                print(", ".join(["%02X" % x for x in read_data]))
            else:
               file_data.add_section(section_start, read_data)


        if not self.format_writer is None:
            try:
                file_data.save_file(self.options.filename)
            except:
                raise SessionError("Unable to save output file \"%s\"." %
                                   self.options.filename)
