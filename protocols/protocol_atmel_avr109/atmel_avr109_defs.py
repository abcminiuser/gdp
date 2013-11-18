'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from protocols import *


class AtmelAVR109Defs(object):
    RESP_TERMINATOR_CHAR         = ord('\r')

    commands = {
        "ENTER_PROG_MODE"        : ord('P'),
        "LEAVE_PROG_MODE"        : ord('L'),
        "SET_LED"                : ord('x'),
        "CLEAR_LED"              : ord('y'),
        "CHIP_ERASE"             : ord('e'),
        "READ_SIGNATURE"         : ord('s'),
        "ADDRESS_AUTO_INCREMENT" : ord('a'),
        "CHECK_BLOCK_SUPPORT"    : ord('b'),
        "READ_FLASH_WORD"        : ord('R'),
        "READ_EEPROM_BYTE"       : ord('d'),
        "WRITE_FLASH_BYTE_LOW"   : ord('c'),
        "WRITE_FLASH_BYTE_HIGH"  : ord('C'),
        "WRITE_EEPROM_BYTE"      : ord('D'),
        "READ_BLOCK"             : ord('g'),
        "WRITE_BLOCK"            : ord('B'),
        "PAGE_WRITE"             : ord('m'),
        "SET_ADDRESS"            : ord('A'),
        "READ_LOCKBITS"          : ord('r'),
        "WRITE_LOCKBITS"         : ord('l'),
        "READ_FUSES_LOW"         : ord('F'),
        "READ_FUSES_HIGH"        : ord('F'),
        "READ_FUSES_EXTENDED"    : ord('Q'),
        "EXIT_BOOTLOADER"        : ord('E')
    }


    @staticmethod
    def find(dictionary, find_value):
        friendly_name = "<UNKNOWN>"

        for key, value in dictionary.iteritems():
            if value == find_value:
                friendly_name = key
                break

        return ("%s (0x%02x)" % (friendly_name, find_value))
