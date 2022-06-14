from manim import *
import numpy as np

def unit(angle):
    return np.array([np.cos(angle), np.sin(angle), 0])

def scale_center(position, target, ratio):
    return position - (position - target) / (1 - ratio)

class Notice(VGroup):
    def __init__(self, m_text1, m_text2):
        super().__init__()
        self.line1 = Text(m_text1, font = 'SimSun')
        self.line2 = Text(m_text2, font = 'SimSun')
        self.line2.next_to(self.line1, DOWN)
        self.add(self.line1, self.line2)
        self.scale(0.5)
        self.shift(np.array([5.8, 2.9, 0]))

class Digit(VGroup):
    def __init__(self, digit):

        super().__init__()
        self.number = []
        self.digit = digit
        for i in range (10):
            numberi = Tex(r"%d"%i).set_opacity(0)
            self.add(numberi)
            self.number.append(numberi)
        self.number[self.digit].set_opacity(1)

    def set_number(self, digit, opacity):
        self.number[self.digit].set_opacity(0)
        self.digit = digit
        self.number[self.digit].set_opacity(opacity)
        return self

class Year(VGroup):
    def __init__(self, decimal):

        super().__init__()
        distance = 0.12
        self.one = Digit(decimal % 10).shift(3*distance*RIGHT)
        decimal = int(decimal / 10)
        self.ten = Digit(decimal % 10).shift(distance*RIGHT)
        decimal = int(decimal / 10)
        self.hundred = Digit(decimal % 10).shift(distance*LEFT)
        decimal = int(decimal / 10)
        self.thousand = Digit(decimal % 10).shift(3*distance*LEFT)
        self.add(self.one, self.ten, self.hundred, self.thousand)

    def set_year(self, year, opacity):
        self.one.set_number(year % 10, opacity)
        year = int(year / 10)
        self.ten.set_number(year % 10, opacity)
        year = int(year / 10)
        self.hundred.set_number(year % 10, opacity)
        year = int(year / 10)
        self.thousand.set_number(year % 10, opacity)

class Intro0(Scene):
    def construct(self):
        ##  Making object
        notice0 = Notice("沃茨基·硕德", "请勿模仿")
        quote = Text(
            "数学家们喜欢给相同的东西起不同的名字，\n这样，一些好用的性质就会自己长出来。", 
            font = 'SimSun', 
            t2c={
                "相同的东西": GREEN, 
                "不同的名字": GREEN, 
                "好用的性质": BLUE}
        )

        author = Text("-Walski Schölder", color = YELLOW, font = "Times New Roman")
        author.next_to(quote.get_corner(DOWN + RIGHT), DOWN + LEFT)
        ##  Showing object
        self.play(Write(quote), runtime = 2)
        self.play(Write(author), Write(notice0))
        self.wait(2)
        self.play(FadeOut(quote), FadeOut(author))
        self.wait(1)

class Intro1(Scene):
    def waiting(self, second, frame = 0):
        self.wait(second + frame / 30.0)

    def construct(self):
        notice0 = Notice("沃茨基·硕德", "请勿模仿")
        notice1 = Notice("历史故事", "请听介绍")
        notice2 = Notice("最妙算法", "请　瞻仰")
        notice3 = Notice("历史故事", "请听介绍")
        notice4 = Notice("有 蜘 蛛", "啊啊啊啊")
        notice5 = Notice("硬件知识", "请记结论*")
        notice6 = Notice("历史故事", "请听介绍")
        notice7 = Notice("视频前言", "请听介绍")

        picture_winograd = ImageMobject("picture_winograd.jpg")
        picture_winograd.height = 4
        picture_winograd.shift(2*LEFT + 0.5*UP)
        picture_cover_book = ImageMobject("picture_cover_book.jpg")
        picture_cover_book.height = 5
        picture_cover_book.shift(2*RIGHT)
        text_winograd = Text("Shmuel Winograd", font = "Times New Roman").scale(0.5).next_to(picture_winograd, DOWN)
        life_winograd = Text("1936.1.4 - 2019.3.25").scale(0.5).next_to(text_winograd, DOWN)
        group_winograd = VGroup(text_winograd, life_winograd)
        copy_winograd = group_winograd.copy().scale(0.5, about_point = scale_center(np.array([-2, 0.5, 0]), np.array([-2.7, -0.1, 0]), 0.5)).set_opacity(0)

        self.play(ReplacementTransform(notice0, notice1))
        self.waiting(0, 10)
        
        self.play(FadeIn(picture_winograd, shift = UP), FadeIn(group_winograd, shift = UP))
        
        self.waiting(0, 28) #Shmuel Winograd 在他编写的......
        self.play(FadeIn(picture_cover_book, shift = UP))
        self.waiting(1, 8) #......《计算的算术复杂度》一书中
        self.waiting(2, 16) #提出了一种计算卷积的快速方法
        self.waiting(0, 24) #（空闲）

        time_axis = NumberLine(color = WHITE, x_range = [1950, 2030, 1], unit_size = 0.2, tick_size = 0.02, longer_tick_multiple = 5, numbers_with_elongated_ticks = np.linspace(1950, 2030, 17, endpoint = True))
        time_axis.shift(DOWN*1.7)
        group_axis = VGroup(time_axis)
        tip = Polygon(np.array([0.1, 0, 0]), np.array([-0.1, 0, 0]), np.array([0, -0.1, 0]), color = GREEN, fill_opacity = 1).shift(1.3*DOWN)

        tip1 = tip.copy().shift(2*LEFT)
        time1 = Year(1980).shift(2*LEFT+2.2*DOWN)
        group_axis.add(tip1, time1)
        anim1 = picture_winograd.animate.scale(
            0.5, 
            about_point = scale_center(np.array([-2, 0.5, 0]), np.array([-2.7, -0.1, 0]), 0.5)
        )
        anim2 = picture_cover_book.animate.scale(
            0.4, 
            about_point = scale_center(np.array([2, 0, 0]), np.array([-1.3, -0.1, 0]), 0.4)
        )

        self.play(anim1, anim2, Transform(group_winograd, copy_winograd), Write(time_axis), FadeIn(tip1, shift = DOWN), FadeIn(time1, shift = UP), run_time = 1)
        self.waiting(0, 13) #但在那时

        picture_cooley = ImageMobject("picture_cooley.jpg").set(height = 1.5).shift(5.7*LEFT)
        picture_tukey = ImageMobject("picture_tukey.jpg").set(height = 1.5).shift(4.3*LEFT)
        group_picture = Group(picture_winograd, picture_cover_book, picture_cooley, picture_tukey)
        text_cooley = Text("J.Cooley", font = "Times New Roman", stroke_width = 0.1).scale(0.5).next_to(picture_cooley, DOWN, buff = 0.1)
        text_tukey = Text("J.Tukey", font = "Times New Roman").scale(0.5).next_to(picture_tukey, DOWN, buff = 0.1)
        text_FFT = Text("快速傅立叶算法", font = 'Source Han Sans HW SC').scale(0.6).next_to(np.array([-5, 0.85, 0]), UP)
        word_FFT = Text("FFT", font = "Times New Roman").scale(0.6).next_to(text_FFT, UP)
        beams = VGroup()
        for i in range (11):
            beam_i = Line(np.array([-3.3, 0.5, 0]), np.array([-3, 0.5, 0])).rotate(((1+0.4*i)/6)*PI, about_point = np.array([-5, 0.5, 0]))
            beams.add(beam_i)
        group_name = Group(text_cooley, text_tukey, picture_cooley, picture_tukey)
        group_FFT = VGroup(text_FFT, word_FFT, beams).set_color("#FFD700")
        tip2 = tip.copy().shift(5*LEFT)
        time2 = Year(1965).shift(5*LEFT+2.2*DOWN)
        group_axis.add(tip2, time2)
        self.play(FadeIn(group_name, shift = DOWN), FadeIn(tip2, shift = DOWN), FadeIn(time2, shift = UP))
        self.waiting(0, 9) #1965年提出的......
        self.play(FadeIn(group_FFT, shift = UP), ReplacementTransform(notice1, notice2))
        self.waiting(0, 15)#......快速傅立叶算法

        slash_l = Line(np.array([-3.7, 0.5, 0]), np.array([-3.2, 0.5, 0])).rotate(2*PI/3, about_point = np.array([-5, 0.5, 0])).shift(UP)
        slash_r = Line(np.array([-3.7, 0.5, 0]), np.array([-3.2, 0.5, 0])).rotate(PI/3, about_point = np.array([-5, 0.5, 0])).shift(UP)
        text_1 = Text("卷积算法", font = 'Source Han Sans HW SC').scale(0.5).shift(5*LEFT+2.9*UP)
        praise_1 = VGroup(text_1, slash_l.copy(), slash_r.copy()).set_color("#FFFF00").rotate(PI/24, about_point = np.array([-5, 0.5, 0]))
        text_2 = Text("智慧结晶", font = 'Source Han Sans HW SC').scale(0.5).shift(5*LEFT+2.9*UP)
        praise_2 = VGroup(text_2, slash_l.copy(), slash_r.copy()).set_color("#66CCFF").rotate(-PI/12, about_point = np.array([-5, 0.5, 0]))
        text_3 = Text("美的化身", font = 'Source Han Sans HW SC').scale(0.5).shift(5*LEFT+2.9*UP)
        praise_3 = VGroup(text_3, slash_l.copy(), slash_r.copy()).set_color("#00FFCC").rotate(-PI/3, about_point = np.array([-5, 0.5, 0]))
        text_4 = Text("人类之光", font = 'Source Han Sans HW SC').scale(0.5).shift(5*LEFT+2.9*UP)
        praise_4 = VGroup(text_4, slash_l.copy(), slash_r.copy()).set_color("#9999FF").rotate(PI/6, about_point = np.array([-5, 0.5, 0]))
        text_5 = Text("最终答案", font = 'Source Han Sans HW SC').scale(0.5).shift(5*LEFT+2.9*UP)
        praise_5 = VGroup(text_5, slash_l.copy(), slash_r.copy()).set_color("#0080FF").rotate(-5*PI/24, about_point = np.array([-5, 0.5, 0]))
        text_6 = Text("唯一真神", font = 'Source Han Sans HW SC').scale(0.5).shift(5*LEFT+2.9*UP)
        praise_6 = VGroup(text_6, slash_l.copy(), slash_r.copy()).set_color("#EE82EE").rotate(PI/24, about_point = np.array([-5, 0.5, 0]))

        self.play(FadeIn(praise_1, shift = 0.5*unit(13*PI/24)), run_time = 0.6)
        self.waiting(0, 6)
        self.play(FadeOut(praise_1, shift = 0.5*unit(13*PI/24)), FadeIn(praise_2, shift = 0.5*unit(5*PI/12)), run_time = 0.6)
        self.waiting(0, 6)
        self.play(FadeOut(praise_2, shift = 0.5*unit(5*PI/12)), FadeIn(praise_3, shift = 0.5*unit(PI/6)), run_time = 0.6)
        self.waiting(0, 6)
        self.play(FadeOut(praise_3, shift = 0.5*unit(PI/6)), FadeIn(praise_4, shift = 0.5*unit(2*PI/3)), run_time = 0.6)
        self.waiting(0, 6)
        self.play(FadeOut(praise_4, shift = 0.5*unit(2*PI/3)), FadeIn(praise_5, shift = 0.5*unit(7*PI/24)), run_time = 0.6)
        self.waiting(0, 6)
        self.play(FadeOut(praise_5, shift = 0.5*unit(7*PI/24)), FadeIn(praise_6, shift = 0.5*unit(13*PI/24)), run_time = 0.6)
        self.waiting(0, 6)
        self.play(FadeOut(praise_6, shift = 0.5*unit(13*PI/24)), run_time = 0.6)
        self.waiting(1+3+0-4.2, 25+2+23-36) #已经广为人知 Winograd提出的算法并没有受到广泛的关注 （空闲）