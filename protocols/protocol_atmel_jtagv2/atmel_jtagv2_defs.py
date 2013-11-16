'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from protocols import *


class AtmelJTAGV2Defs(object):
    commands = {
        "SIGN_OFF"             : 0x00,
        "SIGN_ON"              : 0x01
    }


    @staticmethod
    def find(dictionary, find_value):
        friendly_name = "<UNKNOWN>"

        for key, value in dictionary.iteritems():
            if value == find_value:
                friendly_name = key
                break

        return ("%s (0x%02x)" % (friendly_name, find_value))

