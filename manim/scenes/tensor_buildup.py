"""텐서 빌드업: 스칼라 -> 벡터 -> 행렬 -> 3D 텐서.
숫자를 모으면 벡터, 벡터(컬럼)를 모으면 행렬, 행렬을 모으면 3D 텐서.
Attaches to notebook: '## Part 1: 텐서 (Tensors)'.
"""
from manimlib import *

SC = BLUE_B
VC = BLUE_D
MC = TEAL_D
TC = GREEN_D


def cell(val=None, color=BLUE_D, size=0.6, fill=0.3):
    sq = Square(size).set_stroke(WHITE, 1.3).set_fill(color, fill)
    if val is None:
        return VGroup(sq)
    n = Integer(val).scale(size * 0.95).move_to(sq)
    return VGroup(sq, n)


def grid(rows, cols, color, size=0.55):
    g = VGroup(*[cell(color=color, size=size) for _ in range(rows * cols)])
    g.arrange_in_grid(rows, cols, buff=0.06)
    return g


def caption(name, shape, rank, anchor):
    t = VGroup(
        Text(name, font_size=24),
        Tex(shape, font_size=26),
        Text(rank, font_size=20, color=GREY_B),
    ).arrange(DOWN, buff=0.1)
    t.next_to(anchor, DOWN, buff=0.3)
    return t


class TensorBuildup(Scene):
    def construct(self):
        title = Text("Tensors: stacking up dimensions", font_size=40).to_edge(UP)
        self.play(Write(title))

        # Scalar
        scalar = cell(7, SC).move_to(LEFT * 5.6 + UP * 0.3)
        sc_cap = caption("scalar", "(\\,)", "rank 0", scalar)
        self.play(FadeIn(scalar), FadeIn(sc_cap))
        self.wait(0.3)

        # Vector = stack scalars into a column
        vec = VGroup(cell(7, VC), cell(3, VC), cell(9, VC)).arrange(DOWN, buff=0.06)
        vec.move_to(LEFT * 3.2 + UP * 0.3)
        vc_cap = caption("vector", "(3,)", "rank 1", vec)
        a1 = Arrow(scalar.get_right(), vec.get_left(), buff=0.25, stroke_width=3)
        a1l = Text("stack\nnumbers", font_size=18, color=YELLOW).next_to(a1, UP, buff=0.05)
        self.play(GrowArrow(a1), FadeIn(a1l))
        self.play(TransformFromCopy(scalar, vec), FadeIn(vc_cap))
        self.wait(0.3)

        # Matrix = stack column-vectors side by side
        mat = grid(3, 2, MC).move_to(LEFT * 0.4 + UP * 0.3)
        mt_cap = caption("matrix", "(3, 2)", "rank 2", mat)
        a2 = Arrow(vec.get_right(), mat.get_left(), buff=0.25, stroke_width=3)
        a2l = Text("stack\ncolumns", font_size=18, color=YELLOW).next_to(a2, UP, buff=0.05)
        self.play(GrowArrow(a2), FadeIn(a2l))
        self.play(TransformFromCopy(vec, mat), FadeIn(mt_cap))
        self.wait(0.3)

        # 3D tensor = stack matrices in depth (faux-3D with offset copies)
        m_back = grid(3, 2, TC).set_fill(TC, 0.18)
        m_front = grid(3, 2, TC)
        m_back.shift(UP * 0.32 + RIGHT * 0.32)
        depth = VGroup(m_back, m_front)
        depth.move_to(RIGHT * 4.0 + UP * 0.3)
        ten_cap = caption("3D tensor", "(2, 3, 2)", "rank 3", depth)
        a3 = Arrow(mat.get_right(), depth.get_left(), buff=0.25, stroke_width=3)
        a3l = Text("stack\nmatrices", font_size=18, color=YELLOW).next_to(a3, UP, buff=0.05)
        self.play(GrowArrow(a3), FadeIn(a3l))
        self.play(TransformFromCopy(mat, m_front))
        self.play(TransformFromCopy(m_front, m_back), FadeIn(ten_cap))
        self.play(Indicate(depth, scale_factor=1.06))

        key = Text("a tensor is just a multi-dimensional array of numbers",
                   font_size=26).to_edge(DOWN)
        self.play(FadeIn(key))
        self.wait(1.4)
