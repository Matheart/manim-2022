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
        board = CellBoard(side_length = 6/24.0, dimension = (24, 13))
        board.set_stageboard_by_rle(file_path = 'skop63.rle')
        self.add(board)
        print(board.board_arr)
        print("fuck")

        for i in range(5):
            board.step()
            self.wait(0.2)
        print(board.board_arr)