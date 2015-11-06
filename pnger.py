from collections import namedtuple
import zlib

class InvalidPNG(Exception):
    pass

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

def parse_ihdr_data(ihdr_data):
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

def parse_idat_data(idat_data):
    Compressed = namedtuple(
        'Compressed', ['method', 'flags', 'data', 'check'])

    data_end = len(idat_data) - 4

    return Compressed(
        method=idat_data[0],
        flags=idat_data[1],
        data=idat_data[2:data_end],
        check=idat_data[data_end:]
    )

if __name__ == '__main__':
    with open('ok.png', 'rb') as file:
        image = file.read()

    valid_png_header = b'\x89PNG\r\n\x1a\n'

    if image[0:8] != valid_png_header:
        raise InvalidPNG('not a valid header')

    chunks = split_into_chunks(image[8:])

    ihdr_chunk = [
        chunk for chunk in chunks 
        if chunk.get('type') == 'IHDR'
    ][0]

    ihdr = parse_ihdr_data(ihdr_chunk.get('data'))

    idat_chunk = [
        chunk for chunk in chunks 
        if chunk.get('type') == 'IDAT'
    ][0]

    image_data = zlib.decompress(idat_chunk.get('data'))
