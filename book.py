import json

def make_book(file_name):
    with open('{}.json'.format(file_name), 'r') as file:
        data = json.loads(file.read())

    num_of_chapters = len(data)

    with open('book.txt', 'w') as file:
        file.write('The Cover of The Sun Also Rises\n\n\n')
        file.write('By Duncan Regan\n\n\n')
        for i, chapter in enumerate(data):
            file.write('Chapter {}\n\n'.format(i+1))
            file.write('{}\n\n'.format('. '.join(chapter)))

if __name__ == '__main__':
    make_book('cover_colors')