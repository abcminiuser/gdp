'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''


class ProtocolError(Exception):
    pass


class Protocol(object):
    def __init__(self):
        raise NotImplementedError


    def get_vtarget(self):
        raise NotImplementedError


    def set_interface_frequency(self, target_frequency):
        raise NotImplementedError


    def enter_session(self):
        raise NotImplementedError


    def exit_session(self):
        raise NotImplementedError


    def erase_memory(self, memory_space):
        raise NotImplementedError()


    def read_memory(self, memory_space, offset, length):
        raise NotImplementedError()


    def write_memory(self, memory_space, offset, data):
        raise NotImplementedError()


    def open(self):
        raise NotImplementedError


    def close(self):
        raise NotImplementedError
