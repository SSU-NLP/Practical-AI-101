"""LLM API round trip: our code sends `messages`, the server returns one completion.
Shows that the request carries the whole conversation and the server keeps nothing.
Attaches to notebook: '## 3. 첫 번째 응답 받기'.
"""
from manimlib import *

MONO = "Consolas"


def panel(inner, pad=0.32, stroke=GREY_B, fill=GREY_E, radius=0.14):
    box = RoundedRectangle(
        width=inner.get_width() + 2 * pad,
        height=inner.get_height() + 2 * pad,
        corner_radius=radius,
    )
    box.set_fill(fill, 1).set_stroke(stroke, 2)
    inner.move_to(box)
    return VGroup(box, inner)


def code(lines, font_size=20, color=WHITE):
    return Text("\n".join(lines), font=MONO, font_size=font_size, color=color)


class ApiRoundTrip(Scene):
    def construct(self):
        title = Text("Calling an LLM through an API", font_size=40).to_edge(UP, buff=0.4)
        self.play(Write(title))

        # --- two sides: our machine and the model server ---
        client = panel(code([
            "client.chat.completions",
            "      .create(",
            "    model=MODEL,",
            "    messages=messages,",
            "  )",
        ], font_size=19))
        client_lab = Text("your notebook", font_size=24, color=BLUE_B)
        client_grp = VGroup(client, client_lab).arrange(DOWN, buff=0.22)

        server = panel(code([
            "LLM",
            "(weights + GPU)",
        ], font_size=22, color=YELLOW_B), pad=0.5, stroke=YELLOW_D)
        server_lab = Text("provider server", font_size=24, color=YELLOW_B)
        server_grp = VGroup(server, server_lab).arrange(DOWN, buff=0.22)

        row = VGroup(client_grp, server_grp).arrange(RIGHT, buff=3.6)
        row.set_width(11.5).move_to(0.35 * DOWN)
        self.play(FadeIn(client_grp, shift=0.2 * RIGHT), FadeIn(server_grp, shift=0.2 * LEFT))
        self.wait(0.3)

        up_arrow = Arrow(client.get_right(), server.get_left(), buff=0.25,
                         stroke_width=4, tip_width_ratio=4).shift(0.45 * UP)
        down_arrow = Arrow(server.get_left(), client.get_right(), buff=0.25,
                           stroke_width=4, tip_width_ratio=4).shift(0.55 * DOWN)
        up_arrow.set_color(BLUE_B)
        down_arrow.set_color(GREEN_B)
        self.play(ShowCreation(up_arrow), ShowCreation(down_arrow))

        # --- request packet travels to the server ---
        req = panel(code([
            '[{"role": "user",',
            '  "content": "..."}]',
        ], font_size=17, color=BLUE_B), pad=0.2, stroke=BLUE_D, fill=BLACK)
        req.scale(0.9).move_to(client.get_center())
        req_tag = Text("request: messages", font_size=20, color=BLUE_B)
        req_tag.next_to(up_arrow, UP, buff=0.12)

        self.play(FadeIn(req, scale=0.8), FadeIn(req_tag))
        self.play(req.animate.move_to(server.get_center()), run_time=1.2)
        self.play(FadeOut(req, scale=0.7), Indicate(server, color=YELLOW, scale_factor=1.05))

        # --- response packet travels back ---
        res = panel(code([
            'choices[0]',
            '  .message.content',
        ], font_size=17, color=GREEN_B), pad=0.2, stroke=GREEN_D, fill=BLACK)
        res.scale(0.9).move_to(server.get_center())
        res_tag = Text("response: one completion", font_size=20, color=GREEN_B)
        res_tag.next_to(down_arrow, DOWN, buff=0.12)

        self.play(FadeIn(res, scale=0.8), FadeIn(res_tag))
        self.play(res.animate.move_to(client.get_center()), run_time=1.2)
        self.play(Indicate(client, color=GREEN, scale_factor=1.03))
        self.wait(0.3)

        # --- the key property: the server remembers nothing ---
        note = Text("the server keeps no memory of this call",
                    font_size=27, color=RED_B)
        note.next_to(row, DOWN, buff=0.5)
        underline = Line(note.get_left(), note.get_right()).set_stroke(RED_B, 2)
        underline.next_to(note, DOWN, buff=0.1)
        self.play(FadeIn(note, shift=0.15 * UP), ShowCreation(underline))

        self.play(FadeOut(res, scale=0.7))
        cost = Text("billed per token: prompt + completion", font_size=24, color=GREY_A)
        cost.next_to(underline, DOWN, buff=0.3)
        self.play(FadeIn(cost))
        self.wait(1.5)
