'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''


from formats.format import *


class FormatSection(Format):
    def __init__(self, format_instance):
        raise NotImplementedError


    def get_name(self):
        raise NotImplementedError


    def get_bounds(self):
        raise NotImplementedError


    def get_data(self):
        raise NotImplementedError
