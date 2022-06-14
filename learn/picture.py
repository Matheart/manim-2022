from manim import *
import numpy as np
from PIL import Image

class Template(Scene):
    def construct(self):
        screen_height = 8

        image = Image.open("/Users/htwong/Desktop/Code/manim-2022/LeZhengChuiXing/projectfiles/07-Exercise_1_picture/test3.jpg")
        size = image.size
        Col = []
        for i in range(size[0]):
            Col.append([])
            for j in range(size[1]):
                pixel = image.getpixel((i, j))
                Col[i].append(rgb_to_color(
                    np.array([
                        pixel[0],
                        pixel[1],
                        pixel[2] 
                    ]) / 255
                ))
        
        pixels = []
        all_pixels = VGroup()
        
        for i in range(size[0]):
            pixels.append([])
            for j in range(size[1]):
                sq = Square(
                    stroke_width = 0,
                    fill_color = Col[j][size[0] - i - 1], 
                    # flip?
                    fill_opacity = 1
                ).scale(screen_height / (2 * size[0]))
                """.shift(
                    screen_height*(np.array([j+0.5,i+0.5,0])/size[0]) - np.array([screen_height,screen_height,0])/2
                )"""
                pixels[i].append(sq)
                all_pixels.add(sq)
        all_pixels.arrange_in_grid(size[0], size[1], buff = 0)  
        self.play(FadeIn(all_pixels), lag_ratio = 2.0 / (size[0] * size[1]), run_time = 3)

