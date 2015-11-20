'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)

   Release under a MIT license; see LICENSE.txt for details.
'''

from core.util import *
from formats.format import *
from formats.formatsection import *
from formats.format_binary import *
from formats.format_intelhex import *
from formats.format_elf import *


def get_gdp_format_reader_extensions():
    handlers = dict()

    for f in Util.get_subclasses(FormatReader):
        handlers[f.get_name()] = f.get_extensions()

    return handlers


def get_gdp_format_reader(file_extension):
    for f in Util.get_subclasses(FormatReader):
        if file_extension in f.get_extensions():
            return f

    raise KeyError()


def get_gdp_format_writer_extensions():
    handlers = dict()

    for f in Util.get_subclasses(FormatWriter):
        handlers[f.get_name()] = f.get_extensions()

    return handlers


def get_gdp_format_writer(file_extension):
    for f in Util.get_subclasses(FormatWriter):
        if file_extension in f.get_extensions():
            return f

    raise KeyError()
