from manim import *
import numpy as np
from PIL import Image

class Picture(VGroup):
    def __init__(self, path):
        super().__init__()

        self.image = Image.open(path)
        self.size = self.image.size
        Colors = []
        for i in range(self.size[0]):
            Colors.append([])
            for j in range(self.size[1]):
                pixel = self.image.getpixel((i, j))
                Colors[i].append(
                    rgb_to_color(
                        np.array([
                            pixel[0], pixel[1], pixel[2]
                        ]) / 255.0
                    )
                )
        
        self.pixel = []
        self.row = []
        self.pixel_position = []
        