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
def Filters(mode):
    def none(x, a, b, c):
        ''' filter = Orig(x)
            reconstruct = Filt(x)
            Will always return the current byte
        '''
        return x

    def sub(x, a, b, c):
        ''' filter = Orig(x) - Orig(a)
            filter = current_byte - original_byte_to_the_left

            reconstruct = Filt(x) + Recon(a)
            reconstruct = current_byte + reconstructed_byte_to_the_left
        '''
        if mode == 'filter':
            return int(x - a) % 256
        else:
            return int(x + a) % 256

    def up(x, a, b, c):
        ''' filter = Orig(x) - Orig(b)
            filter = current_byte - original_byte_above

            reconstruct = Filt(x) + Recon(b)
            reconstruct = current_byte + reconstructed_byte_above
        '''
        if mode == 'filter':
            return int(x - b) % 256
        else:
            return int(x + b) % 256

    def average(x, a, b, c):
        ''' filter = Orig(x) - floor((Orig(a) + Orig(b)) / 2)
            filter = current_byte - floor((original_byte_to_the_left + original_byte_above) / 2)

            reconstruct = Filt(x) + floor((Recon(a) + Recon(b)) / 2)
            reconstruct = current_byte + floor((reconstructed_byte_to_the_left + reconstructed_byte_above) / 2)
        '''
        if mode == 'filter':
            return int(x - math.floor((a + b)/ 2)) % 256
        else:
            return int(x + math.floor((a + b)/ 2)) % 256

    def paeth(x, a, b, c):
        ''' filter = Orig(x) - PaethPredictor(Orig(a), Orig(b), Orig(c))
            filter = current_byte - PaethPredictor(original_byte_to_the_left, original_byte_above, original_byte_above_and_left)

            reconstruct = Filt(x) + PaethPredictor(Recon(a), Recon(b), Recon(c))
            reconstruct = current_byte + PaethPredictor(reconstructed_byte_to_the_left, reconstructed_byte_above, reconstructed_byte_above_and_left)
        '''
        def PaethPredictor(a, b, c):
            p = a + b - c
            pa = abs(p - a)
            pb = abs(p - b)
            pc = abs(p - c)
            if (pa <= pb and pa <= pc):
                return a
            elif (pb <= pc):
                return b
            else:
                return c
        if mode == 'filter':
            return int(x - PaethPredictor(a, b, c)) % 256
        else:
            return int(x + PaethPredictor(a, b, c)) % 256

    return [none, sub, up, average, paeth]
