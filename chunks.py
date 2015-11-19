from collections import namedtuple
import zlib
import struct
from errors import InvalidPNG

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

def create_chunk(data, type):
    chunk_type = bytes(type, 'utf-8')
    chunk_length = bytes(str(len(data)), 'utf-8')
    # TODO: CRC FOR REAL http://www.w3.org/TR/PNG/#5CRC-algorithm
    crc = bytes(4)

    return chunk_length + chunk_type + chunk_data + crc

def create_ihdr_data(
    width,
    height,
    bit_depth=8,
    color_type=2, 
    compression_type=0,
    interlace_type=0):

    # Filter type is ALWAYS 0
    filter_type=0

    if bit_depth != 8:
        raise NotImplementedError(
            'Sorry, bit depths other than 8 have not yet been implemented')

    width_b = struct.pack('<I', width)
    height_b = struct.pack('<I', height)
    bit_depth_b = bytes(str(bit_depth), 'utf-8')
    color_type_b = bytes(str(color_type), 'utf-8')
    compression_type_b = bytes(str(compression_type), 'utf-8')
    filter_type_b = bytes(str(filter_type), 'utf-8')
    interlace_type_b = bytes(str(interlace_type), 'utf-8')

    data = (
        width_b + height_b + bit_depth_b + color_type_b + 
        compression_type_b + filter_type_b + interlace_type_b)

    return data

def parse_header_and_data(chunks):
    ''' Returns the IHDR and IDAT from the chunks
    '''
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
