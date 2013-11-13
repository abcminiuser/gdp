'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from optparse import OptionParser
import os

from core import *
from core.commandparser import *
from formats import *


class CommandParserCLIProgram(CommandParser):
    def _parser_error(self, message):
        raise CommandParserError("PROGRAM", message)


    def parse_arguments(self, args):
        parser = OptionParser(description="PROGRAM command")
        parser.error = self._parser_error
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
        parser.add_option("-v", "--verify",
                          action="store_true", dest="verify",
                          help="verify result after programming")
        (self.options, args) = parser.parse_args(args=args)


        if self.options.filename is None:
            self._parser_error("no input filename specified")


        try:
            file_name = self.options.filename

            if self.options.format:
                file_ext = self.options.format
            else:
                file_ext = os.path.splitext(file_name)[1][1 : ].lower()

            self.format_reader = gdp_formats[file_ext]
        except KeyError:
            self._parser_error("unrecognized input file type \"%s\"." % file_name)

        return args


    def can_execute(self):
        return True


    @staticmethod
    def _apply_arch_offsets(device, memory_type, bounds):
        if memory_type == "eeprom" and "AVR8" in device.get_architecture():
            return (bounds[0] - 0x810000, bounds[1] - 0x810000)
        else:
            return bounds


    def _get_file_sections(self, file_data, device, memory_type):
        file_sections   = file_data.get_sections()
        device_segments = device.get_section_bounds(memory_type)

        if len(device_segments) == 0:
            raise SessionError("Memory type \"%s\" does not exist in the selected device." % memory_type)

        matched_sections = []

        for section_name, section_data in file_sections.iteritems():
            section_bounds = self._apply_arch_offsets(device, memory_type, section_data.get_bounds())

            for segment_bounds in device_segments:
                if section_bounds[0] >= segment_bounds[0] and \
                   section_bounds[1] <= segment_bounds[1]:

                    if section_name is None:
                        section_name = "<Anonymous>"

                    matched_sections.append((section_name, section_data))
                    break

        return matched_sections


    def _write_data(self, protocol, device, memory_type, start, data):
        page_size   = device.get_page_size(memory_type)
        page_offset = start % page_size

        aligned_data = []

        if start % page_size != 0:
            start -= page_offset

            first_page_data = protocol.read_memory(memory_type, start, page_size)
            aligned_data.extend(first_page_data[0 : page_offset])

        aligned_data.extend(data)

        if len(aligned_data) % page_size != 0:
            last_page_offset = len(aligned_data) % page_size

            last_page_data = protocol.read_memory(memory_type,
                                                  start + len(aligned_data) - last_page_offset,
                                                  page_size)
            aligned_data.extend(last_page_data[last_page_offset : ])

        for (address, chunk) in Util.chunk_data(aligned_data, page_size, start):
            protocol.write_memory(memory_type, address, chunk)


    def _read_data(self, protocol, device, memory_type, start, length):
        page_size   = device.get_page_size(memory_type)
        page_offset = start % page_size

        aligned_data = []

        start -= page_offset

        length_aligned = length + (page_size - (length % page_size))

        for (address, chunklen) in Util.chunk_address(length_aligned, page_size, start):
            aligned_data.extend(protocol.read_memory(memory_type,
                                                     address,
                                                     page_size))

        return aligned_data[page_offset : page_offset + length]


    def execute(self, session):
        protocol = session.get_protocol()
        device = session.get_device()

        memory_type = self.options.memory_type.lower()

        try:
            file_data = self.format_reader(self.options.filename)
        except:
            raise SessionError("Unable to parse input file \"%s\"." %
                               self.options.filename)


        if self.options.chiperase is True:
            print(" - Erasing chip...")
            protocol.erase_memory(None, 0)


        for section_name, section in self._get_file_sections(file_data, device, memory_type):
            section_data   = section.get_data()
            section_bounds = self._apply_arch_offsets(device, memory_type, section.get_bounds())
            section_start  = section_bounds[0] + self.options.offset

            memory_info_string = "\"%s\" type \"%s\" (%d bytes, offset 0x%08x)" % \
                                 (section_name, memory_type,
                                  len(section_data), section_start)


            print(" - Programming memory %s..." % memory_info_string)
            self._write_data(protocol, device,
                             memory_type,
                             section_start, section_data)


            if self.options.verify is True:
                print(" - Verifying memory %s..." % memory_info_string)
                read_data = self._read_data(protocol, device,
                                            memory_type,
                                            section_start, len(section_data))

                for x in xrange(len(section_data)):
                    if section_data[x] != read_data[x]:
                        raise SessionError("Verify failed at address 0x%08x, "
                                           "expected 0x%02x got 0x%02x." %
                                           (x, section_data[x], read_data[x]))
