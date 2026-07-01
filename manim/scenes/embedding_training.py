"""Embedding training as migration: 'jordan' occurrences start mixed, then during
training the window (context) pushes location-uses to one side and person-uses to
the other — animating the PCA result (green LOCATION left, red person right).
Attaches to notebook: WW bonus '임베딩이 학습한 문맥 들여다보기'.
"""
from manimlib import *
import numpy as np

LOC = GREEN
PER = RED


def P(x, y):
    return np.array([x, y, 0.0])


class EmbeddingTraining(Scene):
    def construct(self):
        title = Text("The window teaches the embedding (training)", font_size=34).to_edge(UP)
        self.play(Write(title))

        locside = Text("LOCATION side", font_size=22, color=LOC).to_corner(UL).shift(DOWN * 1.2)
        perside = Text("person side", font_size=22, color=PER).to_corner(UR).shift(DOWN * 1.2)
        self.play(FadeIn(locside), FadeIn(perside))

        greens_s = [P(-0.8, 1.2), P(0.9, 0.3), P(-0.3, -1.0), P(1.2, 1.4), P(0.2, -0.5)]
        greens_t = [P(-2.5, 1.4 - 0.7 * i) for i in range(5)]
        reds_s = [P(0.6, 1.0), P(-1.1, 0.5), P(0.4, 1.5), P(-0.6, -1.3), P(1.1, -0.9)]
        reds_t = [P(2.5, 1.4 - 0.7 * i) for i in range(5)]

        gdots = VGroup(*[Dot(s, radius=0.14).set_fill(LOC, 1).set_stroke(WHITE, 1.5) for s in greens_s])
        rdots = VGroup(*[Dot(s, radius=0.14).set_fill(PER, 1).set_stroke(WHITE, 1.5) for s in reds_s])

        # a couple of context labels that follow their dots
        def follow(dot, text, direction):
            lab = Text(text, font_size=18).next_to(dot, direction, buff=0.1)
            lab.add_updater(lambda m, d=dot, dr=direction: m.next_to(d, dr, buff=0.1))
            return lab
        labs = VGroup(
            follow(gdots[0], "to jordan", LEFT),
            follow(gdots[3], "of jordan is", LEFT),
            follow(rdots[0], "michael jordan", RIGHT),
            follow(rdots[3], "jordan passed", RIGHT),
        )

        epoch = Text("epoch 0  (random init — mixed)", font_size=26).next_to(title, DOWN, buff=0.2)
        self.play(FadeIn(epoch), ShowCreation(gdots), ShowCreation(rdots), FadeIn(labs))
        self.wait(0.6)

        stages = [(0.45, "training…"), (0.78, "training…"), (1.0, "trained — two clear clusters")]
        for alpha, msg in stages:
            new_epoch = Text(f"epoch → {msg}", font_size=26).move_to(epoch)
            anims = []
            for d, s, t in zip(gdots, greens_s, greens_t):
                anims.append(d.animate.move_to(s + alpha * (t - s)))
            for d, s, t in zip(rdots, reds_s, reds_t):
                anims.append(d.animate.move_to(s + alpha * (t - s)))
            self.play(*anims, Transform(epoch, new_epoch), run_time=1.2)
            self.wait(0.2)

        # highlight the two clusters
        gbox = SurroundingRectangle(gdots, buff=0.25).set_stroke(LOC, 3)
        rbox = SurroundingRectangle(rdots, buff=0.25).set_stroke(PER, 3)
        self.play(ShowCreation(gbox), ShowCreation(rbox))
        key = Text("same word 'jordan' — its window decides which side",
                   font_size=26, color=YELLOW).to_edge(DOWN)
        self.play(FadeIn(key))
        self.wait(1.5)
