'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

import os
import sys
try:
	from intelhex import IntelHex
except ImportError:
    print("The IntelHex library is not installed.")
    sys.exit(1)


from formats.format import *
from formats.formatsection import *


class FormatIntelHex_Section(FormatSection):
    def __init__(self, instance=None):
        self.instance = instance


    def get_bounds(self):
        return (self.instance.minaddr(), self.instance.maxaddr())


    def get_data(self):
        return self.instance.tobinarray()


class FormatIntelHex(FormatReader, FormatWriter):
    def __init__(self):
        self.hexinstance = IntelHex()


    def load_file(self, filename=None):
        if filename is None:
            raise FormatError("Filename not specified.")

        file_extension = os.path.splitext(filename)[1][1 : ].lower()

        try:
            if file_extension == "bin":
                self.hexinstance.loadbin(filename)
            else:
                self.hexinstance.loadhex(filename)
        except:
            raise FormatError("Could not open %s file \"%s\"." %
                              (file_extension.upper(), filename))


    def save_file(self, filename):
        if filename is None:
            raise FormatError("Filename not specified.")

        file_extension = os.path.splitext(filename)[1][1 : ].lower()

        try:
            if file_extension == "bin":
                self.hexinstance.tofile(filename, format="bin")
            else:
                self.hexinstance.tofile(filename, format="hex")
        except:
            raise FormatError("Could not save %s file \"%s\"." %
                              (file_extension.upper(), filename))


    def add_section(self, start, data):
        self.hexinstance[start : start + len(data)] = data


    def get_sections(self):
        sections = dict()

        if self.hexinstance.minaddr() is not None:
            sections[None] = FormatIntelHex_Section(self.hexinstance)

        return sections


    @staticmethod
    def get_name():
        return "Intel HEX File Parser"


    @staticmethod
    def get_extensions():
        return ["hex", "eep"]
