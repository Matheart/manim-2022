from random import shuffle
from tkinter import Image
from manim import *
from gol import *

# For Chinese text
class MyText(Text):
    def __init__(self, text: str, font: str = "FZYanSongS-R-GB",  **kwargs):
        super().__init__(text = text, font = font, **kwargs)

# For English Text
class EngText(Text):
    def __init__(self, text: str, font: str = "Georgia",  **kwargs):
        super().__init__(text = text, font = font, **kwargs)

# Provide the background rectangle for the mobject when appending that to the scene 
class bgRec(BackgroundRectangle):
    def __init__(self, mobject, **kwargs):
        super().__init__(
            mobject = mobject,
            color = BLACK, 
        )
        self.scale(1.2)

# Double line under the title of intro scene of each part
class doubleLine(VGroup):
    def __init__(self, mobject, **kwargs):
        super().__init__(**kwargs)
        l1 = Line(
            color = YELLOW
        ).scale_to_fit_width(mobject.width).next_to(mobject, DOWN)

        l2 = Line(
            start = [-mobject.width/2.0,0,0], 
            end = [mobject.width/2.0,0,0], 
            color = YELLOW
        ).scale_to_fit_width(mobject.width).next_to(l1, DOWN, buff = 0.2)

        self.add(l1)
        self.add(l2)

class MyTextTest(Scene):
    def construct(self):
        normalText = Text("中文字体", color = RED).shift(UP)
        fzText     = MyText("中文字体", color = BLUE).shift(DOWN)
        self.add(normalText, fzText)

# 当谈到生命游戏时我们通常指最受欢迎的版本 -- 康威生命游戏
class FamousVersion(Scene):
    def construct(self):
        conway = ImageMobject("assets/Conway.jpg")
        magazine = ImageMobject("assets/Scientific_American.jpeg")
        conway.height = 4
        conway.shift(3 * LEFT)
        magazine.height = 5.5
        magazine.shift(3 * RIGHT + 0.5 * DOWN)

        conway.align_to(magazine, UP)

        self.play(
            FadeIn(conway, shift = RIGHT),
            FadeIn(magazine, shift = LEFT)
        )
        conwayName = EngText("John Conway").next_to(conway, DOWN)
        conwayGame = MyText("康威生命游戏").scale(1.25).to_edge(UP)

        self.play(
            FadeIn(conwayName, shift = UP),
        )
        self.wait(1)
        self.play(Write(conwayGame))
        self.wait(2)

"""
它在一个无限大的网格上进行（一个酷炫的FadeIn），每个方格有两种状态，
有生命存在或无生命存在（左上角：灰色方块，死；白色方块，活 ），
而状态的改变取决于周围八个方格的状态
康威生命游戏的规则可以简化成B3/S23（Birth 3 / Survive 23），指：
当一个死的细胞周围有三个细胞时下一代它会变成生的状态（Birth），
当一个活的细胞周围有两个或者三个细胞时下一代它会继续生存，意味着少于两个或者多于三个它下一步会死亡，这很自然的模拟了大自然中周围细胞过少或者过于拥挤导致死亡的现象。

为方便展示，我们把死去的方格标为浅蓝色
根据这个规则，正如现实生命中的演化一样，整个网格一步步的迭代，
初始状态第一代，迭代了n次就是第n代（generation）
"""
class GridRule(Scene):
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

        self.play(Create(grid), run_time = 4)
        self.wait(2)
        
        white_sq = Square(fill_color = WHITE, side_length = 0.5, fill_opacity = 1)
        grey_sq = Square(fill_color = GREY, side_length = 0.5, fill_opacity = 1)
        blue_sq = Square(fill_color = BLUE_C, side_length = 0.5, fill_opacity = 1)

        live = MyText("生:")
        no = MyText("无:")
        death = MyText("死:")

        vg = VGroup(
            live, white_sq, 
            no, grey_sq, 
        ).arrange_in_grid(2, 2).to_edge(UL)
        rect = BackgroundRectangle(vg, color = BLACK).scale(1.2)
        #vg.z_index = 10000
        #rect.z_index = 5
        
        vg = VGroup(rect, vg)
        self.play(
            FadeIn(vg)
        )
        self.wait(2)

        self.play(
            Flash(grid.get_cell(26, 24))
        )
        self.wait(1.5)
        self.play(
            Wiggle(grid.get_cell(25, 24)),
            Wiggle(grid.get_cell(27, 24)),
            Wiggle(grid.get_cell(26, 23)),
            Wiggle(grid.get_cell(26, 25)),
            Wiggle(grid.get_cell(25, 23)),
            Wiggle(grid.get_cell(25, 25)),
            Wiggle(grid.get_cell(27, 23)),
            Wiggle(grid.get_cell(27, 25)),
        )
        self.wait(2)
        rule = MyText(
            "B3/S23",
            t2c = {"B": "#00FF00", "S": ORANGE}
        ).scale(1.2).to_edge(UP)

        rule_rec = bgRec(rule)
        rule_vg = VGroup(rule_rec, rule)
        self.play(
            FadeIn(rule_rec),
            FadeIn(rule),
        )
        self.wait(2.5)
        rule_expand = MyText(
            "Birth 3 / Survive 23",
            t2c = {"Birth": "#00FF00", "Survive": ORANGE}
        ).to_edge(UP)
        expand_rec = bgRec(rule_expand)
        expand_rec.width -= 1
        expand_vg = VGroup(expand_rec, rule_expand)
        self.play(ReplacementTransform(
            rule_vg, expand_vg
        ))
        self.wait(1.5)
        # pifont
        # \ding{}
        myTemplate = TexTemplate()
        myTemplate.add_to_preamble(r"\usepackage{pifont}")

        tick = Tex(r"\ding{51}", color = "#00FF00", tex_template = myTemplate).scale(0.8) # svg
        cross = Tex(r"\ding{55}", color = BLUE_C, tex_template = myTemplate).scale(0.8) # svg

        birth_vg = VGroup(*[
            grid.get_cell(i, j)
            for i in [29, 30, 31]
            for j in [18, 19, 20]
        ])
        birth_rc = DashedVMobject(
            SurroundingRectangle(birth_vg, color = "#00FF00").scale(0.9)
        )
        # Circle(color = "#00FF00", radius = 0.1)
        birth_tick = tick.copy().move_to( grid.get_cell_center(30, 19) )
        self.play(Create(birth_rc))
        self.wait(2)
        self.play(FadeIn(birth_tick))

        dead_cross  = cross.copy().move_to( grid.get_cell_center(23, 27) )
        survive_circ = Circle(color = ORANGE, radius = 0.1).move_to( grid.get_cell_center(26, 28) )

        dead_vg = VGroup(*[
            grid.get_cell(i, j)
            for i in [22, 23, 24]
            for j in [26, 27, 28]
        ])
        dead_rc = DashedVMobject(
            SurroundingRectangle(dead_vg, color = BLUE_C).scale(0.9)
        )  

        survive_vg = VGroup(*[
            grid.get_cell(i, j)
            for i in [25, 26, 27]
            for j in [27, 28, 29]
        ])
        survive_rc = DashedVMobject(
            SurroundingRectangle(survive_vg, color = ORANGE).scale(0.9)
        )               
        
        self.wait(2)
        self.play(Create(survive_rc))
        self.play(FadeIn(survive_circ))
        self.wait(1)
        self.play(Create(dead_rc))
        self.play(FadeIn(dead_cross))
        self.wait(2)

        self.play(FadeOut(
            VGroup(
                survive_rc, dead_rc, birth_rc,
                survive_circ, dead_cross, birth_tick
            )
        ))
        self.wait(2)
        vg_dead = VGroup(
            live.copy(), white_sq.copy(), 
            no.copy(), grey_sq.copy(),
            death.copy(), blue_sq.copy()
        ).arrange_in_grid(3, 2).to_edge(UL)
        rect_dead = BackgroundRectangle(vg_dead, color = BLACK).scale(1.2)
        vg_dead = VGroup(rect_dead, vg_dead)

        self.play(ReplacementTransform(vg, vg_dead))
        self.wait(2)

        GenerationText = MyText("第1代").to_corner(DR)
        GenerationRec = bgRec(GenerationText)
        self.play(
            FadeIn(GenerationRec),
            FadeIn(GenerationText)
        )

        for i in range(50):
            grid.step()
            self.remove(GenerationText, GenerationRec)
            GenerationText = MyText("第"+str(i + 2) + "代").to_corner(DR)
            GenerationRec = bgRec(GenerationText)
            self.add(GenerationRec, GenerationText)
            self.wait(0.18)
        self.wait(2)

"""
而当中有三种最为常见，稳定结构（更常用的叫法是静物），振荡器，和飞船
静物指在每一步的迭代中一直保持不变，振荡器表示它的变化具有周期性，在固定的周期后会变回原样，飞船与振荡器类似，但不会停留在原地，而是会移动
"""
class ThreeStructures(Scene):
    def construct(self):
        still = CellBoard(
            side_length = 0.42,
            dimension = (6, 7)
        )
        still.set_stageboard_by_rle("assets/scorpion.rle")

        oscil = CellBoard(
            side_length = 0.42,
            dimension = (8, 8)
        )
        oscil.set_stageboard_by_rle("assets/octagon2.rle")

        spaceship = CellBoard(
            side_length = 0.42,
            dimension = (8, 8)
        )
        board_arr = np.zeros((8, 8), dtype  = "int64")
        board_arr[0, 1] = board_arr[1, 2] = board_arr[2, :3] = 1
        spaceship.set_stageboard(board_arr)

        vg = VGroup(still, oscil, spaceship).arrange_in_grid(1, 3, buff = 1)
        
        still_text = MyText("静物").next_to(still, DOWN)
        oscil_text = MyText("振荡器").next_to(oscil, DOWN)
        spaceship_text = MyText("飞船").next_to(spaceship, DOWN)
        still_text.align_to(oscil_text, DOWN)

        reminder_text = MyText("*在上期视频我们把静物称为稳定结构").scale(0.4).to_corner(UR)
        self.play(Create(vg))

        self.play(FadeIn(still_text, shift = UP), FadeIn(reminder_text))
        self.play(FadeIn(oscil_text, shift = UP))
        self.play(FadeIn(spaceship_text, shift = UP))
        self.wait(2)
        for _ in range(15):
            oscil.step()
            self.wait(0.15)
        self.wait(2)
        arrow = Arrow(
            spaceship.get_cell_center(2, 2),
            spaceship.get_cell_center(7, 7),
            color = "#8A2BE2",
            stroke_width = 10
        )
        self.play(GrowArrow(arrow))
        for i in range(20):
            spaceship.step()
            self.wait(0.2)
        self.wait(2)

        """
        self.play(FadeIn(still_text, shift = UP))
        self.wait(3)
        self.play(FadeIn(oscil_text, shift = UP))
        self.wait()
        for _ in range(10):
            oscil.step()
            self.wait(0.2)
        self.wait(1)
        self.play(FadeIn(spaceship_text, shift = UP))
        for _ in range(15):
            spaceship.step()
            self.wait(0.15)
        self.wait(3)
        """
"""
我们会在接下来的几集会更加详细的介绍以上结构的性质（BulletedList），
而这期我们会介绍静物的枚举，构造，和用途，那，让我们开始吧！
"""
class FollowingSeries(Scene):
    def construct(self):
        list = VGroup(
            MyText("第一集：生命游戏介绍"),
            MyText("第二集：静物的枚举，构造与用途"),
            MyText("第三集：振荡器的构造，性质与用途"),
            MyText("第四集：飞船的构造，性质与用途"),
            EngText("...")
        ).arrange_in_grid(5, 1)
        list.set_color(YELLOW)
        for i in range(5):
            if i == 1:
                continue
            list[i].align_to(list[1], LEFT)
        list[4].shift(0.2 * DOWN)
        list.shift(0.3 * RIGHT)

        dots = VGroup()
        for i in range(5):
            dots.add(
                Dot(color = YELLOW).scale(2).next_to(list[i], LEFT)
            )
        self.add(list, dots)
        self.wait(3)

        self.play(
            VGroup(list[0],list[2],list[3],list[4]).animate.set_opacity(0.2),
            VGroup(dots[0],dots[2],dots[3],dots[4]).animate.set_opacity(0.2)
        )
        self.wait(5)

# 在上一期视频中我们只展示了几个静物，但是还有非常多的静物没有展示出来
class DisplayStill(Scene):
    def construct(self):
        text = MyText("静物的枚举", color = YELLOW).scale(2.5)
        self.play(Write(text))

        dl = doubleLine(text)
        self.play(Create(dl), run_time = 0.5)
        self.wait(2)

        text.target = MyText("静物的枚举", color = YELLOW).scale(1.3).to_edge(UP)
        dll = doubleLine(text.target).stretch_to_fit_width(16)
        dll[1].shift(0.05 * UP)
        self.play(
            MoveToTarget(text),
            ReplacementTransform(dl, dll)
        )
        self.wait(2)

        # Block 方块
        Block_set = np.zeros((9, 9))
        Block_set[3][4] = Block_set[3][5] = 1
        Block_set[4][4] = Block_set[4][5] = 1
        BlockCell = CellBoard(
            dimension = (9, 9)
        ).scale(0.5)
        BlockCell.set_stageboard(Block_set)

        # Boat 小船
        Boat_set = np.zeros((5, 5))
        Boat_set[1][2] = Boat_set[2][1] = Boat_set[2][3] = 1
        Boat_set[3][2] = Boat_set[3][3] = 1

        BoatCell = CellBoard(
            dimension = (5, 5),
        ).scale(0.9)
        BoatCell.set_stageboard(Boat_set)

        # Dead spark coil 熄灭的火花线圈
        Coil_set = np.zeros((9, 9))
        Coil_set[2][1] = Coil_set[2][2] = Coil_set[2][6] = Coil_set[2][7] = 1
        Coil_set[3][1] = Coil_set[3][3] = Coil_set[3][5] = Coil_set[3][7] = 1
        Coil_set[4][3] = Coil_set[4][5] = 1
        Coil_set[5][1] = Coil_set[5][3] = Coil_set[5][5] = Coil_set[5][7] = 1
        Coil_set[6][1] = Coil_set[6][2] = Coil_set[6][6] = Coil_set[6][7] = 1

        CoilCell = CellBoard(
            dimension = (9, 9),
        ).scale(0.5)
        CoilCell.set_stageboard(Coil_set)

        # Cis-mirrored worm (触角)
        Worm_set = np.zeros((9, 9))
        Worm_set[0][2:4] = 1
        Worm_set[1][1] = Worm_set[1][3] = 1
        Worm_set[2][1] = Worm_set[2][6] = 1
        Worm_set[3][2:7] = Worm_set[5][2:7] = 1
        Worm_set[6][1] = Worm_set[6][6] = 1
        Worm_set[7][1] = Worm_set[7][3] = 1
        Worm_set[8][2:4] = 1

        WormCell = CellBoard(
            dimension = (9, 9),
        ).scale(0.5)
        WormCell.set_stageboard(Worm_set)

        # Inflected clips (弯曲的回形针)
        Clip_set = np.zeros((9, 9))
        Clip_set[0][2] = Clip_set[0][6] = 1
        Clip_set[1][1] = Clip_set[1][3] = Clip_set[1][5] = Clip_set[1][7] = 1
        Clip_set[2][0] = Clip_set[2][3] = Clip_set[2][5] = Clip_set[2][8] = 1
        Clip_set[3][0] = Clip_set[3][1] = Clip_set[3][3] = Clip_set[3][5] = Clip_set[3][7] = Clip_set[3][8] = 1
        Clip_set[4][3] = Clip_set[4][5] = 1
        Clip_set[5][0] = Clip_set[5][1] = Clip_set[5][3] = Clip_set[5][5] = Clip_set[5][7] = Clip_set[5][8] = 1
        Clip_set[6][0] = Clip_set[6][3] = Clip_set[6][5] = Clip_set[6][8] = 1
        Clip_set[7][1] = Clip_set[7][2] = Clip_set[7][6] = Clip_set[7][7] = 1

        ClipCell = CellBoard(
            dimension = (9, 9),
        ).scale(0.5)
        ClipCell.set_stageboard(Clip_set)

        BlockCell.scale_to_fit_height(CoilCell.height)

        cell_vg = VGroup(
            BlockCell, CoilCell, WormCell, ClipCell
        ).arrange_in_grid(1, 4, buff = 0.7)

        BlockName = MyText("方块").scale(0.6).next_to(BlockCell, DOWN)
        CoilName = MyText("熄灭的火花线圈").scale(0.6).next_to(CoilCell, DOWN).align_to(BlockName, DOWN)
        WormName = MyText("触角").scale(0.6).next_to(WormCell, DOWN).align_to(BlockName, DOWN)
        ClipName = MyText("弯曲的回形针").next_to(ClipCell, DOWN).scale(0.6).align_to(BlockName, DOWN)

        text_vg = VGroup(BlockName, CoilName, WormName, ClipName)

        self.play(Create(cell_vg))
        self.play(
            FadeIn(text_vg, shift = UP)
        )
        self.wait(4)

# 如果想枚举的话，最自然的方式就是按细胞数量枚举，但是目前会遇到一个问题
class EnumerProb(Scene):
    def construct(self):
        text = MyText("静物的枚举", color = YELLOW).scale(1.3).to_edge(UP)
        dl   = doubleLine(text).stretch_to_fit_width(16)
        dl[1].shift(0.05 * UP)
        
        self.add(text, dl)

        #------------ Cell object ------------#
        boat = CellBoard(
            side_length = 0.5, 
            dimension = (3, 3)
        )
        boat.set_stageboard(
            expand_rle("assets/boat.rle")[::-1,::]
        )
        boat.scale_to_fit_height(0.85)

        snake = CellBoard(
            side_length = 0.4, 
            dimension = (2, 4)
        )
        snake.set_stageboard(
            expand_rle("assets/snake.rle")[::-1, ::]
        )
        snake.scale_to_fit_height(0.63)

        pond = CellBoard(
            side_length = 0.4, 
            dimension = (4, 4)
        )
        pond.set_stageboard(
            expand_rle("assets/pond.rle")
        )
        pond.scale_to_fit_height(1.3)
        #------------------------------------------#

        fst = ["0", "...", "5", "...", "?"]
        snd = [
            EngText("SSS", color = BLACK).scale(0.65), 
            EngText("SSS", color = BLACK).scale(0.65), 
            snake, 
            EngText("SSS", color = BLACK).scale(0.65), 
            pond
        ]

        lst = [
            [MyText(fst[i]).scale(0.8), snd[i]] 
            for i in range(5)
        ]
        row_labels = [
            MyText(i).scale(0.8) for i in
            ["1", "...", "6",  "...", "8"]
        ]

        table = MobjectTable(
            lst,
            row_labels = row_labels,
            col_labels = [MyText("#静物个数").scale(0.8), MyText("例子").scale(0.8)],
            v_buff = 0.37,
            top_left_entry = MyText("#细胞个数").scale(0.8)
        ).scale(0.9).shift(0.5 * DOWN + 0.22 * LEFT)

        self.play(
            FadeIn(table)
        )
        self.wait(2.5)
        self.play(
            FadeIn(Cross(table))
        )
        self.wait(2)

        #rtable = 

# 当我们列举到细胞数为8个的时候，我们能摆两个方块，随便摆放任何位置都可以，那就会有无限种情况
class BlockRandomPosition(Scene):
    def construct(self):
        text = MyText("静物的枚举", color = YELLOW).scale(1.3).to_edge(UP)
        text_transform = MyText("静物的枚举 - 严格静物", color = YELLOW).scale(1.3).to_edge(UP)
        dl   = doubleLine(text).stretch_to_fit_width(16)
        dl[1].shift(0.05 * UP)
        
        self.add(text, dl)

        board = CellBoard(
            side_length = 0.4, 
            dimension = (10, 10)
        ).scale(0.95).shift(0.6 * DOWN)

        def get_block(start_x, start_y):
            return VGroup(
                board.get_cell(start_x, start_y),
                board.get_cell(start_x + 1, start_y),
                board.get_cell(start_x, start_y + 1),
                board.get_cell(start_x + 1, start_y + 1),
            )
        self.add(board)

        self.play(
            get_block(3, 3).animate.set_color(WHITE),
            get_block(7, 7).animate.set_color(WHITE),
        )
        self.wait(2)

        self.play(
            get_block(3, 3).animate.set_color(RED),
            get_block(7, 7).animate.set_color(BLUE),
        )

        self.play(
            get_block(3, 3).animate.set_color(GREY),
            get_block(7, 7).animate.set_color(GREY),
            get_block(2, 6).animate.set_color(RED),
            get_block(8, 3).animate.set_color(BLUE),
        )
        self.wait(1)
        self.play(
            get_block(2, 6).animate.set_color(GREY),
            get_block(8, 3).animate.set_color(GREY),
            get_block(4, 2).animate.set_color(RED),
            get_block(4, 7).animate.set_color(BLUE),
        )
        self.wait(1)
        self.play(
            get_block(4, 2).animate.set_color(GREY),
            get_block(4, 7).animate.set_color(GREY),
            get_block(2, 2).animate.set_color(RED),
            get_block(8, 5).animate.set_color(BLUE),
        )
        self.wait(3)

"""
于是我们进一步定义 严格静物 (strict still life) ：
1. 若一个静物本身就连在一块（用术语讲是联通的话），那它就是严格静物
beehive
2. 若一个静物由几块组成，也就是非联通的，而去掉一块或多块会让它变成非静物的话，那它就是严格静物
mirrored table
"""
class StrictStillLife(Scene):
    def construct(self):
        text = MyText("静物的枚举", color = YELLOW).scale(1.3).to_edge(UP)
        text_transform = MyText("静物的枚举 - 严格静物", color = YELLOW).scale(1.3).to_edge(UP)        
        dl   = doubleLine(text).stretch_to_fit_width(16)
        dl[1].shift(0.05 * UP)
        
        self.add(text, dl)

        # beehive
        beehive = CellBoard(
            dimension = (3, 4)
        )
        beehive.set_stageboard_by_rle("assets/beehive.rle")

        # mirror table
        mirror = CellBoard(
            dimension = (4, 5)
        )
        mirror.set_stageboard_by_rle("assets/mirroredtable.rle")

        rule_vg = VGroup(beehive, mirror)
        rule_vg.arrange_in_grid(1, 2, buff = 2)
        rule_vg.shift(0.5 * DOWN)

        #beehive.scale_to_fit_height(mirror.height)

        col = ORANGE
        beehive_connect_segment = VGroup(
            Line(
                beehive.get_cell_center(1, 2),
                beehive.get_cell_center(1, 3),
                color = col
            ),

            Line(
                beehive.get_cell_center(1, 3),
                beehive.get_cell_center(2, 4),
                color = col
            ),

            Line(
                beehive.get_cell_center(2, 4),
                beehive.get_cell_center(3, 3),
                color = col
            ),

            Line(
                beehive.get_cell_center(3, 3),
                beehive.get_cell_center(3, 2),
                color = col
            ),

            Line(
                beehive.get_cell_center(3, 2),
                beehive.get_cell_center(2, 1),
                color = col
            ),

            Line(
                beehive.get_cell_center(2, 1),
                beehive.get_cell_center(1, 2),
                color = col
            ),
        )
        ptsL = [[1,1],[1,2],[2,2],[3,2],[4,2],[4,1]]
        mirror_connected_segmentL = VGroup()
        mirror_connected_segmentR = VGroup()
        for i in range(1, len(ptsL)):
            # i-1, i
            mirror_connected_segmentL.add(
                Line(
                    mirror.get_cell_center(ptsL[i-1][0], ptsL[i-1][1]),
                    mirror.get_cell_center(ptsL[i][0], ptsL[i][1]),
                    color = RED
                )
            )

            mirror_connected_segmentR.add(
                Line(
                    mirror.get_cell_center(ptsL[i-1][0], 6 - ptsL[i-1][1]),
                    mirror.get_cell_center(ptsL[i][0], 6 - ptsL[i][1]),
                    color = BLUE
                )
            )
        self.wait(1)
        self.play(ReplacementTransform(text, text_transform))
        self.wait(2.5)
        self.play(Create(rule_vg))
        self.wait(1)
        self.play(Create(beehive_connect_segment))
        self.wait(1)
        self.play(Uncreate(beehive_connect_segment))
        self.wait(2)
        self.play(
            Create(mirror_connected_segmentL),
            Create(mirror_connected_segmentR)
        )
        self.wait(1.5)
        mirror.target = mirror.copy().move_to(0.5 * DOWN).scale(1.5)
        self.play(
            FadeOut(beehive),
            FadeOut(mirror_connected_segmentL),
            FadeOut(mirror_connected_segmentR),
            MoveToTarget(mirror)
        )
        animation_list = []
        for i in ptsL:
            animation_list.append(
                mirror.get_cell(i[0], 6 - i[1]).animate.set_color(GREY)
            )
        self.play(AnimationGroup(*animation_list))

        ear_unstable = CellBoard(
            side_length = 0.4,
            dimension = (11, 11)
        ).scale(0.9).shift(0.6 * DOWN)
        arr = np.zeros((11, 11))
        arr[3][4] = arr[3][5] = arr[4][5] = arr[5][5] = arr[6][5] = arr[6][4] = 1 
        ear_unstable.set_stageboard(arr)

        self.play(ReplacementTransform(mirror, ear_unstable))
        self.play(ear_unstable.animate.shift(4 * LEFT))

        arrow = Arrow(start = 1.2 * LEFT, end = 1.2 * RIGHT, stroke_width = 13).shift(0.8 * DOWN)
        notStill = MyText("不是静物").scale(0.65).next_to(arrow, UP).shift(0.2 * DOWN + 0.1 * LEFT)

        ear_unstable_copy = ear_unstable.copy()
        self.play(
            GrowArrow(arrow),
            ear_unstable_copy.animate.shift(8 * RIGHT)
        )
    
        for i in range(15):
            ear_unstable_copy.step()
            self.wait(0.15)

        self.play(Write(notStill))
        self.wait(2)

"""
举例子：
如图所示有三个静物，
第一个（beehive with tail）看起来好像是两块构成，但其实整一个是连通的，所以是严格静物
第二个（aircraft carrier）去掉上面的部分后剩下的部分不是静物，所以它是严格静物
第三个同理（block on table）
"""
class StrictExample(Scene):
    def construct(self):
        text = MyText("静物的枚举 - 严格静物例子", color = YELLOW).scale(1.3).to_edge(UP)        
        dl   = doubleLine(text).stretch_to_fit_width(16)
        dl[1].shift(0.05 * UP)
        
        self.add(text, dl)

        #--- gol objects --#
        beehive_with_tail = CellBoard(
            dimension = (5, 6)
        )
        beehive_with_tail.set_stageboard_by_rle("assets/beehivewithtail.rle")

        carrier = CellBoard(
            dimension = (3, 4)
        )
        carrier.set_stageboard_by_rle("assets/aircraftcarrier.rle")

        block_on_table = CellBoard(
            dimension = (5, 4)
        )
        block_on_table.set_stageboard_by_rle("assets/blockontable.rle")

        life_vg = VGroup(beehive_with_tail, carrier, block_on_table).arrange_in_grid(1, 3, buff = 1.2).shift(0.8 * DOWN)

        #------------------#
        self.play(Create(life_vg))
        self.wait(2)

        blue_list = [
            [1,2],[1,3],[2,4],[3,3],[3,2],[2,1],
        ]

        red_list = [
            [3,5], [4,5],[5,5],[5,6]
        ]

        blue_vg = VGroup()
        red_vg = VGroup()
        for i in blue_list:
            blue_vg.add(
                beehive_with_tail.get_cell(i[0], i[1])
            )
        for j in red_list:
            red_vg.add(
                beehive_with_tail.get_cell(j[0], j[1])
            )

        self.play(blue_vg.animate.set_color(BLUE), red_vg.animate.set_color(RED))
        self.wait(2)
        self.play(blue_vg.animate.set_color(WHITE), red_vg.animate.set_color(WHITE))

        segment = VGroup()
        for i in range(1, len(blue_vg)):
            # i-1, i
            segment.add(
                Line(
                    blue_vg[i-1].get_center(),
                    blue_vg[i].get_center(),
                    color = GOLD
                )
            )
        segment.add(
            Line(
                beehive_with_tail.get_cell_center(2, 1),
                beehive_with_tail.get_cell_center(1, 2),
                color = GOLD
            )
        )

        for i in range(1, len(red_vg)):
            # i-1, i
            segment.add(
                Line(
                    red_vg[i-1].get_center(),
                    red_vg[i].get_center(),
                    color = GOLD
                )
            )
        segment.add(
            Line(
                beehive_with_tail.get_cell_center(2, 4),
                beehive_with_tail.get_cell_center(3, 5),
                color = GOLD
            )
        )

        self.play(Create(segment))
        self.wait(2)

        myTemplate = TexTemplate()
        myTemplate.add_to_preamble(r"\usepackage{pifont}")
        tick = Tex(r"\ding{51}", color = GREEN, tex_template = myTemplate).scale(1.5)
        
        tick1 = tick.copy().next_to(beehive_with_tail, DOWN)
        tick2 = tick.copy().next_to(carrier, DOWN)
        tick3 = tick.copy().next_to(block_on_table, DOWN)

        self.play(FadeOut(segment), FadeIn(tick1, shift = UP))
        self.wait(2.5)

        self.play(
            carrier.get_cell(1, 1).animate.set_color(GREY),
            carrier.get_cell(1, 2).animate.set_color(GREY),
            carrier.get_cell(2, 1).animate.set_color(GREY)
        )
        self.wait(2)
        self.play(
            carrier.get_cell(1, 1).animate.set_color(WHITE),
            carrier.get_cell(1, 2).animate.set_color(WHITE),
            carrier.get_cell(2, 1).animate.set_color(WHITE)
        )      
        self.wait()
        self.play(FadeIn(tick2, shift = UP))
        self.wait(1.5)
        self.play(
            block_on_table.get_cell(1, 3).animate.set_color(GREY),
            block_on_table.get_cell(1, 4).animate.set_color(GREY),
            block_on_table.get_cell(2, 3).animate.set_color(GREY),
            block_on_table.get_cell(2, 4).animate.set_color(GREY),
        )        
        self.wait(1)
        self.play(
            block_on_table.get_cell(1, 3).animate.set_color(WHITE),
            block_on_table.get_cell(1, 4).animate.set_color(WHITE),
            block_on_table.get_cell(2, 3).animate.set_color(WHITE),
            block_on_table.get_cell(2, 4).animate.set_color(WHITE),
        )      
        self.play(FadeIn(tick3, shift = UP))   
        self.wait(2)       

"""
按这个定义，刚才由两个方块组成的静物就被排除在严格静物之外了
右边的静物由四个蜂窝构成，被叫做蜂蜜农场（是不是很形象），
同理也不是严格静物，因为移去任意一个或多个,整体还是静物
"""
class NonstrictExample(Scene):
    def construct(self):
        text = MyText("静物的枚举 - 非严格静物例子", color = YELLOW).scale(1.3).to_edge(UP)        
        dl   = doubleLine(text).stretch_to_fit_width(16)
        dl[1].shift(0.05 * UP)
        
        self.add(text, dl)

        board = CellBoard(
            side_length = 0.4, 
            dimension = (10, 10)
        ).scale(0.8).shift(0.8 * DOWN + 3.5 * LEFT)

        def get_block(start_x, start_y):
            return VGroup(
                board.get_cell(start_x, start_y),
                board.get_cell(start_x + 1, start_y),
                board.get_cell(start_x, start_y + 1),
                board.get_cell(start_x + 1, start_y + 1),
            )
        get_block(3, 3).set_color(WHITE)
        get_block(7, 7).set_color(WHITE)

        farm = CellBoard(
            side_length = 0.4,
            dimension = (13, 13)
        ).scale(0.8).shift(0.8 * DOWN + 3.5 * RIGHT)
        farm.set_stageboard_by_rle("assets/honeyfarm.rle")

        self.add(board, farm)
        self.wait(8)

"""
于是我们现在能直接枚举严格静物了：p35 table
可以看到严格静物的数量随细胞数增加增长的很快，
当细胞数为二十三的时候已经有将近一百六十多万个静物
"""
class DirectEnum(Scene):
    def construct(self):
        text = MyText("静物的枚举", color = YELLOW).scale(1.3).to_edge(UP)        
        dl   = doubleLine(text).stretch_to_fit_width(16)
        dl[1].shift(0.05 * UP)
        
        self.add(text, dl)

        img1 = ImageMobject("assets/strictEnum1.png").scale(0.7).to_corner(UL).shift(1.5 * DOWN + RIGHT)
        img2 = ImageMobject("assets/strictEnum2.png")
        img2.scale_to_fit_height(img1.height)
        img2.to_corner(UR).shift(1.5 * DOWN + LEFT)
        self.play(FadeIn(img1, shift = UP), FadeIn(img2, shift = UP))
        self.wait(4)

"""
最简单的构造方法就是直接延长一些生命的结构：
比如
boat可以延长中间的结构, long boat, long long boat, ...
snake也可以延长中间的结构，
记法很简单，每延长一次就多一个long，延长n次就是n个long或者简写成long^n次方
也可用以下两种记法：very^(n-1) long = extra^(n-2) long
"""
class ConstructSimple(Scene):
    def construct(self):
        text = MyText("静物的构造", color = YELLOW).scale(2.5)
        self.play(Write(text))

        dl = doubleLine(text)
        self.play(Create(dl), run_time = 0.5)
        self.wait(2)

        text.target = MyText("静物的构造", color = YELLOW).scale(1.3).to_edge(UP)
        dll = doubleLine(text.target).stretch_to_fit_width(16)
        dll[1].shift(0.05 * UP)
        self.play(
            MoveToTarget(text),
            ReplacementTransform(dl, dll)
        )
        self.wait(2)
        boat1 = CellBoard(
            side_length = 0.5, 
            dimension = (3, 3)
        )
        boat1.set_stageboard(
            expand_rle("assets/boat.rle")[::-1,::]
        )

        boat2 = CellBoard(
            side_length = 0.5, 
            dimension = (4, 4)
        )
        boat2.set_stageboard(
            expand_rle("assets/longboat.rle")[::,::-1]
        )

        boat3 = CellBoard(
            side_length = 0.5, 
            dimension = (5, 5)
        )
        boat3.set_stageboard(
            expand_rle("assets/verylongboat.rle")[::,::-1]
        )

        boat4 = CellBoard(
            side_length = 0.5, 
            dimension = (6, 6)
        )
        boat4.set_stageboard_by_rle("assets/long3boat.rle")

        boat_vg = VGroup(boat1, boat2, boat3, boat4).arrange_in_grid(
            1, 4, buff = 0.65
        )
        boat1.align_to(boat4, DOWN)
        boat2.align_to(boat4, DOWN)
        boat3.align_to(boat4, DOWN)

        boat1_text = EngText("boat").scale(0.65).next_to(boat1, DOWN)
        boat2_text = EngText("long boat").scale(0.65).next_to(boat2, DOWN)
        boat3_text = EngText("long long boat").scale(0.65).next_to(boat3, DOWN)
        boat4_text = EngText("long^3 boat").scale(0.65).next_to(boat4, DOWN)

        self.add(boat1, boat1_text)
        self.wait(2)
        self.play(
            Create(boat2),
            Create(boat3),
            Create(boat4)
        )
        self.play(
            FadeIn(boat2_text, shift = UP),
            FadeIn(boat3_text, shift = UP),
            FadeIn(boat4_text, shift = UP)
        )
        self.wait(1.5)

        self.play(
            boat1.get_cell(1, 2).animate.set_color(LIGHT_PINK),
            boat1.get_cell(2, 3).animate.set_color(LIGHT_PINK),
            boat2.get_cell(1, 3).animate.set_color(LIGHT_PINK),
            boat2.get_cell(2, 2).animate.set_color(LIGHT_PINK),
            boat2.get_cell(2, 4).animate.set_color(LIGHT_PINK),
            boat2.get_cell(3, 3).animate.set_color(LIGHT_PINK),
            boat3.get_cell(1, 4).animate.set_color(LIGHT_PINK),
            boat3.get_cell(2, 3).animate.set_color(LIGHT_PINK),
            boat3.get_cell(3, 2).animate.set_color(LIGHT_PINK),
            boat3.get_cell(2, 5).animate.set_color(LIGHT_PINK),
            boat3.get_cell(3, 4).animate.set_color(LIGHT_PINK),
            boat3.get_cell(4, 3).animate.set_color(LIGHT_PINK),
            
            boat4.get_cell(1, 5).animate.set_color(LIGHT_PINK),
            boat4.get_cell(2, 4).animate.set_color(LIGHT_PINK),
            boat4.get_cell(3, 3).animate.set_color(LIGHT_PINK),
            boat4.get_cell(4, 2).animate.set_color(LIGHT_PINK),
            boat4.get_cell(2, 6).animate.set_color(LIGHT_PINK),
            boat4.get_cell(3, 5).animate.set_color(LIGHT_PINK),
            boat4.get_cell(4, 4).animate.set_color(LIGHT_PINK),
            boat4.get_cell(5, 3).animate.set_color(LIGHT_PINK),
        )
        self.wait(1)
        self.play(Uncreate(VGroup(boat_vg, boat1_text, boat2_text, boat3_text, boat4_text)))

        snake1 = CellBoard(
            side_length = 0.4, 
            dimension = (2, 4)
        )
        snake1.set_stageboard(
            expand_rle("assets/snake.rle")[::-1, ::]
        )

        snake2 = CellBoard(
            side_length = 0.4, 
            dimension = (3, 5)
        )
        snake2.set_stageboard(
            expand_rle("assets/longsnake.rle")[::,::-1]
        )

        snake3 = CellBoard(
            side_length = 0.4, 
            dimension = (4, 6)
        )
        snake3.set_stageboard(
            expand_rle("assets/verylongsnake.rle")[::,::-1]
        )
        
        snake_dot = MathTex(r"\cdots")
        snake4 = CellBoard(
            side_length = 0.37, 
            dimension = (10, 8)
        )
        
        snake4.set_stageboard(
            expand_rle("assets/long6snake.rle")[::-1, ::]
        )

        snake_vg = VGroup(
            snake1, snake2, snake3, snake_dot, snake4
        ).arrange_in_grid(1, 5, buff = 0.55)
        snake1.align_to(snake4, DOWN)
        snake2.align_to(snake4, DOWN)
        snake3.align_to(snake4, DOWN)
        snake_dot.align_to(snake4, DOWN)
        snake_vg.shift(0.1 * DOWN)

        snake1_text = EngText("snake").scale(0.65).next_to(snake1, DOWN)
        snake2_text = EngText("long snake").scale(0.65).next_to(snake2, DOWN)
        snake3_text = EngText("long long snake").scale(0.65).next_to(snake3, DOWN)
        snake4_text = EngText("long^n snake").scale(0.65).next_to(snake4, DOWN)
        snake4_text2 = EngText("very^(n-1) long snake", color = GOLD_C).scale(0.65).next_to(snake4, DOWN)
        snake4_text3 = EngText("extra^(n-2) long snake", color = YELLOW_E).scale(0.65).next_to(snake4, DOWN)
        
        self.wait(2)
        self.play(Create(snake_vg))
        self.play(
            FadeIn(
                VGroup(snake1_text, snake2_text, snake3_text, snake4_text),
                shift = UP
            )
        )
        self.wait(2)
        self.play(Wiggle(snake2_text))
        self.wait(1)
        self.play(Wiggle(snake3_text))
        self.wait(3)
        self.play(Wiggle(snake4_text))
        self.wait(2)
        self.play(
            FadeOut(snake4_text, shift = UP),
            FadeIn(snake4_text2, shift = UP),
        )
        self.wait(1)
        self.play(
            FadeOut(snake4_text2, shift = UP),
            FadeIn(snake4_text3, shift = UP),
        )
        self.wait(2) 

# 如这个long long long snake可以叫做very very long snake也可以叫做extra long snake
class EquivNotation(Scene):
    def construct(self):
        text = MyText("静物的构造", color = YELLOW).scale(1.3).to_edge(UP)
        dl   = doubleLine(text).stretch_to_fit_width(16)
        dl[1].shift(0.05 * UP)
        
        self.add(text, dl)

        snake3 = CellBoard(
            side_length = 0.4, 
            dimension = (5, 7)
        ).scale(1.5)
        snake3.set_stageboard(
            expand_rle("assets/long3snake.rle")[::,::-1]
        )

        text1 = EngText("long^3 snake").scale(1.1).next_to(snake3, DOWN)
        text2 = EngText("very very long snake").scale(1.1).next_to(snake3, DOWN)
        text3 = EngText("extra long snake").scale(1.1).next_to(snake3, DOWN)

        self.add(snake3, text1)

        self.wait(1)
        self.play(ReplacementTransform(text1, text2))
        self.wait(1)
        self.play(ReplacementTransform(text2, text3)) 
        self.wait(3)       

# 静物有一个特点，就是不会有“厚”的部分
class NoThick(Scene):
    def construct(self):
        text = MyText("静物的构造", color = YELLOW).scale(1.3).to_edge(UP)
        dl   = doubleLine(text).stretch_to_fit_width(16)
        dl[1].shift(0.05 * UP)
        
        self.add(text, dl)

        thickLife = CellBoard(
            dimension = (8, 8)
        )
        thickLife.set_stageboard_by_rle("assets/thick.rle")

        thickLife.shift(DOWN)

        self.add(thickLife)
        self.wait(2.5)

        cross = Cross(thickLife)
        self.play(Create(cross))
        self.wait(2)

"""
对于静物里的方块，
我们知道里面每个细胞周围都已经有三个活着的细胞，
所以我们可以断定方块周围一圈都没有细胞，
否则方块里就会有细胞因过于拥挤在下一代死亡，违反静物的定义
"""
class StillBlock(Scene):
    def construct(self):
        text = MyText("静物的构造", color = YELLOW).scale(1.3).to_edge(UP)
        dl   = doubleLine(text).stretch_to_fit_width(16)
        dl[1].shift(0.05 * UP)
        
        self.add(text, dl)

        block = CellBoard(
            side_length = 0.6,
            dimension = (4, 4)
        )
        arr = np.zeros((4, 4))
        arr[1:3, 1:3] = 1
        block.set_stageboard(arr)
        self.play(Create(block))

        question_vg = VGroup()
        for i in range(1, 5):
            for j in range(1, 5):
                if i == 1 or i == 4 or j == 1 or j == 4:
                    mark = Text("?", color = WHITE, fill_opacity = 10).scale(0.9).move_to(
                        block.get_cell_center(i, j)
                    )
                    question_vg.add(mark)

        self.wait(1.5)

        myTemplate = TexTemplate()
        myTemplate.add_to_preamble(r"\usepackage{pifont}")

        tick = Tex(r"\ding{51}", color = "#8A2BE2", tex_template = myTemplate).scale(0.8) # svg

        block_vg1 = VGroup(*[
            block.get_cell(i, j)
            for i in [1, 2, 3]
            for j in [1, 2, 3]            
        ])

        rec1 = DashedVMobject(
            SurroundingRectangle(block_vg1, color = "#8A2BE2").scale(0.95),
            num_dashes = 30
        )

        tick1 = VGroup(*[
            tick.copy().move_to(block.get_cell_center(i, j))
            for i, j in [[2,3],[3,2],[3,3]]
        ]) 
        
        self.play(
            FadeIn(rec1), FadeIn(tick1)
        )

        block_vg2 = VGroup(*[
            block.get_cell(i, j)
            for i in [1, 2, 3]
            for j in [2, 3, 4]            
        ])

        rec2 = DashedVMobject(
            SurroundingRectangle(block_vg2, color = "#8A2BE2").scale(0.95),
            num_dashes = 30
        )

        tick2 = VGroup(*[
            tick.copy().move_to(block.get_cell_center(i, j))
            for i, j in [[2,2],[3,3],[3,2]]
        ]) 

        self.play(
            FadeOut(rec1), FadeOut(tick1),
            FadeIn(rec2), FadeIn(tick2)
        )
        self.wait(1.5)
        self.play(
            FadeOut(rec2), FadeOut(tick2)
        )
        self.wait(3)
 
        """
        self.wait(1)
        self.play(FadeOut(rec))
        self.wait(2)
        """

        """
        self.play(FadeOut(question_vg))
        self.wait(2)
        """

"""
所以像刚才展示的一样，存在方块周围有细胞，所以它不是静物
"""
class StillThick(Scene):
    def construct(self):
        text = MyText("静物的构造", color = YELLOW).scale(1.3).to_edge(UP)
        dl   = doubleLine(text).stretch_to_fit_width(16)
        dl[1].shift(0.05 * UP)
        
        self.add(text, dl)

        thickLife = CellBoard(
            dimension = (8, 8)
        ).scale(0.9)
        thickLife.set_stageboard_by_rle("assets/thick.rle")
        thickLife2 = thickLife.copy()
        thickLife2.step()

        thickLife.shift(4 * LEFT + 0.3 * DOWN)
        thickLife2.shift(4 * RIGHT + 0.3 * DOWN)

        arr = Arrow(1.5 * LEFT, 1.5 * RIGHT, color = RED, stroke_width = 17).shift(0.3 * DOWN)
        notStill = MyText("非静物", color = ORANGE).scale(0.9).next_to(thickLife, DOWN)
        text = MyText("下一代", color = RED).scale(0.9).next_to(arr, DOWN).shift(0.15 * LEFT + 0.2 * UP)

        def get_block(start_x, start_y):
            return VGroup(
                thickLife.get_cell(start_x, start_y),
                thickLife.get_cell(start_x + 1, start_y),
                thickLife.get_cell(start_x, start_y + 1),
                thickLife.get_cell(start_x + 1, start_y + 1),
            )
        blk = get_block(6, 2)

        rec = DashedVMobject(SurroundingRectangle(
            VGroup(*[
                thickLife.get_cell(i, j)
                for i in [5,6,7,8]
                for j in [1,2,3,4]
            ]),
            color = "#00FF00",
        ), num_dashes = 30).scale(0.95)

        self.add(thickLife)
        self.wait(1)
        self.play(Create(rec))

        circ_vg = VGroup(*[
            Circle(radius = 0.1, color = "#00FF00").move_to(
                thickLife.get_cell_center(i, j)
            )
            for i, j in [[5,3],[5,4],[6,4],[8,1],[8,2],[8,3]]
        ])
        self.play(FadeIn(circ_vg))
        self.play(GrowArrow(arr), Transform(thickLife.copy(), thickLife2))
        self.wait(1)
        self.play(FadeIn(text))
        self.wait(1)
        self.play(FadeIn(notStill, shift = UP))
        self.wait(2)

# 所以静物只可能由单个细胞厚的线和方块构成
class ConsistSingle(Scene):
    def construct(self):
        text = MyText("静物的构造", color = YELLOW).scale(1.3).to_edge(UP)
        dl   = doubleLine(text).stretch_to_fit_width(16)
        dl[1].shift(0.05 * UP)
        
        self.add(text, dl)
        #singleLife1 10 * 10
        #singleLife2 10 * 10
        #singleLife3 10 * 10

        singleLife1 = CellBoard(
            dimension = (5, 7)
        )
        singleLife1.set_stageboard_by_rle("assets/carriersiameseeaterhead.rle")

        singleLife2 = CellBoard(
            dimension = (6, 5)
        )
        singleLife2.set_stageboard_by_rle("assets/cisblockonlongbookend.rle")

        singleLife3 = CellBoard(
            dimension = (6, 4)
        )
        singleLife3.set_stageboard_by_rle("assets/longintegral.rle")

        life = VGroup(singleLife1, singleLife2, singleLife3).shift(0.3 * DOWN).arrange_in_grid(1, 3, buff = 1.2)
        self.add(life)
        self.wait(5)

# 但反过来说，有些单个细胞厚的线本身未必是静物，大部分情况我们可以在它旁边加一些物体来稳定它
class MayNotStill(Scene):
    def construct(self):
        text = MyText("静物的构造", color = YELLOW).scale(1.3).to_edge(UP)
        dl   = doubleLine(text).stretch_to_fit_width(16)
        dl[1].shift(0.05 * UP)
        
        self.add(text, dl)

        maynot = CellBoard(
            side_length = 0.3,
            dimension = (10, 24)
        ).shift(0.8 * DOWN)

        maynot.set_stageboard_by_rle("assets/maynot.rle")

        cell1 = CellBoard(
            side_length = 0.3,
            dimension = (10, 12)
        ).shift(3 * LEFT + 0.8 * DOWN)
        cell1.set_stageboard(maynot.board_arr[::, :12])

        cell2 = CellBoard(
            side_length = 0.3,
            dimension = (10, 11)
        ).shift(3 * RIGHT + 0.8 * DOWN)

        cell2.set_stageboard(maynot.board_arr[::, 13:])

        for i in range(10):
            for j in range(11):
                if cell2.board_arr[i, j] == 1 and cell1.board_arr[i, j] != 1:
                    cell2.get_cell(i + 1, j + 1).set_color(BLUE)
        
        self.play(Create(cell1))
        self.wait(2)
        self.play(Create(cell2))
        self.wait(3)

"""
对于一长行或者一长列的细胞，也可以加物体来稳定它们
展示feature 2.12
展示feature 2.13
"""
class InductionCoil(Scene):
    def construct(self):
        text = MyText("静物的构造", color = YELLOW).scale(1.3).to_edge(UP)
        dl   = doubleLine(text).stretch_to_fit_width(16)
        dl[1].shift(0.05 * UP)
        
        self.add(text, dl)

        induct1 = CellBoard(
            dimension = (7, 12),
            side_length = 0.5
        ).shift(0.8 * DOWN)

        induct1.set_stageboard_by_rle("assets/induct1.rle")

        self.add(induct1)
        
        extern_vg1 = VGroup()
        for i in range(7):
            for j in range(12):
                if induct1.board_arr[i, j] == 1:
                    if j <= 4 or j >= 9:
                        extern_vg1.add(
                            induct1.get_cell(
                                i + 1, j + 1
                            )
                        )
        
        extern_vg1.set_color(GREY)

        self.wait(2)
        self.play(extern_vg1.animate.set_color(BLUE))
        self.wait(2)

"""
这些物体被称为感应线圈（induction coil)
展示induction coil的table，
"""
class InductionCoilEnum(Scene):
    def construct(self):
        text = MyText("静物的构造", color = YELLOW).scale(1.3).to_edge(UP)
        dl   = doubleLine(text).stretch_to_fit_width(16)
        dl[1].shift(0.05 * UP)
        
        self.add(text, dl)

        coil1 = CellBoard(side_length = 0.4, dimension = (3, 5))
        coil1.set_stageboard_by_rle("assets/house.rle")

        coil2 = CellBoard(side_length = 0.4, dimension = (4, 4))
        coil2.set_stageboard_by_rle("assets/wing.rle")

        coil3 = CellBoard(side_length = 0.4, dimension = (4, 7))
        coil3.set_stageboard_by_rle("assets/anvil.rle")

        coil4 = CellBoard(side_length = 0.4, dimension = (4, 6))
        coil4.set_stageboard_by_rle("assets/racetrack.rle")

        coil5 = CellBoard(side_length = 0.4, dimension = (4, 6))
        coil5.set_stageboard_by_rle("assets/worm.rle")

        coil6 = CellBoard(side_length = 0.4, dimension = (3, 7))
        coil6.set_stageboard_by_rle("assets/bookendsiamesetable.rle")

        coil = VGroup(
            coil1, coil2, coil3, coil4, coil5, coil6
        ).arrange_in_grid(2, 3, buff = 0.9).shift(0.6 * DOWN)

        zhu = MyText("*感应线圈并不是静物，而是拿来稳定一长行/列细胞的物体").scale(0.3).next_to(dl, DOWN).to_edge(RIGHT).shift(0.45 * RIGHT + 0.15 * UP)
        self.add(zhu)
        self.add(coil)
        self.wait(5)

"""
这个是另一个例子，它本身并不是静物，但在加了感应线圈就变成了静物
展示feature 2.13
"""
class AnotherInductionCoil(Scene):
    def construct(self):
        text = MyText("静物的构造", color = YELLOW).scale(1.3).to_edge(UP)
        dl   = doubleLine(text).stretch_to_fit_width(16)
        dl[1].shift(0.05 * UP)
        
        self.add(text, dl)

        zhu = MyText("*感应线圈并不是静物，而是拿来稳定一长行/列细胞的物体").scale(0.3).next_to(dl, DOWN).to_edge(RIGHT).shift(0.45 * RIGHT + 0.15 * UP)
        self.add(zhu)

        induct2 = CellBoard(
            dimension = (11, 31),
            side_length = 0.3
        ).shift(0.8 * DOWN)

        induct2.set_stageboard_by_rle("assets/induct2.rle")

        extern_vg2 = VGroup()
        for i in range(11):
            for j in range(31):
                if induct2.board_arr[i, j] == 1:
                    if i <= 3 or i >= 7:
                        extern_vg2.add(
                            induct2.get_cell(
                                i + 1, j + 1
                            )
                        )
        extern_vg2.set_color(GREY)

        self.play(Create(induct2))
        self.wait(2.5)
        self.play(extern_vg2.animate.set_color(BLUE))
        self.wait(2.5)

"""
上面我们都是在讨论构造有限个细胞的静物，那么是否存在无限个细胞的静物呢？
答案是肯定的，有以下四种：
"""
class FiniteStill(Scene):
    def construct(self):
        text = MyText("静物的构造 - 无限细胞", color = YELLOW).scale(1.5)
        self.play(Write(text))

        dl = doubleLine(text)
        self.play(Create(dl), run_time = 0.5)
        self.wait(2)

        text.target = MyText("静物的构造 - 无限细胞", color = YELLOW).scale(1.3).to_edge(UP)
        dll = doubleLine(text.target).stretch_to_fit_width(16)
        dll[1].shift(0.05 * UP)
        self.play(
            MoveToTarget(text),
            ReplacementTransform(dl, dll)
        )

        #singleLife1 10 * 10
        #singleLife2 10 * 10
        #singleLife3 10 * 10

        singleLife1 = CellBoard(
            dimension = (5, 7)
        )
        singleLife1.set_stageboard_by_rle("assets/carriersiameseeaterhead.rle")

        singleLife2 = CellBoard(
            dimension = (6, 5)
        )
        singleLife2.set_stageboard_by_rle("assets/cisblockonlongbookend.rle")

        singleLife3 = CellBoard(
            dimension = (6, 4)
        )
        singleLife3.set_stageboard_by_rle("assets/longintegral.rle")

        life = VGroup(singleLife1, singleLife2, singleLife3).shift(0.3 * DOWN).arrange_in_grid(1, 3, buff = 1.2)
        
        text1 = MyText("细胞数：11").scale(0.85).next_to(singleLife1, DOWN)
        text2 = MyText("细胞数：12").scale(0.85).next_to(singleLife2, DOWN)
        text3 = MyText("细胞数：10").scale(0.85).next_to(singleLife3, DOWN)

        self.play(Create(life))
        self.play(Write(text1), Write(text2), Write(text3))
        self.wait(5)
        
        black_rec = Rectangle(height = 5, width = 20, color = BLACK, fill_opacity = 0.8).to_edge(DOWN)
        question_mark = Text("?", color = RED).scale(5)

        self.play(
            FadeIn(black_rec),
            GrowFromCenter(question_mark)
        )
        self.wait(2)

# 需要加文字
class InfiniteStill(Scene):
    def construct(self):
        zebra = CellBoard(dimension = (21, 27), side_length = 0.69).shift(1.9 * RIGHT + 1.5 * UP)
        zebra.set_stageboard_by_rle("assets/zebrastripes.rle")
        chicken = CellBoard(dimension = (40, 36))
        chicken.set_stageboard_by_rle("assets/chickenwire.rle")
        onion = CellBoard(dimension = (96, 96))
        onion.set_stageboard_by_rle("assets/onionrings.rle")

        #zebra_text = MyText("斑马条纹")
        #zebra_text2 = EngText("Zebra Stripes")
        zebra_vg = VGroup(MyText("斑马条纹"), EngText("Zebra Stripes")).scale(0.85).arrange_in_grid(2, 1).to_edge(UL).shift(0.3 * UP)
        zebra_rect = BackgroundRectangle(zebra_vg, color = BLACK).scale(1.2)

        chicken_vg = VGroup(MyText("鸡栏网"), EngText("Chicken Wire")).scale(0.85).arrange_in_grid(2, 1).to_edge(UL).shift(0.3 * UP)
        chicken_rect = BackgroundRectangle(chicken_vg, color = BLACK).scale(1.2)

        onion_vg = VGroup(MyText("洋葱圈"), EngText("Onion Rings")).scale(0.85).arrange_in_grid(2, 1).to_edge(UL).shift(0.3 * UP)
        onion_rect = BackgroundRectangle(onion_vg, color = BLACK).scale(1.2)

        self.add(zebra)
        self.add(zebra_rect, zebra_vg)

        self.wait(3)
        self.remove(zebra, zebra_rect, zebra_vg)

        self.add(chicken, chicken_rect, chicken_vg)
        self.wait(3)
        self.remove(chicken, chicken_rect, chicken_vg)
        self.add(onion, onion_rect, onion_vg)
        self.wait(3)

# 正如上集所说，滑翔机是最小的飞船，它在生命游戏中扮演非常重要的角色
class StartUsage(Scene):
    def construct(self):
        text = MyText("静物的用途 - 吞噬者", color = YELLOW).scale(2.5)
        self.play(Write(text))

        dl = doubleLine(text)
        self.play(Create(dl), run_time = 0.5)
        self.wait(2)

        text.target = MyText("静物的用途", color = YELLOW).scale(1.3).to_edge(UP)
        dll = doubleLine(text.target).stretch_to_fit_width(16)
        dll[1].shift(0.05 * UP)

        spaceship = CellBoard(
            side_length = 0.35,
            dimension = (12, 12)
        ).shift(0.7 * DOWN)
        board_arr = np.zeros((12, 12), dtype  = "int64")
        board_arr[0, 1] = board_arr[1, 2] = board_arr[2, :3] = 1
        spaceship.set_stageboard(board_arr)

        self.play(
            MoveToTarget(text),
            ReplacementTransform(dl, dll),
        )
        rec = SurroundingRectangle(spaceship, color = BLACK, fill_opacity = 1)
        self.add(spaceship)
        self.add(rec)
        self.play(FadeOut(rec))
        #self.play(Create(spaceship))
        #self.wait(2)
        
        for _ in range(30):
            spaceship.step()
            self.wait(0.15)
        self.wait(2)

"""
部分静物能有效的起到删除滑翔机的作用，因为整个动作很像把滑翔机吞噬，所以我们将它们称为吞噬者 (Eater)
像画面上展示的就是最受欢迎的吞噬者
因为它占的空间小而且被滑翔机冲击后恢复时间(Recovery Time)短，
"""
class EaterDef(Scene):
    def construct(self):
        text = MyText("静物的用途 - 吞噬者", color = YELLOW).scale(1.3).to_edge(UP)
        dl   = doubleLine(text).stretch_to_fit_width(16)
        dl[1].shift(0.05 * UP)
        
        self.add(text, dl)

        eater_glider = CellBoard(
            dimension = (7, 8)
        ).shift(0.4 * DOWN)
        eater_glider.set_stageboard_by_rle(
            "assets/eater_glider.rle"
        )
        text = MyText("吞噬者").next_to(eater_glider, DOWN)
        self.add(eater_glider)
        eater_glider.save_state()
        self.wait(1.5)
        for _ in range(6):
            eater_glider.step()
            self.wait(0.5)
        self.wait(1.5)
        self.play(Write(text))
        self.wait(4)
        self.play(eater_glider.animate.restore())

        rect = DashedVMobject(SurroundingRectangle(
            VGroup(*[
                eater_glider.get_cell(
                    i, j
                )
                for i in range(4, 8)
                for j in range(5, 9)
            ]),
            color = ORANGE
        ), num_dashes = 35).scale(0.95)

        GenerationText = MyText("0").to_corner(DR)

        self.play(Create(rect), FadeIn(GenerationText))
        self.wait()

        eater_glider.set_stageboard_by_rle(
            "assets/eater_glider.rle"
        )
        
        for i in range(4):
            eater_glider.step()
            self.remove(GenerationText)
            GenerationText = MyText(str(i + 1)).to_corner(DR)
            self.add(GenerationText)
            self.wait(0.5)
        self.wait(2)

# 同时它也可以吞噬掉其他类型的飞船
class EatOtherTypes(Scene):
    def construct(self):
        text = MyText("静物的用途 - 吞噬者", color = YELLOW).scale(1.3).to_edge(UP)
        dl   = doubleLine(text).stretch_to_fit_width(16)
        dl[1].shift(0.05 * UP)
        
        self.add(text, dl)

        eater_multi1 = CellBoard(
            dimension = (8, 34),
            side_length = 0.22
        ).shift(0.8 * UP)
        eater_multi1.set_stageboard(
            expand_rle("assets/eater_multi.rle")[::, 11:45]
        )

        eater_multi2 = CellBoard(
            dimension = (8, 34),
            side_length = 0.22
        ).shift(2.0 * DOWN)
        stage = expand_rle("assets/eater_multi.rle")[::, 44:]
        stage[-1, 0] = 0
        eater_multi2.set_stageboard(
            stage
        )

        self.add(eater_multi1, eater_multi2)
        self.wait(3)
        for i in range(20):
            eater_multi1.step()
            eater_multi2.step()
            self.wait(0.15)
        self.wait(2)

"""
除此之外还有其他吞噬者有不同的作用
"""
class OtherEaters(Scene):
    def construct(self):
        text = MyText("静物的用途 - 吞噬者", color = YELLOW).scale(1.3).to_edge(UP)
        dl   = doubleLine(text).stretch_to_fit_width(16)
        dl[1].shift(0.05 * UP)
        
        self.add(text, dl)
        # eater 1, eater 2, eater 5
        eater1 = CellBoard(
            dimension = (4, 4),
            side_length = 0.4
        )
        eater1.set_stageboard_by_rle("assets/eater1.rle")

        eater2 = CellBoard(
            dimension = (7, 7),
            side_length = 0.4
        )
        eater2.set_stageboard_by_rle("assets/eater2.rle")

        eater5 = CellBoard(
            dimension = (6, 9),
            side_length = 0.4
        )
        eater5.set_stageboard_by_rle("assets/eater5.rle")

        eater_vg = VGroup(
            eater1, eater2, eater5
        )
        eater_vg.arrange_in_grid(1, 3, buff = 1.2)

        self.add(eater_vg)

        eater1_text = EngText("Eater 1").scale(0.8).next_to(eater1, DOWN)
        eater2_text = EngText("Eater 2").scale(0.8).next_to(eater2, DOWN)
        eater5_text = EngText("Eater 5").scale(0.8).next_to(eater5, DOWN)

        eater2_text.shift(0.2 * DOWN)
        eater1_text.align_to(eater2_text, DOWN)
        eater5_text.align_to(eater2_text, DOWN)

        self.add(eater1_text, eater2_text, eater5_text)
        self.wait(2.5)

"""
像eater 2能够吞噬来自四个平行方向的滑翔机, 
eater 5能吞噬来自两个垂直方向的滑翔机
"""
class OtherEatersFunction(Scene):
    def construct(self):
        text = MyText("静物的用途 - 吞噬者", color = YELLOW).scale(1.3).to_edge(UP)
        dl   = doubleLine(text).stretch_to_fit_width(16)
        dl[1].shift(0.05 * UP)
        
        self.add(text, dl)

        eater2 = CellBoard(
            dimension = (33, 35),
            side_length = 0.12
        ).shift(0.6 * DOWN)
        eater2.set_stageboard_by_rle("assets/eater2_four_path.rle")

        self.add(eater2)

        for _ in range(20):
            eater2.step()

        for _ in range(80):
            eater2.step()
            self.wait(0.05)
        self.wait(3)

        eater5 = CellBoard(
            dimension = (13, 12),
            side_length = 0.3
        ).shift(0.6 * DOWN)
        eater5.set_stageboard_by_rle("assets/eater5_two_path.rle")

        self.play(ReplacementTransform(eater2, eater5))
        self.wait(2)

        for _ in range(24):
            eater5.step()
            self.wait(0.1)
        self.wait(3)

"""
有些静物不能完全吞噬单个滑翔机但能吞噬一对吞噬机，
像蛇在接收一个滑翔机后会把它变成小船，再接收第二个把小船消掉，只剩下它自己；
"""
class BoatBit(Scene):
    def construct(self):
        text = MyText("静物的用途 - 吞噬者", color = YELLOW).scale(1.3).to_edge(UP)
        dl   = doubleLine(text).stretch_to_fit_width(16)
        dl[1].shift(0.05 * UP)
        
        self.add(text, dl)

        boat_bit = CellBoard(
            dimension = (15, 20),
            side_length = 0.25
        ).shift(0.6 * DOWN)
        boat_bit.set_stageboard_by_rle(
            "assets/boat_bit.rle"
        )

        self.add(boat_bit)
        self.wait(4)
        for _ in range(12):
            boat_bit.step()
            self.wait(0.2)
        self.wait(1.7)
        for _ in range(32):
            boat_bit.step()
            self.wait(0.1)
        self.wait(2)

"""
叶子接收一个滑翔机之后朝向会反过来
在另一个方向接收滑翔机之后再正回来 
"""
class LoafFlip(Scene):
    def construct(self):
        text = MyText("静物的用途 - 吞噬者", color = YELLOW).scale(1.3).to_edge(UP)
        dl   = doubleLine(text).stretch_to_fit_width(16)
        dl[1].shift(0.05 * UP)
        
        self.add(text, dl)

        loaf_flip = CellBoard(
            side_length = 0.3,
            dimension = (11, 11)
        ).shift(0.5 * DOWN)
        loaf_flip.set_stageboard_by_rle("assets/loaf_flip.rle")

        self.add(loaf_flip)

        self.wait(2)

        for _ in range(4):
            loaf_flip.step()
            self.wait(0.3)
        
        self.wait(2.5)

        for _ in range(4):
            loaf_flip.step()
            self.wait(0.3)
        
        self.wait(2)

"""
这个特点被用在了eater 3的设计当中
当接收滑翔机过后叶子朝向反过来
旁边的结构又会把它正回来
"""
class Eater3(Scene):
    def construct(self):
        text = MyText("静物的用途 - 吞噬者", color = YELLOW).scale(1.3).to_edge(UP)
        dl   = doubleLine(text).stretch_to_fit_width(16)
        dl[1].shift(0.05 * UP)
        
        self.add(text, dl)

        eater3 = CellBoard(
            dimension = (16, 16),
            side_length = 0.26
        ).shift(0.6 * DOWN)
        eater3.set_stageboard_by_rle("assets/eater3_glider.rle")
        eater3_text = EngText("Eater 3").scale(.8).next_to(dl, DOWN).shift(4 * LEFT)
        self.add(eater3, eater3_text)
        self.wait(2)

        for _ in range(8):
            eater3.step()
            self.wait(0.3)
        self.wait(2.5)
        for _ in range(8):
            eater3.step()
            self.wait(0.3)
        self.wait(2.5)
    
"""
考虑以下这个场景，如果我们想删掉以上两个滑翔机，第一个想法是做两个吞噬者分别吞掉滑翔机，
但因为两个滑翔机已经靠的太近，
已经没有空间同时放下两个吞噬者，而且让它们依然是静物
解决方案是把两个吞噬者“焊接”在一起
对于eater 1来说只有上方的部分真正起到吞噬的作用，下方只是做支撑，
于是我们可以保留上方的结构，重新设计支撑部分
"""
class WeldedStill(Scene):
    def construct(self):
        """
        text = MyText("静物的用途 - 吞噬者", color = YELLOW).scale(1.3).to_edge(UP)
        dl   = doubleLine(text).stretch_to_fit_width(16)
        dl[1].shift(0.05 * UP)
        
        self.add(text, dl)
        """
        
        text = MyText("静物的用途 - 焊接静物", color = YELLOW).scale(1.3)
        self.play(Write(text))

        dl = doubleLine(text)
        self.play(Create(dl), run_time = 0.5)
        self.wait(2)

        text.target = MyText("静物的用途 - 焊接静物", color = YELLOW).scale(1.3).to_edge(UP)
        dll = doubleLine(text.target).stretch_to_fit_width(16)
        dll[1].shift(0.05 * UP)
        self.play(
            MoveToTarget(text),
            ReplacementTransform(dl, dll)
        )
        self.wait(2)

        modified_table = CellBoard(
            dimension = (13, 21),
            side_length = 0.3
        ).shift(0.6 * DOWN)

        arr = expand_rle("assets/unstable_eater.rle")
        modified_arr = arr.copy()
        modified_arr[6:, ::] = 0
        #null_arr = np.zeros((1, 21))
        #modified_arr = np.concatenate((modified_arr, null_arr))

        modified_table.set_stageboard(
            modified_arr
        )
        

        self.add(modified_table)
        self.wait(3)

        # begin with 0
        red_cells_arr = [
            [6, 7], [6, 8],
            [7, 7], [7, 9],
            [8, 9], 
            [9, 9], [9, 10], 
        ]

        blue_cells_arr = [
            [8, 12], [8, 13],
            [9, 11], [9, 13],
            [10, 11], 
            [11, 10], [11, 11]
        ]
        anim_list = []
        
        for i, j in red_cells_arr:
            anim_list.append(
                modified_table.get_cell(i + 1, j + 1).animate.set_color(YELLOW)
            )

        for i, j in blue_cells_arr:
            anim_list.append(
                modified_table.get_cell(i + 1, j + 1).animate.set_color(ORANGE)
            )
        
        anim_group = AnimationGroup(*anim_list)

        myTemplate = TexTemplate()
        myTemplate.add_to_preamble(r"\usepackage{pifont}")

        tick = Tex(r"\ding{51}", color = GREEN, tex_template = myTemplate).scale(0.8) # svg
        cross = Tex(r"\ding{55}", color = RED, tex_template = myTemplate).scale(0.8) # svg

        cross_vg = VGroup(
            cross.copy().move_to(modified_table.get_cell_center(9, 10)),
            cross.copy().move_to(modified_table.get_cell_center(10, 11)),
        )

        tick_vg = VGroup(
            tick.copy().move_to(modified_table.get_cell_center(8, 11)),
            tick.copy().move_to(modified_table.get_cell_center(10, 9)),
        )

        self.play(anim_group)
        self.wait(3)
        self.play(FadeIn(tick_vg), FadeIn(cross_vg))
        self.wait(2.5)

        anim_list = []
        for i, j in red_cells_arr:
            anim_list.append(
                modified_table.get_cell(i + 1, j + 1).animate.set_color(WHITE)
            )

        for i, j in blue_cells_arr:
            anim_list.append(
                modified_table.get_cell(i + 1, j + 1).animate.set_color(WHITE)
            )

        self.play(
            FadeOut(VGroup(cross_vg, tick_vg)),
            AnimationGroup(*anim_list)
        )
        self.wait(3)

        anim_list = []
        useful_cells_arr = [
            [6, 7], [6, 8],
            [7, 7],
            [8, 12], [8, 13],
            [9, 13],
        ]
        for i, j in useful_cells_arr:
            anim_list.append(
                modified_table.get_cell(i + 1, j + 1).animate.set_color("#8A2BE2")
            )
        self.play(AnimationGroup(*anim_list))

        not_useful_arr = [
            [9, 9], [9, 10], 
            [11, 10], [11, 11]
        ]

        for i, j in not_useful_arr:
            anim_list.append(
                modified_table.get_cell(i + 1, j + 1).animate.set_color(GREY)
            )
        self.play(AnimationGroup(*anim_list))

        new_cells_arr = [
            [9, 9], [10, 9], [11, 9],
            [11, 11], [12, 10],
            [10, 6], [10, 7],
            [11, 6], [11, 7]
        ]

        anim_list = []
        for i, j in new_cells_arr:
            anim_list.append(
                modified_table.get_cell(i + 1, j + 1).animate.set_color(WHITE)
            )
        self.play(AnimationGroup(*anim_list))
        self.wait(3)

# 在接下来每一集视频最后会放一个翻译对照表，方便大家对照中英版本的术语
class TranslateAnim(Scene):
    def construct(self):
        """
        eater 吞噬者
        induction coil 感应线圈
        welded still life 焊接静物
        """
        vg = VGroup(
            EngText("eater", color = RED), MyText("吞噬者", color = BLUE),
            EngText("induction coil", color = RED), MyText("感应线圈", color = BLUE),
            EngText("welded still life", color = RED), MyText("焊接静物", color = BLUE),
        ).arrange_in_grid(3, 2, buff = (2.5, MED_LARGE_BUFF))
        # three arrows
        #self.add(vg)
        arrow1 = Arrow(LEFT, 1.2 * RIGHT, color = ORANGE).shift(1.25 * UP + 0.8* RIGHT)
        arrow2 = Arrow(LEFT, 1.2 * RIGHT, color = ORANGE).shift(0.00* UP + 0.8 * RIGHT)
        arrow3 = Arrow(LEFT, 1.2 * RIGHT, color = ORANGE).shift(1.25 * DOWN + 0.8 * RIGHT)
        #self.add(arrow1, arrow2, arrow3)

        self.play(AnimationGroup(*[
            GrowFromCenter(
                mob
            )
            for mob in vg
        ]))
        self.wait(1.5)
        self.play(
            GrowArrow(arrow1),
            GrowArrow(arrow2),
            GrowArrow(arrow3)
        )
        self.wait(2)
        

# 另外在P2我都会放一个生命游戏有关的书籍/工具/论坛安利
class Anli(Scene):
    def construct(self):
        # three svgs pop up
        book  = SVGMobject("assets/book.svg").shift(3.5 * LEFT)
        tool  = SVGMobject("assets/tool.svg")
        forum = SVGMobject("assets/forum.svg", color = WHITE).shift(3.5 * RIGHT)

        self.play(
            SpinInFromNothing(book),
            SpinInFromNothing(tool),
            SpinInFromNothing(forum)
        )
        self.wait(4)

"""
像这集安利的就是我这个系列的参考书籍 Game of Life -- Construction and Mathematics
大家如果有兴趣可以看看！
"""
class AnliBook(Scene):
    def construct(self):
        page_1 = ImageMobject("assets/conway_life_book/conway_life_book-1.png").scale(0.5)
        page_2 = ImageMobject("assets/conway_life_book/conway_life_book-2.png").scale(0.5)
        page_3 = ImageMobject("assets/conway_life_book/conway_life_book-3.png").scale(0.5)
        page_4 = ImageMobject("assets/conway_life_book/conway_life_book-4.png").scale(0.5)
        page_5 = ImageMobject("assets/conway_life_book/conway_life_book-5.png").scale(0.5)
        page_1.z_index = 5
        page_2.z_index = 4
        page_3.z_index = 3
        page_4.z_index = 2
        page_5.z_index = 1
        vg = Group(page_1, page_2, page_3, page_4, page_5)
        
        self.add(vg)
        self.wait(2)
        self.play(
            page_1.animate.shift(4 * LEFT),
            page_2.animate.shift(2.00 * LEFT),
            page_3.animate.shift(0.0 * RIGHT),
            page_4.animate.shift(2.0 * RIGHT),
            page_5.animate.shift(4 * RIGHT)
        )
        self.wait(2)
        # some animations like in PPT
        # save_state()
        # restore()
"""
三连动画
"""
class Sanlian(Scene):
    def construct(self):
        good = SVGMobject("assets/good.svg", color = WHITE).scale(1.1).shift(3.8 * LEFT)
        coin = SVGMobject("assets/coin.svg", color = WHITE).scale(1.1)
        favo = SVGMobject("assets/favo.svg", color = WHITE).scale(1.1).shift(3.8 * RIGHT)

        self.play(
            SpinInFromNothing(good),
            SpinInFromNothing(coin),
            SpinInFromNothing(favo)
        )
        circle_coin = Circle().scale(1.15).move_to(coin.get_center()).set_stroke(PINK, 10)
        circle_favo = Circle().scale(1.25).move_to(favo.get_center()).set_stroke(PINK, 10).shift(0.1 * DOWN)
        # color = "#FF69B4"

        self.play(
            good.animate.set_color("#FF69B4"),
            Create(circle_coin),
            Create(circle_favo)
        )

        self.play(
            FadeOut(circle_coin),
            FadeOut(circle_favo),
            coin.animate.set_color("#FF69B4"),
            favo.animate.set_color("#FF69B4"),
            Flash(good, color = "#FF69B4", flash_radius = 1.5, line_length = 0.9, line_stroke_width = 7),
            Flash(coin, color = "#FF69B4", flash_radius = 1.5, line_length = 0.9, line_stroke_width = 7),
            Flash(favo, color = "#FF69B4", flash_radius = 1.5, line_length = 0.9, line_stroke_width = 7)
        )
        
        self.wait(2)

"""
翻译对照表
"""
class TranslateTerm(Scene):
    def construct(self):
        text = MyText("中英对照表 - 术语", color = YELLOW).scale(1.3).to_edge(UP)
        dl   = doubleLine(text).stretch_to_fit_width(16)
        dl[1].shift(0.05 * UP)
        
        self.add(text, dl)

        term_dict = {
            "still life": "静物",
            "stable pattern": "稳定结构",
            "oscillator": "振荡器",
            "spaceship": "飞船",
            "connected": "连通",
            "strict still life": "严格静物",
            "eater": "吞噬者",
            "induction coil": "感应线圈",
            "recovery time": "恢复时间",
            "welded still life": "焊接静物"
        }
        term = [EngText(key, color = ORANGE).scale(0.8) for key in term_dict.keys()]
        term_vg = VGroup(*term).arrange_in_grid(5, 2, (3, 0.45)).shift(0.65 * DOWN + 0.8 * LEFT)
        for i in [0,2,4,6]:
            term_vg[i].align_to(term_vg[8], LEFT)
        for i in [1,3,5,7]:
            term_vg[i].align_to(term_vg[9], LEFT)
        self.add(term_vg)

        term_ch = [
            MyText(val, color = RED_D).scale(0.8).next_to(term_vg[i], RIGHT) 
            for i, val in enumerate(term_dict.values())
        ]
        term_ch_vg = VGroup(*term_ch)
        self.add(term_ch_vg)
        self.wait(5)
        
"""
翻译对照表
"""
class TranslateObject(Scene):
    def construct(self):
        text = MyText("中英对照表 - 物体", color = YELLOW).scale(1.3).to_edge(UP)
        dl   = doubleLine(text).stretch_to_fit_width(16)
        dl[1].shift(0.05 * UP)
        
        self.add(text, dl)

        term_dict = {
            "glider": "滑翔机",
            "block": "方块",
            "beehive": "蜂窝",
            "honey farm": "蜂蜜农场",
            "boat": "船",
            "snake": "蛇",
            "zebra stripes": "斑马条纹",
            "chicken wire": "鸡栏网",
            "onion rings": "洋葱圈",
            "leave": "叶子"
        }
        term = [EngText(key, color = ORANGE).scale(0.8) for key in term_dict.keys()]
        term_vg = VGroup(*term).arrange_in_grid(5, 2, (3, 0.45)).shift(0.65 * DOWN + 0.8 * LEFT)
        for i in [0,2,4,6]:
            term_vg[i].align_to(term_vg[8], LEFT)
        for i in [1,3,5,7]:
            term_vg[i].align_to(term_vg[9], LEFT)
        self.add(term_vg)

        term_ch = [
            MyText(val, color = RED_D).scale(0.8).next_to(term_vg[i], RIGHT) 
            for i, val in enumerate(term_dict.values())
        ]
        term_ch_vg = VGroup(*term_ch)
        self.add(term_ch_vg)
        self.wait(5)

class NextViewOne(Scene):
    def construct(self):
        text = MyText("下期预览", color = YELLOW).to_corner(UL)
        self.add(text)

        volcano = CellBoard(
            dimension = (17, 24),
            side_length = 0.21
        ).shift(3.5 * LEFT + 0.4 * DOWN)
        volcano.set_stageboard_by_rle("assets/heavyweightvolcano.rle")

        hebdarole = CellBoard(
            dimension = (20, 24),
            side_length = 0.21
        ).shift(3.5 * RIGHT + 0.4 * DOWN)
        hebdarole.set_stageboard(
            np.concatenate(
                [np.zeros((2, 24)),
                expand_rle("assets/hebdarole.rle")],
                axis = 0
            )
        )

        self.add(volcano, hebdarole)
        
        for _ in range(30):
            volcano.step()
            hebdarole.step()
            self.wait(0.15)
        

class NextViewTwo(Scene):
    def construct(self):
        text = MyText("下期预览", color = YELLOW).to_corner(UL)
        self.add(text)

        fountain = CellBoard(
            dimension = (15, 19),
            side_length = 0.28
        ).shift(3.1 * LEFT + 0.4 * DOWN)
        fountain.set_stageboard_by_rle("assets/fountain.rle")

        galaxy = CellBoard(
            dimension = (13, 13),
            side_length = 0.35
        ).shift(3.9 * RIGHT + 0.4 * DOWN)
        galaxy.set_stageboard(
            np.pad(
                expand_rle("assets/koksgalaxy.rle"),
                ((2, 2), (2, 2))
            )
        )

        fountain.scale_to_fit_height(galaxy.height)

        self.add(fountain, galaxy)
        
        for _ in range(30):
            fountain.step()
            galaxy.step()
            self.wait(0.15)

class NextViewThree(Scene):
    def construct(self):
        text = MyText("下期预览", color = YELLOW).to_corner(UL)
        self.add(text)

        p37 = CellBoard(
            dimension = (47, 47),
            side_length = 0.1
        ).shift(0.4 * DOWN)
        p37.set_stageboard(
            expand_rle("assets/132p37.rle")
        )
        self.add(p37)
        
        for _ in range(37):
            p37.step()
            self.wait(0.12)
        

class NextViewFour(Scene):
    def construct(self):
        text = MyText("下期预览", color = YELLOW).to_corner(UL)
        self.add(text)

        shuttle = CellBoard(
            dimension = (37, 37),
            side_length = 0.12
        ).shift(0.4 * DOWN)
        shuttle.set_stageboard_by_rle("assets/prepulsarshuttle26.rle")

        self.add(shuttle)

        for _ in range(26):
            shuttle.step()
            self.wait(0.12)