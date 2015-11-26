CRC_POLY = 0xEDB88320
INITIAL_CRC = 0xFFFFFFFF

class CRC(object):
    def __init__(self):
        self.table = {c: self._compute_entry(c) for c in range(256)}

    def _compute_entry(self, c):
        for _ in range(8):
            if c & 1:
                c = CRC_POLY ^ c >> 1
            else:
                c = c >> 1

        return c

    # create : bytes -> bytes
    def create(self, buf):
        ''' Where buf is the contents of the chunk type and the chunk data
        '''
        crc = INITIAL_CRC
        for i, byt in enumerate(buf):
            crc = self.table[(crc ^ byt) & 0xFF] ^ (crc >> 8)

        return (crc ^ INITIAL_CRC).to_bytes(4, 'big')
