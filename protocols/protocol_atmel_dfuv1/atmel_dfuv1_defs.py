'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from protocols import *


class AtmelDFUV1Defs(object):
    DFU_DNLOAD_ALIGNMENT_LENGTH = 26
    DFU_DNLOAD_SUFFIX_LENGTH    = 16

    requests = {
        "DETATCH"             : 0,
        "DNLOAD"              : 1,
        "UPLOAD"              : 2,
        "GETSTATUS"           : 3,
        "CLRSTATUS"           : 4,
        "GETSTATE"            : 5,
        "ABORT"               : 6
    }

    states = {
        "APP_IDLE"            : 0,
        "APP_DETACH"          : 1,
        "IDLE"                : 2,
        "DNLOAD_SYNC"         : 3,
        "DNBUSY"              : 4,
        "DNLOAD_IDLE"         : 5,
        "MANIFEST_SYNC"       : 6,
        "MANIFEST"            : 7,
        "MANIFEST_WAIT_RESET" : 8,
        "UPLOAD_IDLE"         : 9,
        "ERROR"               : 10
    }

    status_codes = {
        "OK"                  : 0x00,
        "ERROR_TARGET"        : 0x01,
        "ERROR_FILE"          : 0x02,
        "ERROR_WRITE"         : 0x03,
        "ERROR_ERASE"         : 0x04,
        "ERROR_CHECK_ERASED"  : 0x05,
        "ERROR_PROG"          : 0x06,
        "ERROR_VERIFY"        : 0x07,
        "ERROR_ADDRESS"       : 0x08,
        "ERROR_NOTDONE"       : 0x09,
        "ERROR_FIRMWARE"      : 0x0a,
        "ERROR_VENDOR"        : 0x0b,
        "ERROR_USBR"          : 0x0c,
        "ERROR_POR"           : 0x0d,
        "ERROR_UNKNOWN"       : 0x0e,
        "ERROR_STALLEDPKT"    : 0x0f,
    }


    @staticmethod
    def find(dictionary, find_value):
        friendly_name = "<UNKNOWN>"

        for key, value in dictionary.iteritems():
            if value == find_value:
                friendly_name = key
                break

        return ("%s (0x%02x)" % (friendly_name, find_value))
