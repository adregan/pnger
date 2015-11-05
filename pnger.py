class InvalidPNG(Exception):
    pass

def split_into_chunks(file_bytes, chunks=[]):
    ''' chunks should look like this:
        {'length': int, 'type': str, 'data': bytes, 'crc': int}
    '''
    if not file_bytes:
        return chunks

    chunk_data_length = int.from_bytes(file_bytes[0:4], 'big')
    data_end = 8 + chunk_data_length
    chunk_end = data_end + 4
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

if __name__ == '__main__':
    with open('ok.png', 'rb') as file:
        image = file.read()

    valid_png_header = b'\x89PNG\r\n\x1a\n'

    if image[0:8] != valid_png_header:
        raise ErrorDude('not a valid header')

    chunks = split_into_chunks(image[8:])

    # IHDR_data_length = int.from_bytes(image[8:12], 'big')

    # if image[12:16] != b'IHDR' or IHDR_data_length != 13:
    #     raise ErrorDude('Invalid IHDR chunk')

    # IHDR_data = image[16:29]

    # width = int.from_bytes(
    #     IHDR_data[0:4],
    #     'big'
    # )

    # height = int.from_bytes(
    #     IHDR_data[4:8],
    #     'big'
    # )

    # bit_depth = IHDR_data[8]
    # color_type = IHDR_data[9]
    # compression_type = IHDR_data[10]
    # filter_type = IHDR_data[11]
    # interlace_type = IHDR_data[12]

    # IHDR_crc = image[29:33]

    # second_chunk_length = int.from_bytes(
    #     image[33:37],
    #     'big'
    # )
    # second_chunk_type = image[37:41]
    # second_chunk_data = image[41:41+second_chunk_length]
    # second_chunk_crc = image[41+second_chunk_length:41+second_chunk_length+4]