'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from formats.format import *
from formats.formatsection import *
from formats.format_binary import *
from formats.format_intelhex import *

gdp_formats = {
        'bin'   :   FormatBinary,
        'hex'   :   FormatIntelHex,
        'eep'   :   FormatIntelHex,
    }
