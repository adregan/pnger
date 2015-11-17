from decoder import Decoder
from pixels import create_pixels
from colors.classifier import Classifier, Point
import json

def run(file_name):
    decoder = Decoder('{}.png'.format(file_name))

    pixel_lines = [
        create_pixels(decoder.Pixel, scanline, decoder.bytes_per_pixel)
        for scanline in decoder.decode()
    ]

    c = Classifier()
    color_lines = []
    for line in pixel_lines:
        colors = [
            c.classify(Point(pixel.red, pixel.green, pixel.blue, pixel.alpha))
            for pixel in line
        ]

        color_lines.append(colors)

    with open('{}_colors.json'.format(file_name), 'w') as file:
        file.write(json.dumps(color_lines))

if __name__ == '__main__':
    run('test')
