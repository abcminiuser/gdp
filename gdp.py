#!/usr/bin/env python

'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

import sys
from optparse import OptionParser, OptionGroup

from core import *


def _create_option_parser(usage, description):
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


def main():
    description = "GDP, the Generic Device Programmer."
    usage = "usage: %prog [options] COMMAND"
    parser = _create_option_parser(usage, description)
    (options, args) = parser.parse_args()

    if len(sys.argv) == 1:
        print("%s\n\n%s" % (description, parser.get_usage()))
        sys.exit(0)

    try:
        session = Session(options)

        session.open()
        session.process_commands(args)
        session.close()
    except (FormatError, SessionError, TransportError,
            ToolError, ProtocolError) as gdp_error:
        error_type = type(gdp_error).__name__.split("Error")[0]
        error_message = gdp_error.message

        print("GDP Error (%s): %s" % (error_type, error_message))
        sys.exit(1)


if __name__ == "__main__":
    main()
