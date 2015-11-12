''' Converted from http://gauth.fr/2011/09/get-a-color-name-from-any-rgb-combination/
    x = R
    y = G
    z = B
'''

import math
import json

with open('colors.json') as file:
    COLORS = json.loads(file.read())

class Point(object):
    def __init__(self, x, y, z, a=255, label=None):
        self.x = x
        self.y = y
        self.z = z
        self.a = a
        self.label = label

    def dist(self, color):
        x = abs(color['x'] - self.x)
        y = abs(color['y'] - self.y)
        z = abs(color['z'] - self.z)

        return math.sqrt(x * x + y * y + z * z)

class Classifier(object):
    def __init__(self):
        self.data = COLORS
    def classify(self, point):
        minimum = float('inf')
        minimum_index = -1
        for i, color in enumerate(self.data):
            dist = point.dist(color);
            if dist < minimum:
                minimum = dist;
                minimum_index = i;
            if 190 >= point.a <= 250:
                alpha = ', slightly transparent'
            elif 127 >= point.a < 190:
                alpha = ', fairly transparent'
            elif 63 >= point.a < 127:
                alpha = ', mostly transparent'
            elif 5 >= point.a < 63:
                alpha = ', very transparent'
            elif point.a < 5:
                alpha = ', pretty much invisible'
            else:
                alpha = ''
        
        return self.data[minimum_index].get('label') + alpha
