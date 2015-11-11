from filters import Filters

filt = Filters('reconstruct')

def reconstructer(scanlines, bpp):
    reconstructed = [list(scanline.get('bytes')) for scanline in scanlines]

    def reconstruct_byte(filter_type, current_byte, y, x):
        above = y - 1
        left = x - bpp
        a = 0 if left < 0 else reconstructed[y][left]
        b = 0 if above < 0 else reconstructed[above][x]
        c = 0 if (above < 0 or left < 0) else reconstructed[above][left]

        return filt[filter_type](current_byte, a, b, c)

    for y, scanline in enumerate(scanlines):
        for x, current_byte in enumerate(scanline.get('bytes')):
            reconstructed[y][x] = reconstruct_byte(
                scanline.get('type'), current_byte, y, x)

    return reconstructed