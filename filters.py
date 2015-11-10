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
    return current_byte

def sub(scanlines, position, type, bytes_per_pixel, reconstructed):
    ''' filter = Orig(x) - Orig(a)
        filter = current_byte - original_byte_to_the_left

        reconstruct = Filt(x) + Recon(a)
        filter = current_byte + reconstructed_byte_to_the_left
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
        filter = current_byte + reconstructed_byte_above
    '''
    scanline = scanlines[position.y].get('bytes', [])
    current_byte = scanline[position.x]

    if type == 'filter':
        original_byte_above = 0 if ((position.y - 1) < 0) else scanlines[position.y - 1].get('bytes')[position.x]

        return int(current_byte - original_byte_above)
    else:
        reconstructed_byte_above = 0 if ((position.y - 1) < 0) else reconstructed[position.y - 1][position.x]

        return int(current_byte + reconstructed_byte_above)


# def average(current_byte, prior_byte, byte_above, byte_prior_to_above, bytes_per_pixel):
#     pass
# def paeth(current_byte, prior_byte, byte_above, byte_prior_to_above, bytes_per_pixel):
#     pass

Filters = {
    0: none,
    1: sub,
    2: up,
    # 3: average,
    # 4: paeth
}