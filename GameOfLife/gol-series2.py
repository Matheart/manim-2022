from inspect import BoundArguments
from this import s
from cv2 import cartToPolar
from manim import *
from matplotlib import animation
from gol import *

class MyText(Text):
    def __init__(self, text: str, font: str = "FZYanSongS-R-GB",  **kwargs):
        super().__init__(text = text, font = font, **kwargs)

class EngText(Text):
    def __init__(self, text: str, font: str = "Georgia",  **kwargs):
        super().__init__(text = text, font = font, **kwargs)

class bgRec(BackgroundRectangle):
    def __init__(self, mobject, **kwargs):
        super().__init__(
            mobject = mobject,
            color = BLACK, 
        )
        self.scale(1.2)

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

class FamousVersion(Scene):
    def construct(self):
        conway = ImageMobject("assets/Conway.jpg")
        magazine = ImageMobject("assets/Scientific_American.jpeg")
        conway.height = 4
        conway.shift(3 * LEFT + 0.5 * DOWN)
        magazine.height = 5.5
        magazine.shift(3 * RIGHT + 0.5 * DOWN)

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

        self.add(grid)
        
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

class ThreeStructures(Scene):
    def construct(self):
        pass

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
        Block_set = np.zeros((4, 4))
        Block_set[1][1] = Block_set[1][2] = 1
        Block_set[2][1] = Block_set[2][2] = 1
        BlockCell = CellBoard(
            dimension = (4, 4)
        )
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

        BlockName = MyText("方块").next_to(BlockCell, DOWN)
        CoilName = MyText("熄灭的火花线圈").scale(0.6).next_to(CoilCell, DOWN).align_to(BlockName, DOWN)
        WormName = MyText("触角").next_to(WormCell, DOWN).align_to(BlockName, DOWN)
        ClipName = MyText("弯曲的回形针").next_to(ClipCell, DOWN).scale(0.6).align_to(BlockName, DOWN)

        text_vg = VGroup(BlockName, CoilName, WormName, ClipName)

        self.play(Create(cell_vg))
        self.play(
            FadeIn(text_vg, shift = UP)
        )
        self.wait(4)

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
        pond.scale_to_fit_height(0.85)
        #------------------------------------------#

        fst = ["0", "...", "1", "5", "...", "?"]
        snd = [
            EngText("SSS", color = BLACK).scale(0.65), 
            EngText("SSS", color = BLACK).scale(0.65), 
            boat, snake, 
            EngText("SSS", color = BLACK).scale(0.65), 
            pond
        ]

        lst = [
            [EngText(fst[i]).scale(0.8), snd[i]] 
            for i in range(6)
        ]
        row_labels = [
            EngText(i).scale(0.8) for i in
            ["1", "...", "5", "6",  "...", "8"]
        ]

        table = MobjectTable(
            lst,
            row_labels = row_labels,
            col_labels = [MyText("#静物个数").scale(0.8), MyText("例子").scale(0.8)],
            v_buff = 0.37,
            top_left_entry = MyText("#细胞个数").scale(0.8)
        ).shift(DOWN + 0.22 * LEFT)

        self.play(
            FadeIn(table)
        )
        self.wait(2.5)
        self.play(
            FadeIn(Cross(table))
        )
        self.wait(2)

        #rtable = 

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
        ).shift(0.8 * DOWN)

        def get_block(start_x, start_y):
            return VGroup(
                board.get_cell(start_x, start_y),
                board.get_cell(start_x + 1, start_y),
                board.get_cell(start_x, start_y + 1),
                board.get_cell(start_x + 1, start_y + 1),
            )
        get_block(3, 3).set_color(WHITE)
        get_block(7, 7).set_color(WHITE)

        self.add(board)

        self.play(
            get_block(3, 3).animate.set_color(GREY),
            get_block(7, 7).animate.set_color(GREY),
            get_block(2, 6).animate.set_color(WHITE),
            get_block(8, 3).animate.set_color(WHITE),
        )
        self.wait(1)
        self.play(
            get_block(2, 6).animate.set_color(GREY),
            get_block(8, 3).animate.set_color(GREY),
            get_block(4, 2).animate.set_color(WHITE),
            get_block(4, 7).animate.set_color(WHITE),
        )
        self.wait(1)
        self.play(
            get_block(4, 2).animate.set_color(GREY),
            get_block(4, 7).animate.set_color(GREY),
            get_block(2, 2).animate.set_color(WHITE),
            get_block(8, 5).animate.set_color(WHITE),
        )
        self.wait(3)
        self.play(
            get_block(2, 2).animate.set_color(RED),
            get_block(8, 5).animate.set_color(BLUE),            
        )
        self.wait(3)

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

        self.wait(2.5)
        self.play(ReplacementTransform(text, text_transform))
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
        self.wait()
        animation_list = []
        for i in ptsL:
            animation_list.append(
                mirror.get_cell(i[0], 6 - i[1]).animate.set_color(GREY)
            )
        self.play(AnimationGroup(*animation_list))

        ear_unstable = CellBoard(
            side_length = 0.4,
            dimension = (11, 11)
        ).shift(0.8 * DOWN)
        arr = np.zeros((11, 11))
        arr[3][4] = arr[3][5] = arr[4][5] = arr[5][5] = arr[6][5] = arr[6][4] = 1 
        ear_unstable.set_stageboard(arr)

        self.play(ReplacementTransform(mirror, ear_unstable))
        self.wait()
        self.play(ear_unstable.animate.shift(4 * LEFT))

        arrow = Arrow(start = 1.2 * LEFT, end = 1.2 * RIGHT, stroke_width = 13).shift(DOWN)

        ear_unstable_copy = ear_unstable.copy()
        self.play(
            GrowArrow(arrow),
            ear_unstable_copy.animate.shift(8 * RIGHT)
        )
    
        for i in range(15):
            ear_unstable_copy.step()
            self.wait(0.15)
        self.wait(2)

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
        self.play(Wiggle(snake1_text))
        self.wait(5)
        self.play(Wiggle(snake2_text))
        self.wait(1)
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

class EquivNotation(Scene):
    def construct(self):
        text = MyText("静物的构造", color = YELLOW).scale(1.3).to_edge(UP)
        dl   = doubleLine(text).stretch_to_fit_width(16)
        dl[1].shift(0.05 * UP)
        
        self.add(text, dl)

        snake3 = CellBoard(
            side_length = 0.4, 
            dimension = (5, 7)
        ).scale(1.7).shift(0.5 * DOWN)
        snake3.set_stageboard(
            expand_rle("assets/long3snake.rle")
        )

        text1 = EngText("long^3 snake").scale(1.2).next_to(snake3, DOWN)
        text2 = EngText("very very long snake").scale(1.2).next_to(snake3, DOWN)
        text3 = EngText("extra long snake").scale(1.2).next_to(snake3, DOWN)

        self.add(snake3, text1)

        self.wait(1)
        self.play(ReplacementTransform(text1, text2))
        self.wait(1)
        self.play(ReplacementTransform(text2, text3)) 
        self.wait(3)       

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
                    mark = Text("?", color = "#00FFFF", fill_opacity = 10).scale(0.9).move_to(
                        block.get_cell_center(i, j)
                    )
                    question_vg.add(mark)

        self.wait(1.5)


        block_vg = VGroup(*[
            block.get_cell(i, j)
            for i in [1, 2, 3]
            for j in [1, 2, 3]
        ])

        rec = DashedVMobject(
            SurroundingRectangle(block_vg, color = "#00FF00").scale(0.95),
            num_dashes = 30
        )
        
        self.play(
            Create(rec)
        )
        self.wait(1)
        self.play(FadeOut(rec))
        self.wait(2)
        """
        self.play(FadeOut(question_vg))
        self.wait(2)
        """

class StillThick(Scene):
    def construct(self):
        text = MyText("静物的构造", color = YELLOW).scale(1.3).to_edge(UP)
        dl   = doubleLine(text).stretch_to_fit_width(16)
        dl[1].shift(0.05 * UP)
        
        self.add(text, dl)

        thickLife = CellBoard(
            dimension = (8, 8)
        )
        thickLife.set_stageboard_by_rle("assets/thick.rle")
        thickLife2 = thickLife.copy()
        thickLife2.step()

        thickLife.shift(4 * LEFT + DOWN)
        thickLife2.shift(4 * RIGHT + DOWN)

        arr = Arrow(1.5 * LEFT, 1.5 * RIGHT, color = RED, stroke_width = 17).shift(DOWN)
        text = MyText("下一代", color = RED).scale(0.8).next_to(arr, DOWN).shift(0.15 * LEFT)
        self.add(thickLife, thickLife2, arr, text)
        self.wait(3)

        cross = Cross(thickLife)
        self.play(Create(cross))

