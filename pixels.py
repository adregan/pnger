from collections import namedtuple

PIXELS = {
    0: namedtuple('Pixel', ['gray']),
    2: namedtuple('Pixel', ['red', 'green', 'blue']),
    # 3: A Palette index,
    4: namedtuple('Pixel', ['gray', 'alpha']),
    6: namedtuple('Pixel', ['red', 'green', 'blue', 'alpha'])
}

def create_pixels(Pixel, scanline, bytes_per_pixel):
    pixel_range = range(len(scanline))[::bytes_per_pixel]

    return [
        Pixel(*scanline[pixel_index:pixel_range[i+1]])
        for i, pixel_index in enumerate(pixel_range[:-1])]
