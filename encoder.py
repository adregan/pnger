from filters import Filters

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
    def __init__(self):
        pass