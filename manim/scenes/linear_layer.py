"""Linear layer = neuron computation = Wx + b.
nn.Linear(4, 2): bridges the 'graph of neurons' view and the matrix form.
Attaches to notebook: '### 선형 레이어 (Linear Layer)' (cells ~71-73).
"""
from manimlib import *

IN_C = BLUE_D
OUT_C = TEAL_D


def node(label, color):
    c = Circle(radius=0.34).set_stroke(WHITE, 2).set_fill(color, 0.35)
    t = Tex(label, font_size=30).move_to(c)
    return VGroup(c, t)


class LinearLayerNeuron(Scene):
    def construct(self):
        title = Text("Linear layer:  nn.Linear(4, 2)", font_size=42).to_edge(UP)
        self.play(Write(title))

        inputs = VGroup(*[node(f"x_{i+1}", IN_C) for i in range(4)])
        inputs.arrange(DOWN, buff=0.55).shift(LEFT * 4 + DOWN * 0.3)
        outputs = VGroup(node("y_1", OUT_C), node("y_2", OUT_C))
        outputs.arrange(DOWN, buff=1.6).shift(RIGHT * 3.2 + DOWN * 0.3)

        edges = VGroup()
        edge_of = {}
        for oi, o in enumerate(outputs):
            for ii, inp in enumerate(inputs):
                e = Line(inp[0].get_right(), o[0].get_left(), buff=0.04).set_stroke(GREY, 1.5)
                edges.add(e)
                edge_of[(oi, ii)] = e

        self.play(ShowCreation(edges, lag_ratio=0.02),
                  FadeIn(inputs, lag_ratio=0.1), FadeIn(outputs, lag_ratio=0.1))
        self.wait(0.3)

        # Focus neuron y1: weighted sum + bias.
        focus = VGroup(*[edge_of[(0, ii)] for ii in range(4)])
        dim = VGroup(*[e for (oi, ii), e in edge_of.items() if oi != 0])
        self.play(focus.animate.set_stroke(YELLOW, 3), dim.animate.set_stroke(GREY, 0.6))
        formula = Tex(R"y_1 = w_{11}x_1 + w_{12}x_2 + w_{13}x_3 + w_{14}x_4 + b_1",
                      font_size=34).to_edge(DOWN)
        self.play(Write(formula))

        # Inputs flow along the edges into the neuron.
        dots = VGroup(*[Dot(color=YELLOW, radius=0.09).move_to(inputs[k][0]) for k in range(4)])
        self.play(LaggedStart(*[dot.animate.move_to(outputs[0][0]) for dot in dots],
                              lag_ratio=0.12, run_time=1.6))
        self.play(FadeOut(dots), Indicate(outputs[0], color=YELLOW, scale_factor=1.3))
        self.wait(0.4)

        # Reveal: both neurons at once = matrix form y = W x + b.
        self.play(focus.animate.set_stroke(GREY, 1.5), dim.animate.set_stroke(GREY, 1.5),
                  FadeOut(formula))
        bridge = Text("Both outputs at once  =  one matrix multiply", font_size=30, color=YELLOW)
        bridge.to_edge(DOWN)
        self.play(FadeIn(bridge))

        W = Matrix([["w_{11}", "w_{12}", "w_{13}", "w_{14}"],
                    ["w_{21}", "w_{22}", "w_{23}", "w_{24}"]])
        xv = Matrix([["x_1"], ["x_2"], ["x_3"], ["x_4"]])
        bv = Matrix([["b_1"], ["b_2"]])
        yv = Matrix([["y_1"], ["y_2"]])
        W.get_entries().set_color(YELLOW)
        xv.get_entries().set_color(IN_C)
        yv.get_entries().set_color(OUT_C)
        eq = Tex("="); plus = Tex("+")
        expr = VGroup(yv, eq, W, xv, plus, bv).arrange(RIGHT, buff=0.25)
        expr.set_height(1.9).center().shift(UP * 0.2)
        box = SurroundingRectangle(expr, buff=0.3).set_stroke(YELLOW, 2)

        self.play(LaggedStart(FadeOut(edges), FadeOut(inputs), FadeOut(outputs), lag_ratio=0.1))
        self.play(Write(expr))
        shapes = Tex(R"(2,1) = (2,4)\,(4,1) + (2,1)", font_size=34)
        shapes.next_to(expr, UP, buff=0.4)
        self.play(ShowCreation(box), FadeIn(shapes, shift=0.2 * UP))
        self.wait(1.4)
