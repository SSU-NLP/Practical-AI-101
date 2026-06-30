"""실전 예제 ② Word Window Classification — 아키텍처 Overview (flow).
토큰 시퀀스 위를 슬라이딩 윈도우(2S+1)가 미끄러지며 각 단어를 분류:
window -> embed (S,D) -> flatten (S*D) -> Linear+Tanh (H) -> Linear+sigmoid -> per-word prob.
Attaches to the Word Window Classification example section.
"""
from manimlib import *

TOK_C = BLUE_D
EMB_C = TEAL_D
HID_C = PURPLE_B


def tok_box(label, color=TOK_C, w=0.95, h=0.7, fs=20):
    box = Rectangle(width=w, height=h).set_stroke(WHITE, 1.3).set_fill(color, 0.25)
    t = Text(str(label), font_size=fs).move_to(box)
    return VGroup(box, t)


class WordWindowOverview(Scene):
    def construct(self):
        title = Text("Word window classification — overview", font_size=38).to_edge(UP)
        self.play(Write(title))

        toks = ["<pad>", "We", "always", "come", "to", "Paris", "<pad>"]
        row = VGroup(*[tok_box(t, GREY_D if t == "<pad>" else TOK_C) for t in toks])
        row.arrange(RIGHT, buff=0.12).shift(UP * 1.9)
        self.play(LaggedStartMap(FadeIn, row, lag_ratio=0.1))
        note = Text("window size S=1  ->  2S+1 = 3 tokens", font_size=22, color=YELLOW)
        note.next_to(row, DOWN, buff=0.25)
        self.play(FadeIn(note))

        centers = list(range(1, 6))           # real-word positions in `toks`
        probs = [0.05, 0.02, 0.08, 0.15, 0.95]

        win = SurroundingRectangle(VGroup(row[0], row[1], row[2]), buff=0.06)
        win.set_stroke(YELLOW, 4)
        prob_row = [None] * len(toks)

        self.play(ShowCreation(win))
        for k, c in enumerate(centers):
            target = SurroundingRectangle(VGroup(row[c - 1], row[c], row[c + 1]), buff=0.06)
            target.set_stroke(YELLOW, 4)
            self.play(Transform(win, target), run_time=0.35)
            col = GREEN if probs[k] > 0.5 else GREY_B
            p = tok_box(f"{probs[k]:.2f}", col, w=0.95, h=0.55, fs=18)
            p.next_to(row[c], DOWN, buff=1.0)
            prob_row[c] = p
            self.play(FadeIn(p, shift=0.2 * DOWN), run_time=0.3)
        self.wait(0.3)

        # Expand the pipeline for the "Paris" window (the high-scoring one).
        self.play(win.animate.set_stroke(GREEN, 4),
                  Indicate(prob_row[5], color=GREEN, scale_factor=1.2))

        fw = VGroup(tok_box("to", w=0.8, h=0.6, fs=18),
                    tok_box("Paris", w=0.8, h=0.6, fs=18),
                    tok_box("<pad>", GREY_D, w=0.8, h=0.6, fs=16)).arrange(DOWN, buff=0.07)
        emb = VGroup(*[Square(0.28).set_stroke(WHITE, 1).set_fill(EMB_C, 0.3)
                       for _ in range(3 * 4)]).arrange_in_grid(3, 4, buff=0.05)
        flat = VGroup(*[Square(0.26).set_stroke(WHITE, 1).set_fill(EMB_C, 0.4)
                        for _ in range(6)]).arrange(DOWN, buff=0.05)
        hid = VGroup(*[Square(0.30).set_stroke(WHITE, 1).set_fill(HID_C, 0.4)
                       for _ in range(4)]).arrange(DOWN, buff=0.05)
        prob = tok_box("0.95", GREEN_D, w=1.0, h=0.7, fs=24)

        stages = VGroup(fw, emb, flat, hid, prob).arrange(RIGHT, buff=1.25)
        stages.set_width(12.5).to_edge(DOWN, buff=1.0)

        labels = ["embed", "flatten", "Linear\n+Tanh", "Linear\n+sigmoid"]
        shapes = ["(S,)", "(S, D)", "(S·D,)", "(H,)", "prob"]
        arrows = VGroup()
        for a, b, lab in zip(stages[:-1], stages[1:], labels):
            ar = Arrow(a.get_right(), b.get_left(), buff=0.12, stroke_width=3)
            lb = Text(lab, font_size=16, color=YELLOW).next_to(ar, UP, buff=0.06)
            arrows.add(VGroup(ar, lb))
        shp = VGroup(*[Tex(s, font_size=22).next_to(st, DOWN, buff=0.12)
                       for s, st in zip(shapes, stages)])

        self.play(TransformFromCopy(VGroup(row[4], row[5], row[6]), fw))
        self.play(FadeIn(shp[0]))
        for i in range(4):
            self.play(GrowArrow(arrows[i][0]), FadeIn(arrows[i][1]),
                      TransformFromCopy(stages[i], stages[i + 1]), FadeIn(shp[i + 1]),
                      run_time=0.6)
        self.play(Indicate(prob, color=GREEN, scale_factor=1.2))
        loc = Text("LOCATION", font_size=22, color=GREEN).next_to(prob, UP, buff=0.2)
        self.play(FadeIn(loc))
        self.wait(1.4)
