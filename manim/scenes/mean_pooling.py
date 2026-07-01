"""Mean pooling as arrows: a sentence becomes several 'mood' vectors; averaging
them = the center of mass = the sentence's overall mood. Also: averaging turns
any length into ONE vector, but ignores word order ('not good' -> wrong).
Attaches to notebook: sentiment '임베딩 평균 풀링' model section.
"""
from manimlib import *
import numpy as np

POS = GREEN
NEG = RED
AVG = YELLOW
O = LEFT * 2.3 + DOWN * 0.4
SCALE = 1.1


def vpoint(v):
    return O + SCALE * np.array([v[0], v[1], 0.0])


class MeanPooling(Scene):
    def construct(self):
        title = Text("Mean pooling = average of word vectors", font_size=36).to_edge(UP)
        self.play(Write(title))

        # faint mood-space orientation
        posz = Text("positive", font_size=22, color=POS).move_to(vpoint((2.5, 1.9)))
        negz = Text("negative", font_size=22, color=NEG).move_to(vpoint((-1.3, -1.5)))
        dot0 = Dot(O, radius=0.05, color=GREY_B)
        self.play(FadeIn(posz), FadeIn(negz), FadeIn(dot0))

        # 1) each word -> one 'mood' arrow
        words = ["an", "amazing", "fun", "movie"]
        vecs = [(0.4, 0.25), (2.1, 1.5), (1.5, 1.15), (0.6, -0.2)]
        cols = [GREY_B, POS, POS, GREY_B]
        arrows, labels = VGroup(), VGroup()
        for w, v, c in zip(words, vecs, cols):
            a = Arrow(O, vpoint(v), buff=0, stroke_width=4).set_color(c)
            lab = Text(w, font_size=20, color=c).next_to(a.get_end(), UR, buff=0.05)
            arrows.add(a); labels.add(lab)

        sent = Text('"an amazing fun movie"  →  4 word vectors', font_size=26)
        sent.next_to(title, DOWN, buff=0.2)
        self.play(FadeIn(sent))
        for a, lab in zip(arrows, labels):
            self.play(GrowArrow(a), FadeIn(lab), run_time=0.5)
        self.wait(0.3)

        # 2) but we need ONE answer
        q = VGroup(
            Text("but we must answer ONE thing:", font_size=26),
            Text("positive or negative?", font_size=26, color=YELLOW),
            Text("→ combine 4 vectors into 1", font_size=24, color=GREY_B),
            Text("(like averaging 4 friends' ratings)", font_size=22, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.6).shift(UP * 0.3)
        self.play(FadeIn(q, lag_ratio=0.2))
        self.wait(0.4)

        # 3) average = center of mass of the tips
        tips = VGroup(*[Dot(a.get_end(), radius=0.06, color=a.get_color()) for a in arrows])
        self.play(FadeOut(labels), ShowCreation(tips))
        avg = np.mean(np.array(vecs), axis=0)
        cdot = Dot(vpoint(avg), radius=0.09, color=AVG)
        spokes = VGroup(*[DashedLine(t.get_center(), cdot.get_center(), stroke_width=1.5).set_color(GREY)
                          for t in tips])
        self.play(ShowCreation(spokes), FadeIn(cdot))
        avg_arrow = Arrow(O, vpoint(avg), buff=0, stroke_width=7).set_color(AVG)
        self.play(GrowArrow(avg_arrow), FadeOut(spokes))
        avg_lab = Text("average = center of mass = overall mood", font_size=24, color=AVG)
        avg_lab.next_to(title, DOWN, buff=0.2)
        self.play(FadeTransform(sent, avg_lab), Indicate(avg_arrow, color=AVG))
        verdict = Text("leans positive  →  POSITIVE", font_size=26, color=POS).move_to(q).shift(DOWN * 1.6)
        self.play(FadeIn(verdict))
        self.wait(0.6)

        # 4) any length -> ONE vector
        self.play(FadeOut(q), FadeOut(verdict), FadeOut(tips))
        length_note = Text("3 words or 30 words -> always ONE vector\n(fixes variable sentence length)",
                           font_size=24, color=GREY_B).to_edge(RIGHT, buff=0.5).shift(UP * 0.5)
        self.play(FadeIn(length_note))
        self.wait(0.8)

        # 5) honest caveat: order is ignored
        self.play(FadeOut(length_note))
        cav = VGroup(
            Text("⚠ average ignores word ORDER", font_size=26, color=RED),
            Text('"not good" averages to positive', font_size=24),
            Text("→ that's what attention fixes (later)", font_size=24, color=TEAL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.5)
        self.play(FadeIn(cav, lag_ratio=0.2))
        self.wait(1.4)
