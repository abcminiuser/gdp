'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

class TransportError(Exception):
    pass


class Transport(object):
    def __init__(self):
        raise NotImplementedError


    def open(self):
        raise NotImplementedError


    def close(self):
        raise NotImplementedError


    def read(self):
        raise NotImplementedError


    def write(self, data):
        raise NotImplementedError
