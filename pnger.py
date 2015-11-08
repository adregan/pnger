from collections import namedtuple
import zlib

class InvalidPNG(Exception):
    pass

class UnderConstruction(Exception):
    ''' Imagine the little animated GIF
    '''
    pass

# TODO: Make dicts to hold the different pixel types 
# and the different filter types

def split_into_chunks(file_bytes, chunks=[]):
    ''' chunks should look like this:
        {'length': int, 'type': str, 'data': bytes, 'crc': int}
    '''
    if not file_bytes:
        return chunks

    chunk_data_length = int.from_bytes(file_bytes[0:4], 'big')
    data_end = 8 + chunk_data_length # 8 bytes for the length and the type
    chunk_end = data_end + 4 # The 4 bytes represent the crc
    chunk_type = file_bytes[4:8].decode('utf-8')
    chunk_data = file_bytes[8:data_end]
    chunck_crc = file_bytes[data_end:chunk_end]

    chunk = {
        'length': chunk_data_length,
        'type': chunk_type,
        'data': chunk_data,
        'crc': chunck_crc
    }

    chunks.append(chunk)

    return split_into_chunks(file_bytes[chunk_end:], chunks)

def parse_ihdr_data(ihdr_chunk):
    ihdr_data = ihdr_chunk.get('data')
    Header = namedtuple(
        'Header',
        ['width', 'height', 'bit_depth', 'color_type','compression_type',
        'filter_type', 'interlace_type'])    

    return Header(
        width=int.from_bytes(ihdr_data[0:4], 'big'),
        height=int.from_bytes(ihdr_data[4:8], 'big'),
        bit_depth=ihdr_data[8],
        color_type=ihdr_data[9],
        compression_type=ihdr_data[10],
        filter_type = ihdr_data[11],
        interlace_type = ihdr_data[12]
    )

def parse_chunks(chunks):
    try:
        image_header = parse_ihdr_data([
            chunk for chunk in chunks 
            if chunk.get('type') == 'IHDR'
        ][0])
    except IndexError as err:
        raise InvalidPNG('Missing IHDR chunk')

    try:
        image_data = zlib.decompress(
            b''.join([
                idat.get('data')
                for idat in [
                    chunk for chunk in chunks 
                    if chunk.get('type') == 'IDAT']]))
    except IndexError as err:
        raise InvalidPNG('Invalid IDAT chunks')

    return image_header, image_data

def split_scanlines(width, height, pixel_size, data):
    scanline_length = width * pixel_size + 1

    scanlines = [
        data[(scanline_length * i):(scanline_length * (i + 1))]
        for i in range(height)
    ]

    return scanlines

def create_pixel_scanlines(header, data):
    if header.color_type == 6:
        Pixel = namedtuple('Pixel', ['red', 'green', 'blue', 'alpha'])
    else:
        # TODO: implement other color types
        raise UnderConstruction('Sorry dude.')

    scanlines = split_scanlines(
        header.width, header.height, len(Pixel._fields), data)

    return [create_pixels(Pixel, scanline) for scanline in scanlines]

if __name__ == '__main__':
    with open('ok.png', 'rb') as file:
        image = file.read()

    valid_png_header = b'\x89PNG\r\n\x1a\n'

    if image[0:8] != valid_png_header:
        raise InvalidPNG('not a valid header')

    image_header, image_data = parse_chunks(split_into_chunks(image[8:]))

    scanlines = create_scanlines(image_header, image_data)
