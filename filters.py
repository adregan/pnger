import math

''' Filter Algorithms
    http://www.w3.org/TR/PNG/#9Filters

    > Filters are applied to bytes, not to pixels, regardless of the bit depth
    > or color type of the image.

    Generated from the following bytes:

    Name |  Description
    ===================================================
      x  |  the current byte being filtered
      a  |  the byte corresponding to the same value in the previous pixel
      b  |  the byte corresponding to the same value in the scanline above
      c  |  the byte corresponding to the same value in the scanline above and to the left

    All of the algorithm functions take the following arguments 
    List Posn List List -> Int
    Posn is position of x, y where y is the scanline and x is the position in the scanline
'''

def none(scanlines, position, *args):
    ''' filter = Orig(x)
        reconstruct = Filt(x)
        Will always return the current byte
    '''
    current_byte = scanlines[position.y].get('bytes')[position.x]
    return current_byte % 256

def sub(scanlines, position, type, bytes_per_pixel, reconstructed):
    ''' filter = Orig(x) - Orig(a)
        filter = current_byte - original_byte_to_the_left

        reconstruct = Filt(x) + Recon(a)
        reconstruct = current_byte + reconstructed_byte_to_the_left
    '''
    scanline = scanlines[position.y].get('bytes', [])
    current_byte = scanline[position.x]

    byte_to_the_left_i = position.x - bytes_per_pixel

    if type == 'filter':
        original_byte_to_the_left = 0 if (byte_to_the_left_i < 0) else scanline[byte_to_the_left_i]
        return int(current_byte - original_byte_to_the_left)
    else:
        reconstructed_byte_to_the_left = 0 if (byte_to_the_left_i < 0) else reconstructed[position.y][byte_to_the_left_i]
        return int(current_byte + reconstructed_byte_to_the_left)

def up(scanlines, position, type, bytes_per_pixel, reconstructed):
    ''' filter = Orig(x) - Orig(b)
        filter = current_byte - original_byte_above

        reconstruct = Filt(x) + Recon(b)
        reconstruct = current_byte + reconstructed_byte_above
    '''
    scanline = scanlines[position.y].get('bytes', [])
    current_byte = scanline[position.x]

    if type == 'filter':
        original_byte_above = 0 if ((position.y - 1) < 0) else scanlines[position.y - 1].get('bytes')[position.x]
        return int(current_byte - original_byte_above)
    else:
        reconstructed_byte_above = 0 if ((position.y - 1) < 0) else reconstructed[position.y - 1][position.x]
        return int(current_byte + reconstructed_byte_above)


def average(scanlines, position, type, bytes_per_pixel, reconstructed):
    ''' filter = Orig(x) - floor((Orig(a) + Orig(b)) / 2)
        filter = current_byte - floor((original_byte_to_the_left + original_byte_above) / 2)

        reconstruct = Filt(x) + floor((Recon(a) + Recon(b)) / 2)
        reconstruct = current_byte + floor((reconstructed_byte_to_the_left + reconstructed_byte_above) / 2)
    '''
    scanline = scanlines[position.y].get('bytes', [])
    current_byte = scanline[position.x]

    byte_to_the_left_i = position.x - bytes_per_pixel
    if type == 'filter':
        original_byte_above = 0 if ((position.y - 1) < 0) else scanlines[position.y - 1].get('bytes')[position.x]
        original_byte_to_the_left = 0 if (byte_to_the_left_i < 0) else scanline[byte_to_the_left_i]

        return int(current_byte - math.floor((original_byte_to_the_left + original_byte_above)/ 2))
    else:
        reconstructed_byte_above = 0 if ((position.y - 1) < 0) else reconstructed[position.y - 1][position.x]
        reconstructed_byte_to_the_left = 0 if (byte_to_the_left_i < 0) else reconstructed[position.y][byte_to_the_left_i]

        return int(current_byte + math.floor((reconstructed_byte_to_the_left + reconstructed_byte_above)/ 2))

def paeth(scanlines, position, type, bytes_per_pixel, reconstructed):
    ''' filter = Orig(x) - PaethPredictor(Orig(a), Orig(b), Orig(c))
        filter = current_byte - PaethPredictor(original_byte_to_the_left, original_byte_above, original_byte_above_and_left)

        reconstruct = Filt(x) + PaethPredictor(Recon(a), Recon(b), Recon(c))
        reconstruct = current_byte + PaethPredictor(reconstructed_byte_to_the_left, reconstructed_byte_above, reconstructed_byte_above_and_left)
    '''
    scanline = scanlines[position.y].get('bytes', [])
    current_byte = scanline[position.x]

    byte_to_the_left_i = position.x - bytes_per_pixel
    up_and_to_the_left_i = position.x - (2 * bytes_per_pixel)

    if type == 'filter':
        original_byte_to_the_left = 0 if (byte_to_the_left_i < 0) else scanline[byte_to_the_left_i]
        original_byte_above = 0 if ((position.y - 1) < 0) else scanlines[position.y - 1].get('bytes')[position.x]
        original_byte_above_and_left = 0 if (((position.y - 1) < 0) or (byte_to_the_left_i < 0)) else scanlines[position.y - 1].get('bytes')[position.x - 1]

        return int(current_byte - PaethPredictor(
                original_byte_to_the_left,
                original_byte_above,
                original_byte_above_and_left))
    else:
        reconstructed_byte_to_the_left = 0 if (byte_to_the_left_i < 0) else reconstructed[position.y][byte_to_the_left_i]
        reconstructed_byte_above = 0 if ((position.y - 1) < 0) else reconstructed[position.y - 1][position.x]
        reconstructed_byte_above_and_left = 0 if (((position.y - 1) < 0) or (up_and_to_the_left_i < 0)) else reconstructed[position.y - 1][up_and_to_the_left_i]

        return int(current_byte + PaethPredictor(
                reconstructed_byte_to_the_left,
                reconstructed_byte_above,
                reconstructed_byte_above_and_left))

def PaethPredictor(a, b, c):
    p = a + b - c
    pa = abs(p - a)
    pb = abs(p - b)
    pc = abs(p - c)
    if (pa <= pb and pa <= pc):
        Pr = a
    elif (pb <= pc):
        Pr = b
    else:
        Pr = c

    return Pr

Filters = {
    0: none,
    1: sub,
    2: up,
    3: average,
    4: paeth
}