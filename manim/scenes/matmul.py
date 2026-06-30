"""Matrix multiplication: (3,2) @ (2,4) -> (3,4).
Row . column dot products; the inner dimension cancels.
Attaches to notebook cell ~19: a.matmul(b) / a @ b.
"""
from manimlib import *
import numpy as np

A_C = BLUE_B
B_C = GREEN_B


class MatMul(Scene):
    def construct(self):
        A = np.array([[1, 2], [0, 1], [2, 1]])      # (3,2)
        B = np.array([[1, 0, 2, 1], [3, 1, 0, 2]])  # (2,4)
        C = A @ B                                    # (3,4)

        mA = IntegerMatrix(A); mA.get_entries().set_color(A_C)
        mB = IntegerMatrix(B); mB.get_entries().set_color(B_C)
        mC = IntegerMatrix(C)
        for m in (mA, mB, mC):
            m.set_height(2.2)
        at = Tex("@", font_size=48)
        eq = Tex("=", font_size=48)
        group = VGroup(mA, at, mB, eq, mC).arrange(RIGHT, buff=0.3)
        group.center().shift(DOWN * 0.4)

        # Shape annotation; t2c colors the two inner dims (the matching 2s) yellow.
        shape = Tex(R"(3,2) @ (2,4) \rightarrow (3,4)", t2c={"2": YELLOW},
                    font_size=44).to_edge(UP)
        self.play(Write(shape))
        self.play(FadeIn(mA), FadeIn(at), FadeIn(mB))
        self.play(Indicate(shape, color=YELLOW, scale_factor=1.1))
        inner = Text("inner dims match -> they cancel", font_size=28, color=YELLOW)
        inner.next_to(shape, DOWN, buff=0.2)
        self.play(FadeIn(inner))
        self.wait(0.3)
        self.play(FadeIn(eq), Write(mC.get_brackets()))

        entries = mC.get_entries()
        for e in entries:
            e.set_opacity(0)
        rowsA = mA.get_rows()
        colsB = mB.get_columns()

        def rects(i, j):
            r = SurroundingRectangle(rowsA[i], buff=0.05).set_stroke(A_C, 3)
            c = SurroundingRectangle(colsB[j], buff=0.05).set_stroke(B_C, 3)
            return r, c

        # First cell (0,0) in detail with the dot-product formula.
        r, c = rects(0, 0)
        terms = R" + ".join(fR"{A[0][k]}\cdot{B[k][0]}" for k in range(2))
        formula = Tex(terms + fR" = {C[0][0]}", font_size=40).to_edge(DOWN)
        self.play(ShowCreation(r), ShowCreation(c))
        self.play(Write(formula))
        self.play(entries[0].animate.set_opacity(1).set_color(YELLOW))
        self.play(Indicate(entries[0], color=YELLOW))
        self.wait(0.3)
        self.play(FadeOut(formula))

        # Remaining cells, faster sweep.
        last = VGroup(r, c)
        for i in range(3):
            for j in range(4):
                if i == 0 and j == 0:
                    continue
                r, c = rects(i, j)
                self.play(FadeOut(last), ShowCreation(r), ShowCreation(c), run_time=0.25)
                self.play(entries[i * 4 + j].animate.set_opacity(1), run_time=0.2)
                last = VGroup(r, c)
        self.play(FadeOut(last))
        self.play(Indicate(mC, color=YELLOW, scale_factor=1.05))
        self.wait(1.2)
