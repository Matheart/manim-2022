from manim import *

class HelloWorld(Scene):
    def construct(self):
        orange_sq = Square(
            color = ORANGE,
            fill_opacity = 0.5
        ).shift(2 * LEFT)

        blue_circ = Circle(
            color = BLUE,
            fill_opacity = 0.5
        ).shift(3 * RIGHT)

        self.play(Create(orange_sq), FadeIn(blue_circ))