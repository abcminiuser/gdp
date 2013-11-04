'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

class FormatError(Exception):
    pass


class Format(object):
    def __init__(self):
        raise NotImplementedError


    def get_sections(self):
        raise NotImplementedError

