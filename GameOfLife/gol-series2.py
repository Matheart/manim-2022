from inspect import BoundArguments
from this import s
from manim import *
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
        ).scale(1.5)
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
                    mark = Text("?", color = BLUE_D).scale(0.9).move_to(
                        block.get_cell_center(i, j)
                    )
                    question_vg.add(mark)
        self.play(FadeIn(question_vg))

        self.wait(1.5)


        block_vg = VGroup(*[
            block.get_cell(i, j)
            for i in [1, 2, 3]
            for j in [1, 2, 3]
        ])

        rec = DashedVMobject(
            SurroundingRectangle(block_vg, color = PINK)
        )

        self.play(
            Create(rec)
        )
        self.wait(1)
        self.play(FadeOut(rec))
        self.wait(2)
        self.play(FadeOut(question_vg))
        self.wait(2)

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

