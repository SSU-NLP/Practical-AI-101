"""Why the whole `messages` list is resent every turn.
Turn by turn the list grows (user -> assistant -> user ...) and the entire stack
is shipped again, so prompt tokens grow with the conversation.
Attaches to notebook: '## 6. 대화 이어가기'.
"""
from manimlib import *

MONO = "Consolas"

ROLE_COLOR = {"user": BLUE_B, "assistant": GREEN_B}


def bubble(role, text, width=4.6):
    label = Text(f'{role}: "{text}"', font=MONO, font_size=17, color=ROLE_COLOR[role])
    box = RoundedRectangle(width=width, height=label.get_height() + 0.3, corner_radius=0.1)
    box.set_fill(BLACK, 1).set_stroke(ROLE_COLOR[role], 2)
    label.move_to(box)
    return VGroup(box, label)


class MessagesContext(Scene):
    def construct(self):
        title = Text("The model only sees what you resend", font_size=38).to_edge(UP, buff=0.35)
        self.play(Write(title))

        # server on the right, the growing messages list on the left
        server = RoundedRectangle(width=2.6, height=1.5, corner_radius=0.14)
        server.set_fill(GREY_E, 1).set_stroke(YELLOW_D, 2)
        server_txt = Text("LLM\n(stateless)", font=MONO, font_size=20, color=YELLOW_B).move_to(server)
        server_grp = VGroup(server, server_txt).to_edge(RIGHT, buff=0.9).shift(0.3 * DOWN)
        self.play(FadeIn(server_grp))

        list_title = Text("messages", font=MONO, font_size=24, color=GREY_A)
        list_title.to_edge(LEFT, buff=1.0).shift(1.9 * UP)
        self.play(FadeIn(list_title))

        turns = [
            ("user", "I like the number 7"),
            ("assistant", "Noted!"),
            ("user", "multiply it by 3"),
        ]
        tokens = [12, 12, 31]

        stack = VGroup()
        tok_label = None

        for i, (role, text) in enumerate(turns):
            b = bubble(role, text)
            if len(stack) == 0:
                b.next_to(list_title, DOWN, buff=0.3).align_to(list_title, LEFT)
            else:
                b.next_to(stack, DOWN, buff=0.18).align_to(stack, LEFT)
            self.play(FadeIn(b, shift=0.2 * RIGHT), run_time=0.5)
            stack.add(b)

            if role != "user":
                continue

            # the WHOLE stack is sent, not just the new message
            flying = stack.copy().set_opacity(0.9)
            arrow = Arrow(stack.get_right(), server.get_left(), buff=0.3,
                          stroke_width=4, tip_width_ratio=4).set_color(BLUE_B)
            self.play(ShowCreation(arrow), run_time=0.4)
            self.play(flying.animate.scale(0.35).move_to(server.get_center()), run_time=1.0)
            self.play(FadeOut(flying, scale=0.6), Indicate(server, color=YELLOW), run_time=0.5)

            new_tok = Text(f"prompt tokens: {tokens[i]}", font=MONO, font_size=22, color=GREY_A)
            new_tok.next_to(server_grp, DOWN, buff=0.45)
            if tok_label is None:
                self.play(FadeIn(new_tok), run_time=0.4)
            else:
                self.play(FadeTransform(tok_label, new_tok), run_time=0.5)
            tok_label = new_tok
            self.play(FadeOut(arrow), run_time=0.3)

        # the payoff: drop the history and the answer falls apart
        note = Text("drop the history -> the model cannot answer",
                    font_size=26, color=RED_B)
        note.to_edge(DOWN, buff=0.75)
        self.play(FadeIn(note, shift=0.15 * UP))
        self.play(LaggedStart(*[b.animate.set_opacity(0.18) for b in stack[:2]], lag_ratio=0.15))
        self.wait(0.6)
        self.play(LaggedStart(*[b.animate.set_opacity(1.0) for b in stack[:2]], lag_ratio=0.15))

        cost = Text("longer conversation = more prompt tokens = higher cost",
                    font=MONO, font_size=21, color=GREY_A)
        cost.next_to(note, DOWN, buff=0.22)
        self.play(FadeIn(cost))
        self.wait(1.4)
