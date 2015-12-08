CRC_POLY = 0xEDB88320
INITIAL_CRC = 0xFFFFFFFF

class CRC(object):
    def __init__(self):
        self.table = {c: self._compute_entry(c) for c in range(256)}

    def _compute_entry(self, c):
        ''' _compute_entry : Int -> Int
        Builds an entry in the CRC table from an Int (0 <= c <= 255) using
        the CRC algorithm described here: 
        http://stigge.org/martin/pub/SAR-PR-2006-05.pdf
        >>> assert crc._compute_entry(0) == 0
        >>> assert crc._compute_entry(113) == 654459306
        >>> assert crc._compute_entry(248) == 3009837614
        '''
        for _ in range(8):
            if c & 1:
                c = CRC_POLY ^ c >> 1
            else:
                c = c >> 1

        return c

    # create : bytes -> bytes
    def create(self, buf):
        ''' create : Bytes -> Bytes
        Where buf is the contents of the chunk type and the chunk data 
        as a string of bytes.
        '''
        crc = INITIAL_CRC
        for i, byt in enumerate(buf):
            crc = self.table[(crc ^ byt) & 0xFF] ^ (crc >> 8)

        return (crc ^ INITIAL_CRC).to_bytes(4, 'big')

if __name__ == '__main__':
    import doctest
    doctest.testmod(extraglobs={'crc': CRC()})
