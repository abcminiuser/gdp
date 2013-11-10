'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from protocols import *


class AtmelSTKV2Defs(object):
    commands = {
        "SIGN_ON"              : 0x01,
        "SET_PARAMETER"        : 0x02,
        "GET_PARAMETER"        : 0x03,
        "OSCCAL"               : 0x05,
        "LOAD_ADDRESS"         : 0x06,
        "FIRMWARE_UPGRADE"     : 0x07,
        "RESET_PROTECTION"     : 0x0A,
        "ENTER_PROGMODE_ISP"   : 0x10,
        "LEAVE_PROGMODE_ISP"   : 0x11,
        "CHIP_ERASE_ISP"       : 0x12,
        "PROGRAM_FLASH_ISP"    : 0x13,
        "READ_FLASH_ISP"       : 0x14,
        "PROGRAM_EEPROM_ISP"   : 0x15,
        "READ_EEPROM_ISP"      : 0x16,
        "PROGRAM_FUSE_ISP"     : 0x17,
        "READ_FUSE_ISP"        : 0x18,
        "PROGRAM_LOCK_ISP"     : 0x19,
        "READ_LOCK_ISP"        : 0x1A,
        "READ_SIGNATURE_ISP"   : 0x1B,
        "READ_OSCCAL_ISP"      : 0x1C,
        "SPI_MULTI"            : 0x1D,
        "XPROG"                : 0x50,
        "XPROG_SETMODE"        : 0x51
    }

    status_codes = {
        "CMD_OK"               : 0x00,
        "CMD_TOUT"             : 0x80,
        "RDY_BSY_TOUT"         : 0x81,
        "SET_PARAM_MISSING"    : 0x82,
        "CMD_FAILED"           : 0xC0,
        "CMD_UNKNOWN"          : 0xC9,
        "ISP_READY"            : 0x00,
        "CONN_FAIL_MOSI"       : 0x01,
        "CONN_FAIL_RST"        : 0x02,
        "CONN_FAIL_SCK"        : 0x04,
        "TGT_NOT_DETECTED"     : 0x10,
        "TGT_REVERSE_INSERTED" : 0x20
    }

    params = {
        "BUILD_NUMBER_LOW"     : 0x80,
        "BUILD_NUMBER_HIGH"    : 0x81,
        "HW_VER"               : 0x90,
        "SW_MAJOR"             : 0x91,
        "SW_MINOR"             : 0x92,
        "VTARGET"              : 0x94,
        "SCK_DURATION"         : 0x98,
        "RESET_POLARITY"       : 0x9E,
        "STATUS_TGT_CONN"      : 0xA1,
        "DISCHARGEDELAY"       : 0xA4
    }

    xprog_commands = {
        "ENTER_PROGMODE"       : 0x01,
        "LEAVE_PROGMODE"       : 0x02,
        "ERASE"                : 0x03,
        "WRITE_MEMORY"         : 0x04,
        "READ_MEMORY"          : 0x05,
        "CRC"                  : 0x06,
        "SET_PARAMETER"        : 0x07
    }

    xprog_status_codes = {
        "OK"                   : 0x00,
        "FAILED"               : 0x01,
        "COLLISION"            : 0x02,
        "TIMEOUT"              : 0x03
    }

    xprog_params = {
        "NVMBASE"              : 0x01,
        "EEPPAGESIZE"          : 0x02,
        "NVMCMD_REG"           : 0x03,
        "NVMCSR_REG"           : 0x04,
        "UNKNOWN_1"            : 0x05
    }

    xprog_memory_types = {
        "APPLICATION"          : 0x01,
        "BOOTLOADER"           : 0x02,
        "EEPROM"               : 0x03,
        "FUSES"                : 0x04,
        "LOCKBITS"             : 0x05,
        "USER_SIGNATURE"       : 0x06,
        "FACTORY_CALIBRATION"  : 0x07
    }

    xprog_erase_types = {
        "CHIP"                 : 0x01,
        "APPLICATION"          : 0x02,
        "BOOT"                 : 0x03,
        "EEPROM"               : 0x04,
        "APPLICATION_PAGE"     : 0x05,
        "BOOTLOADER_PAGE"      : 0x06,
        "EEPROM_PAGE"          : 0x07,
        "USER_SIGNATURE"       : 0x08
    }


    @staticmethod
    def find(dictionary, find_value):
        friendly_name = "<UNKNOWN>"

        for key, value in dictionary.iteritems():
            if value == find_value:
                friendly_name = key
                break

        return ("%s (0x%02x)" % (friendly_name, find_value))

