'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from optparse import OptionParser

from core.commandparser import *


class CommandParserCLIChipErase(CommandParser):
    def _parser_error(self, message):
        raise CommandParserError("CHIPERASE", message)


    def parse_arguments(self, args):
        description = "CHIPERASE command: erases all memory spaces of an " \
                      "attached device."

        parser = OptionParser(description=description, usage="")
        parser.error = self._parser_error
        parser.disable_interspersed_args()

        (self.options, args) = parser.parse_args(args=args)

        return args


    def can_execute(self):
        return True


    def execute(self, session):
        protocol = session.get_protocol()

        print(" - Erasing chip...")
        protocol.erase_memory(None, 0)
