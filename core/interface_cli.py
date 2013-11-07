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


    @staticmethod
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


    def parse(self, args):
        description = "GDP, the Generic Device Programmer."
        usage = "usage: %prog [options] COMMAND"
        parser = self._create_general_option_parser(usage, description)

        if len(args) == 1:
            print("%s\n\n%s" % (description, parser.get_usage()))
            return 0
        else:
            (options, args) = parser.parse_args()

        try:
            session = Session(options)

            session.open()

            command_list = []

            while len(args) > 0:
                current_command = args[0]

                try:
                    command_parser = InterfaceCLI.command_parsers[current_command](session)
                    command_list.append(command_parser)
                    args = command_parser.parse_arguments(args[1 : ])
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
            return 1

        return 0
