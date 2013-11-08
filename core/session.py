'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

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


    def get_protocol(self):
        return self.protocol


    def get_device(self):
        return self.device


    def get_tool(self):
        return self.tool
