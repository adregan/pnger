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
        raise InvalidPNG('not a valid header')

    chunks = split_into_chunks(image[8:])

    ihdr_chunk = [
        chunk for chunk in chunks 
        if chunk.get('type') == 'IHDR'][0]
    ]

    ihdr_data = ihdr_chunk.get('data')
    image_width = int.from_bytes(ihdr_data[0:4], 'big')
    image_height = int.from_bytes(ihdr_data[4:8], 'big')

    idat_chunk = [
        chunk for chunk in chunks 
        if chunk.get('type') == 'IDAT'][0]
    ]

    image_data = idat_chunk.get('data')
