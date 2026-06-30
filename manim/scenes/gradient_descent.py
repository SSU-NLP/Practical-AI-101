"""Gradient descent on L(x) = 3x^2  (gradient = 6x).
Ball on the loss curve; tangent shows the slope; step downhill; loss shrinks.
Attaches to notebook: 'Part 2: 자동 미분' (y=3x^2, grad=6x) and the 학습 루프.
"""
from manimlib import *


class GradientDescent(Scene):
    def construct(self):
        f = lambda x: 3 * x ** 2
        grad = lambda x: 6 * x

        title = Text("Gradient Descent", font_size=40).to_edge(UP)
        rule = Tex(R"x \;\leftarrow\; x - \eta\,\frac{dL}{dx}", font_size=44)
        rule.next_to(title, DOWN, buff=0.15)
        self.play(Write(title), FadeIn(rule))

        axes = Axes(x_range=(-2.5, 2.5, 1), y_range=(0, 16, 4), width=8.5, height=5.0)
        axes.add_coordinate_labels(font_size=16)
        axes.to_edge(DOWN, buff=0.5)
        graph = axes.get_graph(f, color=BLUE)
        glabel = Tex(R"L(x) = 3x^2", font_size=40, color=BLUE)
        glabel.next_to(axes.get_top(), DOWN, buff=0.1).shift(LEFT * 3.5)
        self.play(ShowCreation(axes), FadeIn(glabel))
        self.play(ShowCreation(graph))

        # minimum marker
        min_dot = Dot(axes.c2p(0, 0), color=GREEN)
        min_lab = Text("minimum", font_size=24, color=GREEN).next_to(min_dot, UR, buff=0.1)
        self.play(FadeIn(min_dot, scale=2), FadeIn(min_lab))

        x = 2.0
        lr = 0.1
        dot = Dot(axes.i2gp(x, graph), color=YELLOW, radius=0.1).set_z_index(2)
        self.play(FadeIn(dot, scale=2))

        def tangent(xv):
            m, d = grad(xv), 0.6
            p1 = axes.c2p(xv - d, f(xv) - m * d)
            p2 = axes.c2p(xv + d, f(xv) + m * d)
            return Line(p1, p2).set_stroke(RED, 4)

        def panel(i, xv):
            t = VGroup(
                Text(f"step {i}", font_size=28),
                Tex(fR"x = {xv:.2f}", font_size=30),
                Tex(fR"\nabla = 6x = {grad(xv):.2f}", font_size=30, color=RED),
                Tex(fR"L = {f(xv):.2f}", font_size=30, color=BLUE),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
            t.to_corner(UR).shift(DOWN * 0.3)
            return t

        info = panel(0, x)
        tan = tangent(x)
        self.play(FadeIn(info), ShowCreation(tan))
        self.wait(0.5)

        path_pts = [axes.i2gp(x, graph)]
        for i in range(1, 8):
            x_new = x - lr * grad(x)
            new_tan = tangent(x_new)
            new_info = panel(i, x_new)
            new_dot_pos = axes.i2gp(x_new, graph)
            path_pts.append(new_dot_pos)
            self.play(
                dot.animate.move_to(new_dot_pos),
                Transform(tan, new_tan),
                Transform(info, new_info),
                run_time=0.7,
            )
            x = x_new
            if abs(grad(x)) < 0.2:
                break

        trail = VMobject().set_points_smoothly(path_pts).set_stroke(YELLOW, 3)
        self.play(FadeOut(tan), ShowCreation(trail))
        conv = Text("converged to the minimum", font_size=30, color=GREEN)
        conv.next_to(min_dot, UP, buff=0.6)
        self.play(FadeIn(conv, scale=1.2), Indicate(dot, color=GREEN, scale_factor=1.6))
        self.wait(1.4)
