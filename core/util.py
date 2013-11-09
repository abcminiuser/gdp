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
