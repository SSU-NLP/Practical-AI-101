"""Backpropagation through a neural network.
Forward pass (blue) flows input -> hidden -> output -> loss; then backward()
flows gradients (red) loss -> output -> hidden -> input, layer by layer.
Attaches to notebook: '## Part 2: 자동 미분 (Autograd)'.
"""
from manimlib import *

IN_C = BLUE_D
HID_C = TEAL_D
OUT_C = PURPLE_B
FWD = BLUE_B
BWD = RED


def node(label, color, r=0.32):
    c = Circle(radius=r).set_stroke(WHITE, 2).set_fill(color, 0.4)
    t = Tex(label, font_size=24).move_to(c)
    return VGroup(c, t)


class Backprop(Scene):
    def construct(self):
        title = Text("Backpropagation", font_size=42).to_edge(UP)
        self.play(Write(title))

        inputs = VGroup(node("x_1", IN_C), node("x_2", IN_C)).arrange(DOWN, buff=1.3)
        inputs.move_to(LEFT * 5)
        hidden = VGroup(node("h_1", HID_C), node("h_2", HID_C), node("h_3", HID_C))
        hidden.arrange(DOWN, buff=0.8).move_to(LEFT * 1.6)
        output = node(R"\hat{y}", OUT_C).move_to(RIGHT * 1.8)
        loss = VGroup(
            RoundedRectangle(width=1.3, height=1.0, corner_radius=0.12).set_stroke(YELLOW, 2).set_fill(GREY_E, 1),
            Tex("L", font_size=34),
        )
        loss.move_to(RIGHT * 4.5)

        W1 = VGroup(*[Line(i[0].get_right(), h[0].get_left(), buff=0.04).set_stroke(GREY, 1.8)
                      for i in inputs for h in hidden])
        W2 = VGroup(*[Line(h[0].get_right(), output[0].get_left(), buff=0.04).set_stroke(GREY, 1.8)
                      for h in hidden])
        e_out = Arrow(output.get_right(), loss.get_left(), buff=0.1, stroke_width=3).set_color(GREY)

        self.play(ShowCreation(W1, lag_ratio=0.03), ShowCreation(W2, lag_ratio=0.05),
                  FadeIn(inputs), FadeIn(hidden), FadeIn(output))
        self.play(GrowArrow(e_out), FadeIn(loss))

        def flow(edges, color, reverse=False, rt=1.0):
            dots = VGroup()
            anims = []
            for e in edges:
                s, t = (e.get_end(), e.get_start()) if reverse else (e.get_start(), e.get_end())
                d = Dot(color=color, radius=0.07).move_to(s)
                dots.add(d)
                anims.append(d.animate.move_to(t))
            self.add(dots)
            self.play(LaggedStart(*anims, lag_ratio=0.04, run_time=rt))
            self.play(FadeOut(dots), run_time=0.2)

        # ---- Forward ----
        fwd_lab = Text("forward  ->", font_size=28, color=FWD).to_corner(UL).shift(DOWN * 0.9)
        self.play(FadeIn(fwd_lab))
        flow(W1, FWD)
        self.play(hidden.animate.set_fill(HID_C, 0.7), run_time=0.3)
        self.play(hidden.animate.set_fill(HID_C, 0.4), run_time=0.3)
        flow(W2, FWD)
        flow([e_out], FWD, rt=0.6)
        self.play(Indicate(loss, color=YELLOW))
        self.wait(0.3)

        # ---- Backward ----
        bwd_lab = Text("<-  backward", font_size=28, color=BWD).to_corner(UL).shift(DOWN * 1.5)
        self.play(FadeIn(bwd_lab))

        g_out = Tex(R"\frac{\partial L}{\partial \hat{y}}", font_size=30, color=BWD).next_to(output, UP, buff=0.3)
        flow([e_out], BWD, reverse=True, rt=0.6)
        self.play(FadeIn(g_out))

        # W2 gradients
        gw2 = Tex(R"\nabla W_2", font_size=30, color=BWD).next_to(W2, UP, buff=0.2)
        self.play(W2.animate.set_stroke(BWD, 4), FadeIn(gw2))
        flow(W2, BWD, reverse=True)

        # W1 gradients
        gw1 = Tex(R"\nabla W_1", font_size=30, color=BWD).next_to(W1, UP, buff=0.2)
        self.play(W1.animate.set_stroke(BWD, 4), FadeIn(gw1))
        flow(W1, BWD, reverse=True)

        chain = Tex(R"\frac{\partial L}{\partial W_1} = "
                    R"\frac{\partial L}{\partial \hat{y}}\cdot"
                    R"\frac{\partial \hat{y}}{\partial h}\cdot"
                    R"\frac{\partial h}{\partial W_1}", font_size=40)
        chain.to_edge(DOWN, buff=0.5)
        self.play(Write(chain))
        self.wait(1.5)
