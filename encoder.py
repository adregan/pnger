from filters import Filters
from pixels import PIXELS
from chunks import create_ihdr_data, create_chunk, create_image_data

def filterer(scanlines, bpp):
    original = [list(scanline.get('bytes')) for scanline in scanlines]
    filtered = list(original)

    def filter_byte(filter_type, current_byte, y, x):
        above = y - 1
        left = x - bpp
        a = 0 if left < 0 else original[y][left]
        b = 0 if above < 0 else original[above][x]
        c = 0 if (above < 0 or left < 0) else original[above][left]

        return Filters('filter')[filter_type](current_byte, a, b, c)

    for y, scanline in enumerate(scanlines):
        for x, current_byte in enumerate(scanline.get('bytes')):
            filtered[y][x] = filter_byte(
                scanline.get('type'), current_byte, y, x)

    return filtered

class Encoder(object):
    def __init__(self, output_path):
        self.output_path = output_path
        self.image_data = None

    def encode(self, image_bytes, width, height, color_type=2, bit_depth=8,
        compression_type=0, interlace_type=0):
        try:
            pixel = PIXELS[color_type]
        except KeyError as err:
            raise NotImplementedError('I haven\'t done that yet.')
        else:
            bpp = int(
                len(pixel._fields) * (bit_depth / 8))

        if compression_type != 0 or interlace_type != 0:
            raise NotImplementedError(
                'Only compression type 0 and interlace type 0 supported.')

        image_header_data = create_ihdr_data(
            width, height, bit_depth, color_type, 0, 0)

        image_data = create_image_data(image_bytes, width, height, bpp)
