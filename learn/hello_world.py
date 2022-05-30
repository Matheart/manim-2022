from manim import *

class HelloWorld(Scene):
    def construct(self):
        sq = Square()
        circ = Circle()
        self.play(Transform(sq, circ))
        self.wait()