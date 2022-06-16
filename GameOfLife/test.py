"""
File Name: test.py
Create Time: 2022.05.30
轮子测试代码
"""

from manim import *
from gol import CellBoard

class CellBoardTest(Scene):
    def construct(self):
        board = CellBoard(side_length = 0.3, dimension = (5, 15))
        self.add(board)

class CellCenterTest(Scene):
    def construct(self):
        board = CellBoard(dimension = (5, 7))

        self.add(board)
        for i in range(1, 6): # height
            for j in range(1, 8): # width
                print(f"({i}, {j}): {board.get_cell_center(i, j)}")
                circ = Circle(color = RED, radius = 0.1).move_to( board.get_cell_center(i, j) )
                self.play(FadeIn(circ))

class SetStageboardTest(Scene):
    def construct(self):
        #np.set_printoptions(threshold = np.inf)
        board = CellBoard(side_length = 6/47.0, dimension = (47, 47))
        board.set_stageboard_by_rle(file_path = 'star-board.rle')
        self.add(board)

        for _ in range(15):
            self.wait(0.2)
            board.step()
        print(board.board_arr)

class StepTest(Scene):
    def construct(self):
        grid = CellBoard(
            side_length = 0.3, 
            dimension = (50, 50),
            colors = {'live': WHITE, 'dead': BLUE_C, 'empty': GREY}
        )
        arr = np.zeros((50, 50))

        arr[25, 23:28] = 1
        arr[22:25, 26] = 1
        arr[30, 17:21] = 1

        grid.set_stageboard(arr)

        self.add(grid)

        for _ in range(30):
            self.wait(0.2)
            grid.step()

class SetSquareColorTest(Scene):
    def construct(self):
        sq = Square(color = GREY, fill_opacity = 1, fill_color = GREY)
        self.add(sq)
        self.wait(1)
        sq.set_color(BLUE_C).set_style(fill_opacity = 0.5, fill_color = BLUE_C, stroke_width = 0)
        self.wait(1)