'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

import os.path


from devices import *
from formats import *
from tools import *


class SessionError(Exception):
    pass


class Session(object):
    def __init__(self, options):
        if options.device is None:
            raise SessionError("No device specified.")

        if options.tool is None:
            raise SessionError("No tool specified.")

        if options.interface is None:
            raise SessionError("No interface specified.")

        try:
            self.device = DeviceAtmelStudio(part=options.device)
        except DeviceError:
            raise SessionError("Unknown device \"%s\"." % options.device)

        try:
            self.tool = gdp_tools[options.tool](device=self.device,
                                                port=options.port,
                                                interface=options.interface)
        except KeyError:
            raise SessionError("Unknown tool \"%s\"." % options.tool)

        self.protocol = self.tool.get_protocol()
        self.options = options


    def open(self):
        self.tool.open()

        if not self.options.no_verify_vtarget:
            device_vtarget = self.protocol.get_vtarget()
            dev_vccrange = self.device.get_vcc_range()

            if device_vtarget is not None and \
                not dev_vccrange[0] <= device_vtarget <= dev_vccrange[1]:
                raise SessionError("Device VCC range of (%0.2fV-%0.2fV) is outside "
                                   "the measured VTARGET of %0.2fV." %
                                   (dev_vccrange[0], dev_vccrange[1], device_vtarget))

        self.protocol.set_interface_frequency(self.options.frequency)
        self.protocol.enter_session()

        if not self.options.no_verify_signature:
            expected_signature = self.device.get_signature(self.options.interface)
            read_signature = self.protocol.read_memory("signature", 0, len(expected_signature))

            if expected_signature[0 : len(read_signature)] != read_signature:
                raise SessionError("Read device signature [%s] does not match the "
                                   "expected signature [%s]." %
                                   (' '.join('0x%02X' % b for b in read_signature),
                                    ' '.join('0x%02X' % b for b in expected_signature)))


    def close(self):
        self.protocol.exit_session()
        self.tool.close()


    def process_commands(self, command_args):
        # TEST SESSION CODE
        # FIXME

        try:
            file_name = command_args[0]
            file_ext = os.path.splitext(file_name)[1][1:].lower()

            format_reader = gdp_formats[file_ext](file_name)
        except KeyError:
            raise SessionError("Unrecognized input file type \"%s\"." % file_name)

        for name, section in format_reader.get_sections().items():
            section_bounds = section.get_bounds()
            print("Section %s - 0x%08x-0x%08x" %
                  (name, section_bounds[0], section_bounds[1]))


        flash_section = format_reader.get_sections()["text"]
        flash_section_bounds = flash_section.get_bounds()
        flash_section_data   = flash_section.get_data()

        print("Erasing device memory...")
        self.protocol.erase_memory(None)

        print("Programming %d bytes of data to %s at 0x%08x-0x%08x..." %
              (len(flash_section_data), "flash",
               flash_section_bounds[0], flash_section_bounds[1]))
        self.protocol.write_memory("flash", flash_section_bounds[0], flash_section_data)

        print("Reading %d bytes of data from %s at 0x%08x-0x%08x..." %
              (len(flash_section_data), "flash",
               flash_section_bounds[0], flash_section_bounds[1]))
        print([hex(x) for x in self.protocol.read_memory("flash", flash_section_bounds[0], len(flash_section_data))])

        """
        lockbits = self.protocol.read_memory("lockbits", 0, 1)
        if not lockbits is None:
            print("Lockbits: [%s]" % ' '.join('0x%02X' % b for b in lockbits))

        fusebits = self.protocol.read_memory("fuses", 0, 3)
        if not fusebits is None:
            print("Fusebits: [%s]" % ' '.join('0x%02X' % b for b in fusebits))

        self.protocol.erase_memory(None)
        self.protocol.write_memory("flash", 2, [0xDC] * 4)
        print(self.protocol.read_memory("flash", 2, 4))
        """
