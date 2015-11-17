from chunks import split_into_chunks, parse_header_and_data
from pixels import PIXELS
from scanlines import split_scanlines
from filters import Filters

def reconstructer(scanlines, bpp):
    reconstructed = [list(scanline.get('bytes')) for scanline in scanlines]

    def reconstruct_byte(filter_type, current_byte, y, x):
        above = y - 1
        left = x - bpp
        a = 0 if left < 0 else reconstructed[y][left]
        b = 0 if above < 0 else reconstructed[above][x]
        c = 0 if (above < 0 or left < 0) else reconstructed[above][left]

        return Filters('reconstruct')[filter_type](current_byte, a, b, c)

    for y, scanline in enumerate(scanlines):
        for x, current_byte in enumerate(scanline.get('bytes')):
            reconstructed[y][x] = reconstruct_byte(
                scanline.get('type'), current_byte, y, x)

    return reconstructed

class Decoder(object):
    def __init__(self, file_path):
        with open('{}'.format(file_path), 'rb') as file:
            self.image = file.read()

        valid_png_header = b'\x89PNG\r\n\x1a\n'

        if self.image[0:8] != valid_png_header:
            raise InvalidPNG('not a valid header')

        self.chunks = split_into_chunks(self.image[8:])
        self.header, self.data = parse_header_and_data(self.chunks)

        try:
            self.pixel = PIXELS[self.header.color_type]
        except KeyError as err:
            raise KeyError('I haven\'t done that yet.')
        else:
            self.bpp = int(
                len(self.pixel._fields) * (self.header.bit_depth / 8))

    @property
    def Pixel(self):
        return self.pixel

    @property
    def bytes_per_pixel(self):
        return self.bpp

    def decode(self):
        scanlines = split_scanlines(
            self.header.width,
            self.header.height,
            self.bytes_per_pixel, 
            self.data
        )

        return reconstructer(
            scanlines, self.bytes_per_pixel)
