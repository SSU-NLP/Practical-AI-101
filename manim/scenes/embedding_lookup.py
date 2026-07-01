"""Embedding lookup table: word -> index -> row of the table -> embedding vector.
Makes nn.Embedding concrete: it is just a learnable table you index into.
Attaches to notebook: '### 단어를 임베딩으로 변환하기'.
"""
from manimlib import *

D = 5
WORDS = ["<pad>", "michael", "to", "jordan", "scored", "paris"]
ROWS = {
    "<pad>":   [0.0, 0.0, 0.0, 0.0, 0.0],
    "michael": [0.8, -0.3, 0.1, 0.6, -0.2],
    "to":      [-0.4, 0.2, 0.9, -0.1, 0.3],
    "jordan":  [0.5, 0.7, -0.6, 0.2, -0.9],
    "scored":  [0.3, -0.8, 0.2, 0.7, 0.1],
    "paris":   [-0.7, 0.4, 0.5, -0.3, 0.8],
}
KEY = "jordan"


def cell_color(v):
    if abs(v) < 1e-9:
        return GREY
    return BLUE_D if v > 0 else RED_D


def cell(v, size=0.55):
    sq = Square(size).set_stroke(WHITE, 1.2).set_fill(cell_color(v), 0.32)
    n = DecimalNumber(v, num_decimal_places=1).scale(size * 0.8).move_to(sq)
    return VGroup(sq, n)


class EmbeddingLookup(Scene):
    def construct(self):
        title = Text("nn.Embedding = a lookup table", font_size=40).to_edge(UP)
        self.play(Write(title))

        # The embedding table E (vocab rows x D columns), with word row-labels.
        rows = VGroup(*[VGroup(*[cell(v) for v in ROWS[w]]).arrange(RIGHT, buff=0.06)
                        for w in WORDS]).arrange(DOWN, buff=0.12)
        rows.move_to(RIGHT * 2.2 + DOWN * 0.2)
        labels = VGroup(*[Text(w, font_size=22).next_to(r, LEFT, buff=0.35)
                          for w, r in zip(WORDS, rows)])
        idxcol = VGroup(*[Text(str(i), font_size=20, color=GREY_B).next_to(labels[i], LEFT, buff=0.35)
                          for i in range(len(WORDS))])
        tbl_brace = Brace(rows, UP, buff=0.1)
        tbl_lab = Tex(R"E \in \mathbb{R}^{V \times D}", font_size=34).next_to(tbl_brace, UP, SMALL_BUFF)

        self.play(FadeIn(idxcol), FadeIn(labels),
                  FadeIn(rows, lag_ratio=0.02), GrowFromCenter(tbl_brace), FadeIn(tbl_lab))
        self.wait(0.3)

        ki = WORDS.index(KEY)
        # 1) word
        word = Text(f'"{KEY}"', font_size=40, color=YELLOW).to_edge(LEFT, buff=0.6).shift(UP * 1.5)
        self.play(FadeIn(word, shift=0.2 * RIGHT))

        # 2) word -> index
        a1 = Arrow(word.get_bottom(), word.get_bottom() + DOWN * 1.0, buff=0.15, stroke_width=3)
        a1lab = Text("word_to_ix", font_size=20, color=YELLOW).next_to(a1, RIGHT, buff=0.1)
        idxbox = VGroup(Square(0.8).set_stroke(YELLOW, 2.5).set_fill(GREY_E, 1),
                        Text(str(ki), font_size=34, color=YELLOW))
        idxbox.arrange(ORIGIN).next_to(a1, DOWN, buff=0.15)
        idx_cap = Text("index", font_size=20).next_to(idxbox, DOWN, buff=0.1)
        self.play(GrowArrow(a1), FadeIn(a1lab))
        self.play(FadeIn(idxbox), FadeIn(idx_cap))
        self.wait(0.3)

        # 3) index selects the matching row
        rowsel = SurroundingRectangle(VGroup(idxcol[ki], labels[ki], rows[ki]), buff=0.08).set_stroke(YELLOW, 4)
        a2 = Arrow(idxbox.get_right(), rows[ki].get_left() + LEFT * 0.1, buff=0.2, stroke_width=3).set_color(YELLOW)
        self.play(GrowArrow(a2), ShowCreation(rowsel))
        self.play(Indicate(rows[ki], color=YELLOW))
        self.wait(0.3)

        # 4) that row IS the embedding vector -> pull it out
        vec = VGroup(*[cell(v, 0.65) for v in ROWS[KEY]]).arrange(RIGHT, buff=0.08)
        vec.to_edge(DOWN, buff=0.9)
        veclab = Tex(R"\vec{e}_{\text{jordan}} \in \mathbb{R}^{D}", font_size=32).next_to(vec, LEFT, buff=0.3)
        self.play(TransformFromCopy(rows[ki], vec), FadeIn(veclab))
        self.play(Indicate(vec, color=YELLOW))

        note = Text("the rows are parameters — learned during training",
                    font_size=24, color=GREEN).next_to(title, DOWN, buff=0.2)
        self.play(FadeIn(note))
        self.wait(1.4)
