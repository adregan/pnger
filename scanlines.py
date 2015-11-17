def split_scanlines(width, height, bytes_per_pixel, data):
    scanline_length = width * bytes_per_pixel + 1

    return [
        {'type': scanline[0], 'bytes': scanline[1:]}
        for scanline in [
            data[(scanline_length * i):(scanline_length * (i + 1))]
            for i in range(height)]]
