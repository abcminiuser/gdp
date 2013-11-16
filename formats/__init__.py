'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from core.util import *
from formats.format import *
from formats.formatsection import *
from formats.format_binary import *
from formats.format_intelhex import *
from formats.format_elf import *


def get_gdp_format_extensions():
    handlers = dict()

    for f in Util.get_subclasses(Format):
        handlers[f.get_name()] = f.get_extensions()

    return handlers


def get_gdp_format(file_extension):
    for f in Util.get_subclasses(Format):
        if file_extension in f.get_extensions():
            return f

    raise KeyError()
