"""
File Name: gol.py
Create Time: 2022.05.30
生命游戏轮子
"""
from manim import *
from rle_decode import *

class CellBoard(VGroup):
    def __init__(self, 
            side_length = 0.5, dimension = (10, 10), 
            colors = {'live': WHITE, 'dead': GREY, 'empty': GREY}, 
            rule = 'B3/S23', 
            **kwargs):
        """
        Purpose: Initialise the cell board (by default all are empty cells)
        @param side_length: side_length of one single cell
        @param dimension: (height, width)
            width: number of cells in one row
            height: number of cells in one column
        @param color: default color of the cell
        @param rule: the Game of life rule, now only accept Bxx/Sxx format
        """
        super().__init__(**kwargs)
        self.side_length = side_length
        self.dimension = dimension
        self.live_color = colors['live'] # 1
        self.dead_color = colors['dead'] # -1
        self.empty_color = colors['empty'] # 0
        self.rule = rule
        self.board_arr = np.zeros(dimension)

        for i in range(self.dimension[0] * self.dimension[1]):
            self.add(Square(side_length = self.side_length, color = self.empty_color, fill_color = self.empty_color, fill_opacity = 1))
        
        # this custom_buff may be changed if the visual effect is not satisfactory
        #custom_buff = 0
        if dimension[0] * dimension[1] < 100:
            custom_buff = side_length / 5.0
        else: #dimension[0] * dimension[1] <= 225:
            custom_buff = side_length / 4.0

        # height, width
        self.arrange_in_grid(self.dimension[0], self.dimension[1], buff = custom_buff)

    def get_cell(self, row, column):
        """
        Purpose: get the cell
        @param row: beginning index is 1
        @param column: beginning index is 1
        """
        if row < 1 or row > self.dimension[0]:
            raise RuntimeError('Out of range!')
        if column < 1 or column > self.dimension[1]:
            raise RuntimeError('Out of range!')
        index = (row - 1) * self.dimension[1] + column - 1
        return self[index]

    def get_cell_center(self, row, column):
        """
        Purpose: get the center of the cell
        @param row: beginning index is 1
        @param column: beginning index is 1
        """
        return self.get_cell(row, column).get_center()

    def set_stageboard(self, arr):
        """
        Purpose: Initialize the board
        @param arr 2D array, 1 means live, 0 means empty, 
        -1 means there existed dead cell be4
        """
        self.board_arr = arr
        print(self.board_arr)
        for i in range(arr.shape[0]):
            for j in range(arr.shape[1]):
                if arr[i][j] == 0:
                    self.get_cell(i + 1, j + 1).set_color(self.empty_color)
                elif arr[i][j] == 1:
                    self.get_cell(i + 1, j + 1).set_color(self.live_color)
                elif arr[i][j] == -1:
                    self.get_cell(i + 1, j + 1).set_color(self.dead_color)

    def set_stageboard_by_rle(self, file_path):
        """
        Purpose: configure the setting of the board using rtf file
        @param file_path The path to the rle file
        """
        self.set_stageboard( expand_rle(file_path) )

    def count_live_neighbour(self, x, y):
        """
        Purpose: count the number of live neighbours
        @param x begin with 0
        @param y begin with 0
        """
        cnt = 0
        loc = np.array([x, y, 0])
        directions = np.array([UP, UL, LEFT, DL, DOWN, DR, RIGHT, UR])
        for direction in directions:
            des = loc + direction
            if des[0] < 0 or des[0] >= self.dimension[0]:
                continue
            if des[1] < 0 or des[1] >= self.dimension[1]:
                continue
            dx = int(des[0])
            dy = int(des[1])
            if self.board_arr[dx][dy] == 1:
                cnt += 1
        return cnt

    def next_status(self, x, y, cnt):
        """
        Purpose: obtain the next status of the current cell
        @param x begin with 0
        @param y begin with 0
        """
        Birth, Survival = self.rule.split('/')
        Birth = Birth[1:]
        Survival = Survival[1:]

        if self.board_arr[x][y] == 1: # live
            if str(cnt) not in Survival:
                self.board_arr[x][y] = 0
                self.get_cell(x + 1, y + 1).set_color(self.dead_color)
        else: # otherwise
            if str(cnt) in Birth:
                self.board_arr[x][y] = 1
                self.get_cell(x + 1, y + 1).set_color(self.live_color)

    def step(self):
        """
        Purpose: simulate the next step based on the rule
        """
        cnt_arr = np.zeros(self.board_arr.shape)
        for x in range(self.board_arr.shape[0]):
            for y in range(self.board_arr.shape[1]):
                cnt_arr[x][y] = self.count_live_neighbour(x, y)
        print("cnt_arr")
        print(cnt_arr)
        print()

        for x in range(self.board_arr.shape[0]):
            for y in range(self.board_arr.shape[1]):
                self.next_status(x, y, cnt_arr[x][y])
