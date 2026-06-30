"""실전 예제 ① 감정 분석 — 파이프라인 Overview (flow).
문장 -> 토큰화 -> 인덱스 -> Embedding(L,D) -> 평균 풀링(D) -> Linear -> sigmoid -> 긍/부정.
Attaches to the Sentiment Analysis example section.
"""
from manimlib import *

TOK_C = BLUE_D
EMB_C = TEAL_D


def small_box(label, color, w=1.0, h=0.7, fs=24):
    box = Rectangle(width=w, height=h).set_stroke(WHITE, 1.3).set_fill(color, 0.25)
    t = Text(str(label), font_size=fs).move_to(box)
    return VGroup(box, t)


def op_arrow(a, b, text):
    arr = Arrow(a.get_right(), b.get_left(), buff=0.15, stroke_width=3)
    lab = Text(text, font_size=18, color=YELLOW).next_to(arr, UP, buff=0.08)
    return VGroup(arr, lab)


class SentimentOverview(Scene):
    def construct(self):
        title = Text("Sentiment analysis — overview", font_size=40).to_edge(UP)
        self.play(Write(title))

        # 1) sentence
        sent = small_box("a fantastic movie", GREY_D, w=2.6, h=0.8, fs=22)
        sent.to_edge(LEFT, buff=0.4).shift(UP * 0.3)

        # 2) token indices (L,)
        idxs = VGroup(small_box(3, TOK_C, w=0.6), small_box(12, TOK_C, w=0.6),
                      small_box(27, TOK_C, w=0.6)).arrange(DOWN, buff=0.08)
        idxs.next_to(sent, RIGHT, buff=1.4)
        idx_shape = Tex("(L,)", font_size=26).next_to(idxs, DOWN, buff=0.15)

        # 3) embedding matrix (L, D)
        emb = VGroup(*[Square(0.32).set_stroke(WHITE, 1).set_fill(EMB_C, 0.3)
                       for _ in range(3 * 5)]).arrange_in_grid(3, 5, buff=0.06)
        emb.next_to(idxs, RIGHT, buff=1.5)
        emb_shape = Tex("(L, D)", font_size=26).next_to(emb, DOWN, buff=0.15)

        # 4) pooled sentence vector (D,)
        pooled = VGroup(*[Square(0.32).set_stroke(WHITE, 1).set_fill(EMB_C, 0.5)
                          for _ in range(5)]).arrange(DOWN, buff=0.06)
        pooled.next_to(emb, RIGHT, buff=1.6)
        pooled_shape = Tex("(D,)", font_size=26).next_to(pooled, DOWN, buff=0.15)

        # 5) output prob
        out = small_box("0.92", GREEN_D, w=1.1, h=0.8, fs=26)
        out.next_to(pooled, RIGHT, buff=1.4)
        out_lab = Text("positive", font_size=22, color=GREEN).next_to(out, DOWN, buff=0.15)

        pipeline = VGroup(sent, idxs, emb, pooled, out)
        pipeline.set_width(12.8).move_to(DOWN * 0.2)
        for s, anchor in [(idx_shape, idxs), (emb_shape, emb), (pooled_shape, pooled)]:
            s.next_to(anchor, DOWN, buff=0.15)
        out_lab.next_to(out, DOWN, buff=0.15)

        a1 = op_arrow(sent, idxs, "tokenize\n+ encode")
        a2 = op_arrow(idxs, emb, "Embedding")
        a3 = op_arrow(emb, pooled, "mean pool")
        a4 = op_arrow(pooled, out, "Linear\n+ sigmoid")

        # Flow, stage by stage
        self.play(FadeIn(sent))
        self.play(GrowArrow(a1[0]), FadeIn(a1[1]), FadeIn(idxs, lag_ratio=0.2), FadeIn(idx_shape))
        self.play(GrowArrow(a2[0]), FadeIn(a2[1]),
                  TransformFromCopy(idxs, emb), FadeIn(emb_shape))
        self.wait(0.2)
        # mean pool highlight: rows collapse into one vector
        brace = Brace(emb, LEFT, buff=0.1)
        btext = brace.get_text("mean\nover L").scale(0.6)
        self.play(GrowFromCenter(brace), FadeIn(btext))
        self.play(GrowArrow(a3[0]), FadeIn(a3[1]),
                  TransformFromCopy(emb, pooled), FadeIn(pooled_shape))
        self.play(Indicate(pooled, color=YELLOW))
        self.play(FadeOut(brace), FadeOut(btext))
        self.play(GrowArrow(a4[0]), FadeIn(a4[1]), FadeIn(out), FadeIn(out_lab))
        self.play(Indicate(out, color=GREEN, scale_factor=1.2))

        key = Text("sentence = average of word embeddings  ->  sentiment score",
                   font_size=26).to_edge(DOWN)
        self.play(FadeIn(key))
        self.wait(1.4)
