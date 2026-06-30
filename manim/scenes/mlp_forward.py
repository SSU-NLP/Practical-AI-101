"""MLP forward pass: Linear(5->3) -> ReLU -> Linear(3->5) -> Sigmoid.
Shows the WHOLE pipeline at once, then highlights each stage in turn,
revealing how the values propagate to the final output.
Attaches to notebook: '### 커스텀 모듈 (Custom Modules)' MultilayerPerceptron.
"""
from manimlib import *
import numpy as np


def cell_color(v):
    if abs(v) < 1e-9:
        return GREY
    return BLUE_D if v > 0 else RED_D


def make_vec(values, cell=0.52, hide=False):
    g = VGroup()
    for v in values:
        sq = Square(cell).set_stroke(WHITE, 1.3).set_fill(cell_color(v), 0.28)
        n = DecimalNumber(v, num_decimal_places=1).scale(cell * 0.85).move_to(sq)
        if hide:
            n.set_opacity(0)
        g.add(VGroup(sq, n))
    g.arrange(DOWN, buff=0.07)
    return g


def make_block(text):
    label = Text(text, font_size=22)
    box = RoundedRectangle(width=label.get_width() + 0.45, height=1.05, corner_radius=0.12)
    box.set_fill(GREY_E, 1).set_stroke(GREY_B, 2)
    label.move_to(box)
    return VGroup(box, label)


class MLPForward(Scene):
    def construct(self):
        x = [0.5, -1.2, 0.8, -0.3, 1.0]
        h = [1.4, -0.7, 0.2]
        hr = [1.4, 0.0, 0.2]
        z = [0.3, -2.0, 1.1, 0.0, -0.5]
        y = [round(float(1 / (1 + np.exp(-v))), 1) for v in z]

        title = Text("MLP forward pass", font_size=42).to_edge(UP)
        self.play(Write(title))

        vecs = [make_vec(x), make_vec(h, hide=True), make_vec(hr, hide=True),
                make_vec(z, hide=True), make_vec(y, hide=True)]
        blocks = [make_block("Linear\n5 -> 3"), make_block("ReLU"),
                  make_block("Linear\n3 -> 5"), make_block("Sigmoid")]
        shapes = ["(5,)", "(3,)", "(3,)", "(5,)", "(5,)"]

        row = VGroup(vecs[0], blocks[0], vecs[1], blocks[1], vecs[2],
                     blocks[2], vecs[3], blocks[3], vecs[4])
        row.arrange(RIGHT, buff=0.28)
        row.set_width(13).move_to(DOWN * 0.3)

        shp_labels = VGroup()
        for v, s in zip(vecs, shapes):
            t = Tex(s, font_size=28).next_to(v, DOWN, buff=0.18)
            shp_labels.add(t)

        arrows = VGroup()
        for a, b in zip(row[:-1], row[1:]):
            arrows.add(Arrow(a.get_right(), b.get_left(), buff=0.08,
                             stroke_width=3, tip_width_ratio=4))

        # 1) Show the whole pipeline at once (input values visible, rest blank).
        self.play(
            FadeIn(VGroup(*blocks)),
            ShowCreation(arrows, lag_ratio=0.1),
            FadeIn(VGroup(*vecs)),
            FadeIn(shp_labels),
        )
        in_lab = Text("input", font_size=24).next_to(vecs[0], UP, buff=0.2)
        self.play(FadeIn(in_lab), Indicate(vecs[0], scale_factor=1.08))
        self.wait(0.4)

        notes = ["weighted sum + bias", "negatives -> 0",
                 "weighted sum + bias", "squash into (0, 1)"]

        # 2) Sweep the highlight stage by stage, revealing each output.
        for k in range(4):
            blk = blocks[k]
            note = Text(notes[k], font_size=24, color=YELLOW).next_to(blk, UP, buff=0.25)
            self.play(
                blk[0].animate.set_stroke(YELLOW, 4).set_fill(YELLOW, 0.12),
                FadeIn(note, shift=0.1 * DOWN),
                run_time=0.5,
            )
            out = vecs[k + 1]
            self.play(LaggedStart(*[c[1].animate.set_opacity(1) for c in out],
                                  lag_ratio=0.12), run_time=0.7)
            if k == 1:  # ReLU: emphasise the clamped entry
                zeros = VGroup(*[c for c, v in zip(out, hr) if abs(v) < 1e-9])
                self.play(LaggedStart(*[Indicate(c, color=RED) for c in zeros], lag_ratio=0.1))
            self.play(blk[0].animate.set_stroke(GREY_B, 2).set_fill(GREY_E, 1),
                      FadeOut(note), run_time=0.4)

        # 3) Final output.
        out_lab = Text("output", font_size=26, color=GREEN)
        out_lab.next_to(vecs[4], UP, buff=0.2)
        box = SurroundingRectangle(vecs[4], buff=0.12).set_stroke(GREEN, 3)
        self.play(FadeIn(out_lab), ShowCreation(box), Indicate(vecs[4], color=GREEN, scale_factor=1.1))

        legend = VGroup(
            Square(0.28).set_fill(BLUE_D, 0.4).set_stroke(WHITE, 1), Text("positive", font_size=22),
            Square(0.28).set_fill(RED_D, 0.4).set_stroke(WHITE, 1), Text("negative", font_size=22),
            Square(0.28).set_fill(GREY, 0.4).set_stroke(WHITE, 1), Text("zero", font_size=22),
        ).arrange(RIGHT, buff=0.18).scale(0.95).to_edge(DOWN)
        self.play(FadeIn(legend))
        self.wait(1.4)
