'''
            GDP - The Generic Device Programmer.

    By Dean Camera (dean [at] fourwalledcubicle [dot] com)
'''


class Util(Exception):
    @staticmethod
    def chunk_data(data, chunksize, startaddress):
        for i, c in enumerate(data[ : : chunksize]):
            current_offset = i * chunksize

            yield (startaddress + current_offset,
                   data[current_offset : current_offset + chunksize])


    @staticmethod
    def chunk_address(length, chunksize, startaddress):
        length += chunksize - (length % chunksize)

        for i in xrange(0, length, chunksize):
            yield (i + startaddress, chunksize)


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
