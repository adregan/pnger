from collections import namedtuple
import zlib
import struct
import math
from errors import InvalidPNG
from crc import CRC

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
    chunk_length = len(data).to_bytes(4, 'big')
    buf = chunk_type + data
    crc = CRC().create(buf)

    return chunk_length + chunk_type + data + crc

# def add_padding(image_bytes, total):
#     ''' add_padding : Bytes Int -> Bytes
#     add_padding adds null bytes at random throughout the data
#     '''
#     import random


#     return image_bytes

def create_image_data(image_bytes, ratio, bytes_per_pixel):
    ''' create_image_data: Bytes Fraction Int -> Bytes
    creates the Byte string containing the image scanlines at a given ratio
    '''
    total_pixels = math.ceil(len(image_bytes) / bytes_per_pixel)

    con_number = math.sqrt(total_pixels / (ratio.numerator * ratio.denominator))

    height = math.ceil(con_number * ratio.denominator)

    width = math.ceil(con_number * ratio.numerator)

    bytes_per_row = width * bytes_per_pixel

    # Adding a single null byte to the start of every row as the filter type 0
    # TODO: Optimize filter types
    scan_rows = [
        bytes(1) + image_bytes[i * bytes_per_row:(i + 1) * bytes_per_row]
        for i in range(height)
    ]    
    # filling in padding on last row
    scan_rows[height - 1] = scan_rows[height - 1] + bytes(
        bytes_per_row -  len(scan_rows[height - 1]))

    return zlib.compress(b''.join(scan_rows))

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

    width_b = width.to_bytes(4, 'big')
    height_b = height.to_bytes(4, 'big')
    bit_depth_b = bit_depth.to_bytes(1, 'big')
    color_type_b = color_type.to_bytes(1, 'big')
    compression_type_b = compression_type.to_bytes(1, 'big')
    filter_type_b = filter_type.to_bytes(1, 'big')
    interlace_type_b = interlace_type.to_bytes(1, 'big')

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
