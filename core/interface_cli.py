'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from optparse import OptionParser, OptionGroup

from core import *
from core.commandparser import *
from core.commandparser_cli_chiperase import *
from core.commandparser_cli_program import *


class InterfaceCLI(object):
    command_parsers = {
        "chiperase" : CommandParserCLIChipErase,
        "program"   : CommandParserCLIProgram
    }


    def _parse_main_arguments(self, args):
        description = "GDP, the Generic Device Programmer.\n" \
                      "Copyright (C) 2013 Dean Camera (dean [at] fourwalledcubicle [dot] com)."
        usage = "usage: %prog [general options] COMMAND [command options]"

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
                              help="target communication interface")
        comm_group.add_option("-f", "--frequency",
                              action="store", type="int", dest="frequency",
                              default=250000,
                              help="target communication interface frequency (Hz)")

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

        if len(args) == 0:
            print("%s\n\n%s" % (description, parser.get_usage()))
        else:
            (self.options, args) = parser.parse_args(args=args)

        return args


    def _build_command_list(self, args):
        command_list = []

        while len(args) > 0:
            current_command = args[0].lower()

            try:
                command_parser = InterfaceCLI.command_parsers[current_command]()
                command_list.append(command_parser)

                args = command_parser.parse_arguments(args[1 : ])
            except KeyError:
                raise SessionError("Unknown command \"%s\"." % current_command)

        return command_list


    def parse_arguments(self, args):
        args = self._parse_main_arguments(args[1 : ])
        if len(args) == 0:
            return 0

        try:
            session = Session(self.options)

            print("GDP starting to execute commands.")

            session.open()

            for cmd in self._build_command_list(args):
                cmd.execute(session)

            session.close()

            print("GDP finished executing commands.")
            return 0
        except (FormatError, SessionError, TransportError,
                ToolError, ProtocolError) as gdp_error:
            error_type = type(gdp_error).__name__.split("Error")[0]
            error_message = gdp_error.message

            print("GDP Error (%s): %s" % (error_type, error_message))
            return 1
