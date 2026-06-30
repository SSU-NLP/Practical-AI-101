"""Broadcasting: (3,1) + (1,4) -> (3,4).
Shows the size-1 dimension being physically stretched, then element-wise add.
Attaches to notebook: '### 브로드캐스팅 (Broadcasting)'.
"""
from manimlib import *

COL_C = BLUE_D
ROW_C = GREEN_D
SUM_C = YELLOW


def num_cell(val, color, size=0.85, fill=0.22):
    sq = Square(side_length=size)
    sq.set_stroke(WHITE, 1.5)
    sq.set_fill(color, fill)
    n = Integer(int(val)).scale(0.7).move_to(sq)
    return VGroup(sq, n)


class Broadcasting(Scene):
    def construct(self):
        col_vals = [10, 20, 30]      # shape (3,1)
        row_vals = [1, 2, 3, 4]      # shape (1,4)

        title = Text("Broadcasting", font_size=48).to_edge(UP)
        shape = Tex(R"(3,1) + (1,4) \;\rightarrow\; (3,4)", font_size=40)
        shape.next_to(title, DOWN, buff=0.2)
        self.play(Write(title))
        self.play(FadeIn(shape, shift=0.2 * DOWN))

        # Originals
        col = VGroup(*[num_cell(v, COL_C) for v in col_vals]).arrange(DOWN, buff=0.12)
        col.move_to(LEFT * 4.7 + DOWN * 0.4)
        col_lab = Tex(R"(3,1)", font_size=30).next_to(col, DOWN, buff=0.2)

        row = VGroup(*[num_cell(v, ROW_C) for v in row_vals]).arrange(RIGHT, buff=0.12)
        row.move_to(LEFT * 1.0 + UP * 1.4)
        row_lab = Tex(R"(1,4)", font_size=30).next_to(row, LEFT, buff=0.3)

        self.play(FadeIn(col, lag_ratio=0.2), Write(col_lab),
                  FadeIn(row, lag_ratio=0.2), Write(row_lab))
        self.wait(0.4)

        # Target 3x4 result grid (right) — values hidden until the sum.
        result = VGroup(*[num_cell(col_vals[i] + row_vals[j], SUM_C, fill=0.0)
                          for i in range(3) for j in range(4)])
        result.arrange_in_grid(3, 4, buff=0.12)
        result.move_to(RIGHT * 3.2 + DOWN * 0.4)
        cell = lambda i, j: result[i * 4 + j]
        for c in result:
            c[1].set_opacity(0)
        frames = VGroup(*[c[0] for c in result])
        self.play(ShowCreation(frames, lag_ratio=0.02))

        # Stretch the column across all 4 columns (blue echoes).
        lab1 = Tex(R"(3,1) \rightarrow (3,4)", font_size=30, color=COL_C)
        lab1.next_to(result, UP, buff=0.25).shift(LEFT * 1.4)
        self.play(FadeIn(lab1))
        col_pairs = []
        for j in range(4):
            for i in range(3):
                g = num_cell(col_vals[i], COL_C, fill=0.30).scale(0.55)
                g.move_to(cell(i, j)).shift(LEFT * 0.18 + UP * 0.18)
                col_pairs.append((col[i], g))
        col_ghosts = VGroup(*[g for _, g in col_pairs])
        self.play(LaggedStart(*[TransformFromCopy(s, g) for s, g in col_pairs],
                              lag_ratio=0.04, run_time=2.2))
        self.wait(0.3)

        # Stretch the row down all 3 rows (green echoes).
        lab2 = Tex(R"(1,4) \rightarrow (3,4)", font_size=30, color=ROW_C)
        lab2.next_to(result, UP, buff=0.25).shift(RIGHT * 1.4)
        self.play(FadeIn(lab2))
        row_pairs = []
        for i in range(3):
            for j in range(4):
                g = num_cell(row_vals[j], ROW_C, fill=0.30).scale(0.55)
                g.move_to(cell(i, j)).shift(RIGHT * 0.18 + DOWN * 0.18)
                row_pairs.append((row[j], g))
        row_ghosts = VGroup(*[g for _, g in row_pairs])
        self.play(LaggedStart(*[TransformFromCopy(s, g) for s, g in row_pairs],
                              lag_ratio=0.04, run_time=2.2))
        self.wait(0.3)

        # Element-wise add -> reveal sums.
        caption = Text("element-wise add", font_size=30).to_edge(DOWN)
        self.play(FadeIn(caption))
        reveals = [cell(i, j)[1].animate.set_opacity(1).set_color(WHITE)
                   for i in range(3) for j in range(4)]
        self.play(FadeOut(col_ghosts), FadeOut(row_ghosts), *reveals, run_time=1.5)
        self.play(LaggedStart(*[Indicate(cell(i, j), color=SUM_C)
                                for i in range(3) for j in range(4)], lag_ratio=0.05))
        self.wait(1.2)
