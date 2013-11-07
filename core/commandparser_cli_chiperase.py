'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from core.commandparser import *


class CommandParserCLIChipErase(CommandParser):
    def __init__(self, session):
        self.session = session


    def parse_arguments(self, args):
        return args


    def execute(self):
        protocol = self.session.get_protocol()

        print(" - Erasing chip...")
        protocol.erase_memory(None)
