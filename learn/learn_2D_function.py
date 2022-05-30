from manim import *
from manim.utils.color import Colors

class ExampleFunctionGraph(Scene):
    def construct(self):
        cos_func = FunctionGraph(
            lambda t: np.cos(t) + 0.5 * np.cos(7 * t) + (1 / 7) * np.cos(14 * t),
            color = RED
        )

        sin_func_1 = FunctionGraph(
            lambda t: np.sin(t) + 0.5 * np.sin(7 * t) + (1 / 7) * np.sin(14 * t),
            color = BLUE
        )

        sin_func_2 = FunctionGraph(
            lambda t:  np.sin(t) + 0.5 * np.sin(7 * t) + (1 / 7) * np.sin(14 * t),
            x_range = [-4, 4], color = GREEN
        ).move_to([0, 1, 0])

        self.add(cos_func, sin_func_1, sin_func_2)

# Note: lambda function cannot do summation
class FourierSeries(Scene):
    def construct(self):
        grid = NumberPlane(
            x_range=[-np.pi, np.pi, np.pi/4],  # step size determines num_decimal_places.
            y_range=[-1, 1, 0.25],
            x_length=5.5,
            y_length=5.5,
            tips=False,
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 4,
                "stroke_opacity": 0.3
            }
        )

        segment_func = grid.plot(
            lambda t: t / np.pi,
            color = PURPLE
        )
        self.add(segment_func, grid)

        for i, col in enumerate(Colors):
            n = i + 1

            def func(x):
                result = 0
                val = 0
                for k in range(1, n+1):
                    val = 2.0 / np.pi / float(k) * np.sin(k * x) 
                    if k % 2 == 0:
                        result -= val
                    else:
                        result += val
                return result

            func_plot = grid.plot(func).set_color(col.value).set_stroke(opacity = 0.1)
            self.add(func_plot)
            self.wait(0.2)

class ImplicitCircle(Scene):
    def construct(self):
        graph = ImplicitFunction(
            lambda x, y: x * x + y * y - 1,
            color = YELLOW
        )
        self.add(NumberPlane(), graph)

class ImplicitExamQ(Scene):
    def construct(self):
        graph = ImplicitFunction(
            lambda x, y: y * y - 2 * x * y + x * x * x,
            color = YELLOW
        )
        self.add(NumberPlane(), graph)