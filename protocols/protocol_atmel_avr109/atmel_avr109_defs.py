'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from protocols import *


class AtmelAVR109Defs(object):
    RESP_TERMINATOR_CHAR      = ord('\r')

    commands = {
        "ENTER_PROG_MODE"     : ord('P'),
        "SET_LED"             : ord('x'),
        "CLEAR_LED"           : ord('y'),
        "CHIP_ERASE"          : ord('e'),
        "READ_SIGNATURE"      : ord('s'),
    }


    @staticmethod
    def find(dictionary, find_value):
        friendly_name = "<UNKNOWN>"

        for key, value in dictionary.iteritems():
            if value == find_value:
                friendly_name = key
                break

        return ("%s (0x%02x)" % (friendly_name, find_value))
