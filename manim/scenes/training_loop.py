"""Optimizer / training loop: the zero_grad -> forward -> loss -> backward -> step cycle.
Sweeps the loop; at step() the SGD rule w <- w - eta*grad fires and loss shrinks per epoch.
Attaches to notebook: 'Part 4: 최적화' / '### 학습 루프 (Training Loop)'.
"""
from manimlib import *
import numpy as np

ACTIVE = YELLOW
IDLE = GREY_B


def step_node(text):
    label = Text(text, font_size=20)
    box = RoundedRectangle(width=max(label.get_width() + 0.45, 1.9), height=1.0, corner_radius=0.12)
    box.set_stroke(IDLE, 2).set_fill(GREY_E, 1)
    label.move_to(box)
    return VGroup(box, label)


class TrainingLoop(Scene):
    def construct(self):
        title = Text("Training loop  (optimizer)", font_size=40).to_edge(UP)
        self.play(Write(title))

        steps = ["forward\npass", "compute\nloss", "loss\n.backward()",
                 "optimizer\n.step()", "optimizer\n.zero_grad()"]
        center = LEFT * 3.0 + DOWN * 0.3
        radius = 2.3
        nodes = VGroup()
        for i, s in enumerate(steps):
            ang = PI / 2 - i * TAU / 5
            nd = step_node(s).move_to(center + radius * np.array([np.cos(ang), np.sin(ang), 0]))
            nodes.add(nd)

        edges = VGroup()
        for i in range(5):
            a, b = nodes[i], nodes[(i + 1) % 5]
            d = normalize(b.get_center() - a.get_center())
            edges.add(Arrow(a.get_center() + d * 1.05, b.get_center() - d * 1.05,
                            buff=0.05, stroke_width=3).set_color(IDLE))

        self.play(LaggedStartMap(FadeIn, nodes, lag_ratio=0.15),
                  LaggedStartMap(GrowArrow, edges, lag_ratio=0.1))

        # Side panel
        epoch = Text("epoch 1", font_size=30)
        rule = Tex(R"w \;\leftarrow\; w - \eta\,\nabla_w", font_size=34, color=ACTIVE)
        w_lbl = Tex(R"w =", font_size=32)
        w_num = DecimalNumber(2.00, num_decimal_places=2, color=TEAL)
        w_row = VGroup(w_lbl, w_num).arrange(RIGHT, buff=0.15)
        loss_lbl = Tex(R"L =", font_size=32)
        loss_num = DecimalNumber(1.00, num_decimal_places=2, color=BLUE)
        loss_row = VGroup(loss_lbl, loss_num).arrange(RIGHT, buff=0.15)
        bar = Rectangle(width=0.5, height=2.4).set_fill(BLUE, 0.6).set_stroke(WHITE, 1)
        panel = VGroup(epoch, rule, w_row, loss_row).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        panel.move_to(RIGHT * 3.6 + UP * 0.3)
        bar.next_to(panel, DOWN, buff=0.3)
        bar_base = bar.get_bottom()   # capture AFTER positioning, else new bars jump to origin
        bar_lbl = Text("loss", font_size=22).next_to(bar, DOWN, buff=0.1)
        self.play(FadeIn(panel), FadeIn(bar), FadeIn(bar_lbl))

        losses = [1.00, 0.55, 0.30]
        ws = [2.00, 1.40, 1.03]

        def sweep(ep, detailed):
            for i in range(5):
                rt = 0.45 if detailed else 0.18
                self.play(nodes[i][0].animate.set_stroke(ACTIVE, 4).set_fill(ACTIVE, 0.12),
                          run_time=rt)
                if i == 1:  # compute loss
                    self.play(ChangeDecimalToValue(loss_num, losses[ep]), run_time=rt)
                    new_h = 2.4 * losses[ep] / losses[0]
                    new_bar = Rectangle(width=0.5, height=max(new_h, 0.05))
                    new_bar.set_fill(BLUE, 0.6).set_stroke(WHITE, 1)
                    new_bar.move_to(bar_base, DOWN)
                    self.play(Transform(bar, new_bar), run_time=rt)
                if i == 3 and detailed:  # optimizer.step()
                    self.play(Indicate(rule, color=ACTIVE), run_time=0.4)
                if i == 3:
                    self.play(ChangeDecimalToValue(w_num, ws[ep]), run_time=rt)
                self.play(nodes[i][0].animate.set_stroke(IDLE, 2).set_fill(GREY_E, 1),
                          run_time=rt * 0.6)

        sweep(0, detailed=True)
        for ep in (1, 2):
            new_epoch = Text(f"epoch {ep + 1}", font_size=30).move_to(epoch)
            self.play(Transform(epoch, new_epoch), run_time=0.3)
            sweep(ep, detailed=False)

        done = Text("loss decreases each epoch", font_size=28, color=GREEN)
        done.next_to(title, DOWN, buff=0.2)
        self.play(FadeIn(done))
        self.wait(1.4)
