"""Sentence -> embedding model -> vector, one sentence at a time.
Similar sentences come out with similar numbers; a different one does not.
Attaches to week3 notebook: '## 4. 임베딩: 문장을 좌표로 바꾸기'.
"""
from manimlib import *

SENTS = ["The movie was fantastic.", "The film was great.", "The sun is bright."]
VECS = ["[ 0.12,  0.75, -0.33, ... ]",
        "[ 0.14,  0.71, -0.29, ... ]",
        "[-0.65,  0.08,  0.52, ... ]"]
VCOLORS = [BLUE_B, BLUE_B, GOLD]


def sentence_box(s):
    txt = Text(s, font_size=24)
    box = RoundedRectangle(width=4.4, height=0.9, corner_radius=0.15)
    box.set_stroke(GREY_B, 1.5).set_fill(GREY_E, 0.6)
    return VGroup(box, txt.move_to(box))


def vector_pill(v, color):
    txt = Text(v, font_size=24, font="Menlo", color=color)
    box = RoundedRectangle(width=4.4, height=0.9, corner_radius=0.4)
    box.set_stroke(color, 2).set_fill(GREY_E, 0.6)
    return VGroup(box, txt.move_to(box))


class SentenceEmbedding(Scene):
    def construct(self):
        title = Text("Embedding: sentence → vector", font_size=40).to_edge(UP)
        self.play(Write(title))

        # embedding model: green diamond in the middle
        diamond = Square(2.4).rotate(PI / 4).set_stroke(GREEN_B, 2).set_fill(GREEN_E, 0.9)
        dlabel = VGroup(Text("Embedding", font_size=28, weight=BOLD),
                        Text("Model", font_size=28, weight=BOLD))
        dlabel.arrange(DOWN, buff=0.12).move_to(diamond)
        model = VGroup(diamond, dlabel).shift(DOWN * 0.4)
        self.play(FadeIn(model))

        ys = [1.4, -0.4, -2.2]
        s = 1.2 * math.sqrt(2) / 2  # half-diagonal of the rotated square
        c = diamond.get_center()
        for i, (sent, vec, vcol, y) in enumerate(zip(SENTS, VECS, VCOLORS, ys)):
            sbox = sentence_box(sent).move_to(LEFT * 4.4 + UP * y)
            # arrow targets: midpoints of the diamond's left edges (upper/middle/lower)
            tip = c + [(-s / 2, s / 2, 0), (-s, 0, 0), (-s / 2, -s / 2, 0)][i]
            out = c + [(s / 2, s / 2, 0), (s, 0, 0), (s / 2, -s / 2, 0)][i]
            a_in = Arrow(sbox.get_right(), tip, buff=0.1, stroke_width=3)
            pill = vector_pill(vec, vcol).move_to(RIGHT * 4.4 + UP * y)
            a_out = Arrow(out, pill.get_left(), buff=0.1, stroke_width=3)

            self.play(FadeIn(sbox, shift=0.2 * RIGHT))
            self.play(GrowArrow(a_in), Indicate(model, color=GREEN_B, scale_factor=1.05))
            self.play(GrowArrow(a_out), FadeIn(pill, shift=0.2 * RIGHT))
            self.wait(0.2)
            if i == 0:
                pills = [pill]
            else:
                pills.append(pill)

        # similar meaning -> similar numbers
        rect12 = SurroundingRectangle(VGroup(pills[0], pills[1]), buff=0.12).set_stroke(BLUE, 3)
        lab12 = Text("similar", font_size=24, color=BLUE_B).next_to(rect12, UP, buff=0.12)
        self.play(ShowCreation(rect12), FadeIn(lab12))
        rect3 = SurroundingRectangle(pills[2], buff=0.12).set_stroke(GOLD, 3)
        lab3 = Text("different", font_size=24, color=GOLD).next_to(rect3, DOWN, buff=0.12)
        self.play(ShowCreation(rect3), FadeIn(lab3))

        self.wait(1.5)
