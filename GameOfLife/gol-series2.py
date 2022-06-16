from manim import *
from gol import *

class MyText(Text):
    def __init__(self, text: str, font: str = "FZYanSongS-R-GB",  **kwargs):
        super().__init__(text = text, font = font, **kwargs)

class bgRec(BackgroundRectangle):
    def __init__(self, mobject, **kwargs):
        super().__init__(
            mobject = mobject,
            color = BLACK, 
        )
        self.scale(1.2)

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
        conwayName = MyText("John Conway").scale(0.5).next_to(conway, DOWN)
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

