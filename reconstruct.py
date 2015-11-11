from filters import Filters

filt = Filters('reconstruct')

def reconstructer(scanlines, bpp):
    reconstructed = [list(scanline.get('bytes')) for scanline in scanlines]

    def reconstruct_byte(filter_type, current_byte, y, x):
        a = b = c = 0
        try:
            a = reconstructed[y][x - bpp]
        except IndexError as err:
            pass
        try:
            b = reconstructed[y - 1][x]
        except IndexError as err:
            pass
        try:
            c = reconstructed[y - 1][x - bpp]
        except IndexError as err:
            pass

        return filt[filter_type](current_byte, a, b, c)

    for y, scanline in enumerate(scanlines):
        for x, current_byte in enumerate(scanline.get('bytes')):
            reconstructed[y][x] = reconstruct_byte(
                scanline.get('type'), current_byte, y, x)

    return reconstructed