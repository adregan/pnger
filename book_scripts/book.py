import json

def make_book(file_name, book_title, author):
    with open('{}.json'.format(file_name), 'r') as file:
        data = json.loads(file.read())

    num_of_chapters = len(data)

    with open('book.txt', 'w') as file:
        file.write('{}\n\n\n'.format(book_title))
        file.write('By {}\n\n\n'.format(author))
        for i, chapter in enumerate(data):
            file.write('Chapter {}\n\n'.format(i+1))
            file.write('{}\n\n'.format('. '.join(chapter)))

if __name__ == '__main__':
    make_book(
        'cover_colors',
        book_title='The Cover of The Sun Also Rises',
        author='Duncan Regan'
    )