from filters import Filters

def reconstructer(scanlines, bpp):
    reconstructed = []

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

        return Filters[filter_type](current_byte, a, b, c)

    for y, scanline in enumerate(scanlines):
        reconstructed_bytes = [
            reconstruct_byte(scanline.get('type'), current_byte, y, x)
            for x, current_byte in enumerate(scanline.get('bytes'))]

        reconstructed.append(reconstructed_bytes)

    return reconstructed