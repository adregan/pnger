import json
import os

def create_output_dir(directory_name='output'):
    file_path = os.path.join(os.path.dirname(__file__), directory_name)
    try:
        os.mkdir(file_path)
    except FileExistsError as err:
        split_dir = directory_name.split('.v')
        try:
            version_number = int(split_dir[1]) + 1
        except IndexError as err:
            version_number = 1
        return create_output_dir('{}.v{}'.format(split_dir[0], version_number))
    else:
        return file_path

def make_audio_book(file_name, text_dir, audio_dir):
    with open('{}.json'.format(file_name), 'r') as file:
        data = json.loads(file.read())

    full_text_chapters = [
        {
            'number': i + 1,
            'text': 'Chapter {}\n\n{}\n\n'.format(i+1, '. '.join(chapter))
        }
        for i, chapter in enumerate(data)
    ]

    for chapter in full_text_chapters:
        text = chapter.get('text')
        number = chapter.get('number')
        with open('{}/{}.txt'.format(text_dir, number), 'w') as file:
            file.write(text)
        os.system(
            'say -f {text_dir}/{number}.txt -o {audio_dir}/{number}.mp4 -v Vicki --file-format "mp4f"'
            .format(text_dir=text_dir, number=number, audio_dir=audio_dir)
        )
        os.system(
            'say -f {text_dir}/{number}.txt -o {audio_dir}/{number}.wav -v Vicki --data-format=LEF32@44100'
            .format(text_dir=text_dir, number=number, audio_dir=audio_dir)
        )
        os.system(
            'oggenc {audio_dir}/{number}.wav'.format(number=number, audio_dir=audio_dir)
        )
        os.remove('{audio_dir}/{number}.wav'.format(number=number, audio_dir=audio_dir))

if __name__ == '__main__':
    text_dir = create_output_dir('text')
    audio_dir = create_output_dir('audio')
    make_audio_book('cover_colors', text_dir, audio_dir)

