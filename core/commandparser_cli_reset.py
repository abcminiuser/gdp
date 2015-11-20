'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)

   Release under a MIT license; see LICENSE.txt for details.
'''

from optparse import OptionParser

from core.commandparser import *


class CommandParserCLIReset(CommandParser):
    def _parser_error(self, message):
        raise CommandParserError("RESET", message)


    def parse_arguments(self, args):
        description = "RESET command: resets the target, executing its " \
                      "program from its start address."

        parser = OptionParser(description=description, usage="")
        parser.error = self._parser_error
        parser.disable_interspersed_args()

        parser.add_option("-o", "--offset",
                          action="store", type="int", dest="offset", default=None,
                          help="offset in the target address space to start from")
        (self.options, args) = parser.parse_args(args=args)

        return args


    def can_execute(self):
        return True


    def execute(self, session):
        protocol = session.get_protocol()

        if self.options.offset is None:
            print(" - Resetting target from its default reset vector...")
        else:
            print(" - Resetting target from offset 0x%08x..." % self.options.offset)

        protocol.reset_target(self.options.offset)
