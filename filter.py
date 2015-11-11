from filters import Filters

filt = Filters('filter')

def filterer(scanlines, bpp):
    filtered = [list(scanline.get('bytes')) for scanline in scanlines]

    def filter_byte(filter_type, current_byte, y, x):
        a = b = c = 0
        try:
            a = filtered[y][x - bpp]
        except IndexError as err:
            pass
        try:
            b = filtered[y - 1][x]
        except IndexError as err:
            pass
        try:
            c = filtered[y - 1][x - bpp]
        except IndexError as err:
            pass

        return filt[filter_type](current_byte, a, b, c)

    for y, scanline in enumerate(scanlines):
        for x, current_byte in enumerate(scanline.get('bytes')):
            scanline_bytes[y][x] = filter_byte(
                scanline.get('type'), current_byte, y, x)

    return filtered