'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from core.commandparser import *


class CommandParserCLIChipErase(CommandParser):
    def parse_arguments(self, args):
        return args


    def execute(self, session):
        protocol = session.get_protocol()

        print(" - Erasing chip...")
        protocol.erase_memory(None, 0)
