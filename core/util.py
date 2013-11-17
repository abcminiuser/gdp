'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''


class Util(Exception):
    @staticmethod
    def chunk_data(data, chunk_size, start_address):
        for i, c in enumerate(data[ : : chunk_size]):
            current_offset = i * chunk_size

            yield (start_address + current_offset,
                   data[current_offset : current_offset + chunk_size])


    @staticmethod
    def chunk_address(length, chunk_size, start_address):
        if (length % chunk_size):
            length += chunk_size - (length % chunk_size)

        for i in xrange(0, length, chunk_size):
            yield (i + start_address, chunk_size)


    @staticmethod
    def array_encode(data, length, endian="little"):
        if endian == "little":
            return [((data >> (8 * x)) & 0xFF) for x in xrange(length)]
        else:
            return [((data >> (8 * (length - x - 1))) & 0xFF) for x in xrange(length)]


    @staticmethod
    def array_decode(data, endian="little"):
        value = 0

        if endian == "little":
            for x in xrange(len(data)):
                value |= data[x] << (8 * x)
        else:
            for x in xrange(len(data)):
                value = (value << 8) | data[x]

        return value


    @staticmethod
    def get_subclasses(c):
        subclasses = c.__subclasses__()
        for d in list(subclasses):
            subclasses.extend(Util.get_subclasses(d))
        return subclasses
