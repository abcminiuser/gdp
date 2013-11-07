#!/usr/bin/env python

'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

import sys
from optparse import OptionParser, OptionGroup

from core import *


class CommandParser_ChipErase(object):
    def __init__(self, session):
        self.session = session


    def parse_arguments(self, args):
        return args


    def execute(self):
        protocol = self.session.get_protocol()

        print(" - Erasing chip...")
        protocol.erase_memory(None)


class CommandParser_Program(object):
    def __init__(self, session):
        self.session = session


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
        (self.options, args) = parser.parse_args(args)

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


    def execute(self):
        protocol = self.session.get_protocol()


        if self.options.chiperase:
            print(" - Erasing chip...")
            protocol.erase_memory(None)

        section_name_map = {
            "flash"  : "text",
            "eeprom" : "eeprom",
        }

        memory_type = self.options.memory_type.lower()
        section_name = section_name_map[memory_type]
        section = self.format_reader.get_sections()[section_name]

        print(" - Programming memory type \"%s\"..." % memory_type)
        protocol.write_memory(memory_type,
                              self.options.offset + section.get_bounds()[0],
                              section.get_data())


def _create_general_option_parser(usage, description):
    parser = OptionParser(usage=usage, description=description)
    parser.disable_interspersed_args()

    comm_group = OptionGroup(parser,
                             "Communication Settings",
                             "Basic device/tool settings.")
    comm_group.add_option("-d", "--device",
                          action="store", type="string", dest="device",
                          help="target device selection")
    comm_group.add_option("-t", "--tool",
                          action="store", type="string", dest="tool",
                          help="target device selection")
    comm_group.add_option("-p", "--port",
                          action="store", type="string", dest="port",
                          help="communication port (for serial tools)")
    comm_group.add_option("-i", "--interface",
                          action="store", type="string", dest="interface",
                          help="communication interface to use to the target")
    comm_group.add_option("-f", "--frequency",
                          action="store", type="int", dest="frequency", default=250000,
                          help="communication interface frequency to use to the target")

    override_group = OptionGroup(parser,
                                 "Sanity Check Overrides",
                                 "[Here be dragons.]")
    override_group.add_option("", "--no-vtarget",
                              action="store_true", dest="no_verify_vtarget",
                              help="disable VCC range validity check of the target")
    override_group.add_option("", "--no-signature",
                              action="store_true", dest="no_verify_signature",
                              help="disable signature validity check of the target")

    parser.add_option_group(comm_group)
    parser.add_option_group(override_group)

    return parser


def main():
    description = "GDP, the Generic Device Programmer."
    usage = "usage: %prog [options] COMMAND"
    parser = _create_general_option_parser(usage, description)
    (options, args) = parser.parse_args()

    if len(sys.argv) == 1:
        print("%s\n\n%s" % (description, parser.get_usage()))
        sys.exit(0)

    try:
        session = Session(options)

        session.open()

        command_list = []

        cmd_parsers = {
            "chiperase" : CommandParser_ChipErase,
            "program"   : CommandParser_Program
        }

        while len(args) > 0:
            current_command = args[0]

            try:
                command_parser_inst = cmd_parsers[current_command](session)
                command_list.append(command_parser_inst)
                args = command_parser_inst.parse_arguments(args[1 : ])
            except KeyError:
                raise SessionError("Unknown command \"%s\"." % current_command)

        for cmd in command_list:
            cmd.execute()

        session.close()

        print("Finished executing commands.")
    except (FormatError, SessionError, TransportError,
            ToolError, ProtocolError) as gdp_error:
        error_type = type(gdp_error).__name__.split("Error")[0]
        error_message = gdp_error.message

        print("GDP Error (%s): %s" % (error_type, error_message))
        sys.exit(1)


if __name__ == "__main__":
    main()
