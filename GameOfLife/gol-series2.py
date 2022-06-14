from manim import *
from gol import *

class MyText(Text):
    def __init__(self, text: str, font: str = "FZYanSongS-R-GB",  **kwargs):
        super().__init__(text = text, font = font, **kwargs)

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
            dimension = (50, 50)
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

        vg_dead = VGroup(
            live, white_sq, 
            no, grey_sq,
            death, blue_sq 
        ).arrange_in_grid(3, 2).to_edge(UL)
        rect_dead = BackgroundRectangle(vg_dead, color = BLACK).scale(1.2)
        vg_dead = VGroup(vg_dead, rect_dead)

        self.play(ReplacementTransform(vg, vg_dead))
        # have bug here
        self.wait(2)
