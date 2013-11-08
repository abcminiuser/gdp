'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''

from abc import ABCMeta, abstractmethod


class ProtocolError(Exception):
    pass


class Protocol(object):
    __metaclass__ = ABCMeta


    @staticmethod
    def _chunk_data(data, chunksize, startaddress):
        for i, c in enumerate(data[ : : chunksize]):
            current_address = i * chunksize
            yield (startaddress + current_address,
                   data[current_address : current_address + chunksize])


    @staticmethod
    def _chunk_address(length, chunksize, startaddress):
        for i in xrange(0, length, chunksize):
            yield (i + startaddress, chunksize)

        rem_bytes = length % chunksize
        yield (startaddress + (length - rem_bytes), chunksize)


    @abstractmethod
    def get_vtarget(self):
        pass


    @abstractmethod
    def set_interface_frequency(self, target_frequency):
        pass


    @abstractmethod
    def enter_session(self):
        pass


    @abstractmethod
    def exit_session(self):
        pass


    @abstractmethod
    def erase_memory(self, memory_space):
        pass


    @abstractmethod
    def read_memory(self, memory_space, offset, length):
        pass


    @abstractmethod
    def write_memory(self, memory_space, offset, data):
        pass


    @abstractmethod
    def open(self):
        pass


    @abstractmethod
    def close(self):
        pass
