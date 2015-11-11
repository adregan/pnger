from filters import Filters

filt = Filters('filter')

def filterer(scanlines, bpp):
    filtered = [list(scanline.get('bytes')) for scanline in scanlines]

    def filter_byte(filter_type, current_byte, y, x):
        above = y - 1
        left = x - bpp
        a = 0 if left < 0 else filtered[y][left]
        b = 0 if above < 0 else filtered[above][x]
        c = 0 if (above < 0 or left < 0) else filtered[above][left]

        return filt[filter_type](current_byte, a, b, c)

    for y, scanline in enumerate(scanlines):
        for x, current_byte in enumerate(scanline.get('bytes')):
            scanline_bytes[y][x] = filter_byte(
                scanline.get('type'), current_byte, y, x)

    return filtered