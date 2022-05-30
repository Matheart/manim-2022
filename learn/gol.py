from manim import *

class CellBoard(VGroup):
    """
    @param side_length: side_length of one single cell
    @param dimension: (width, height)
        width: number of cells in one row
        height: number of cells in one column
    @param color: default color of the cell
    @param rule: the Game of life rule, now only accept Bxx/Sxx format
    """
    def __init__(self, side_length = 0.5, dimension = (10, 10), color = GREY, rule = 'B3/S23', **kwargs):
        super().__init__(**kwargs)
        self.side_length = side_length
        self.dimension = dimension
        self.color = color

        for i in range(self.dimension[0] * self.dimension[1]):
            self.add(Square(side_length = self.side_length, color = self.color, fill_color = self.color, fill_opacity = 1))
        
        # this custom_buff may be changed if the visual effect is not satisfactory
        custom_buff = 0
        if dimension[0] * dimension[1] < 100:
            custom_buff = side_length / 5.0
        elif dimension[0] * dimension[1] <= 225:
            custom_buff = side_length / 4.0

        self.arrange_in_grid(self.dimension[0], self.dimension[1], buff = custom_buff)


class Test(Scene):
    def construct(self):
        board = VGroup(*[Square(side_length = 0.5, color = GREY, fill_color = GREY, fill_opacity = 1) for i in range(100)]).arrange_in_grid(10, 10, buff = 0.1)
        self.add(board)

class CellBoardTest(Scene):
    def construct(self):
        board = CellBoard(side_length = 0.3, dimension = (15, 15))
        self.add(board)