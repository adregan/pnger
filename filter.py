from filters import Filters

def filterer(scanlines, bpp):
    scanline_bytes = [scanline.get('data') for scanline in scanlines]

    def filter_byte(filter_type, current_byte, y, x):
        a = b = c = 0
        try:
            a = scanline_bytes[y][x - bpp]
        except IndexError as err:
            pass
        try:
            b = scanline_bytes[y - 1][x]
        except IndexError as err:
            pass
        try:
            c = scanline_bytes[y - 1][x - bpp]
        except IndexError as err:
            pass

        return Filters[filter_type](current_byte, a, b, c)

    filtered = []

    for y, scanline in enumerate(scanlines):
        filtered_bytes = [
            filter_byte(scanline.get('type'), current_byte, y, x)
            for x, current_byte in enumerate(scanline.get('bytes'))]


    return filtered