'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from optparse import OptionParser

from core.commandparser import *


class CommandParserCLIErase(CommandParser):
    def _parser_error(self, message):
        raise CommandParserError("ERASE", message)


    def parse_arguments(self, args):
        parser = OptionParser(description="ERASE command")
        parser.error = self._parser_error
        parser.disable_interspersed_args()

        parser.add_option("-m", "--memory",
                          action="store", dest="memory_type", metavar="TYPE",
                          default="application",
                          help="erase target address space TYPE")
        parser.add_option("-o", "--offset",
                          action="store", type="int", dest="offset", default=0,
                          help="offset in the target address space to erase from")
        (self.options, args) = parser.parse_args(args=args)

        return args


    def execute(self, session):
        protocol = session.get_protocol()

        memory_type   = self.options.memory_type.lower()
        memory_offset = self.options.offset

        print(" - Erasing memory type \"%s\" from offset 0x%08x..." %
              (memory_type, memory_offset))
        protocol.erase_memory(memory_type, memory_offset)
