"""Function calling round trip: the model asks, OUR code executes.
Five steps down the right column, alternating between the model and our runtime.
Attaches to notebook: '## 7. 함수 호출(Function Calling) 기초'.
"""
from manimlib import *

MONO = "Consolas"


def card(lines, color, font_size=17):
    body = Text("\n".join(lines), font=MONO, font_size=font_size, color=color)
    box = RoundedRectangle(width=body.get_width() + 0.5,
                           height=body.get_height() + 0.36,
                           corner_radius=0.11)
    box.set_fill(BLACK, 1).set_stroke(color, 2)
    body.move_to(box)
    return VGroup(box, body)


def step_dot(n, color):
    circ = Circle(radius=0.19).set_fill(color, 1).set_stroke(color, 2)
    num = Text(str(n), font=MONO, font_size=19, color=BLACK).move_to(circ)
    return VGroup(circ, num)


def side_box(text, color):
    box = RoundedRectangle(width=2.7, height=1.15, corner_radius=0.14)
    box.set_fill(GREY_E, 1).set_stroke(color, 2)
    label = Text(text, font=MONO, font_size=21, color=color).move_to(box)
    return VGroup(box, label)


class FunctionCalling(Scene):
    def construct(self):
        title = Text("Function calling: the model asks, your code runs",
                     font_size=32).to_edge(UP, buff=0.3)
        self.play(Write(title))

        model = side_box("LLM", YELLOW_B)
        runtime = side_box("your code", BLUE_B)
        model.move_to(4.9 * LEFT + 1.55 * UP)
        runtime.move_to(4.9 * LEFT + 1.75 * DOWN)
        self.play(FadeIn(model), FadeIn(runtime))

        # five steps, alternating owner: user code -> model -> code -> code -> model
        steps = [
            (runtime, ['user: "what is the weather in Seoul?"'], BLUE_B),
            (model,   ['tool_calls  ->  name: get_weather',
                       '                arguments: {"city": "Seoul"}',
                       '                id: call_abc123'], YELLOW_B),
            (runtime, ['get_weather(city="Seoul")  ->  "sunny, 27C"'], BLUE_B),
            (runtime, ['role: "tool"   tool_call_id: call_abc123',
                       'content: "sunny, 27C"'], GREEN_B),
            (model,   ['"It is sunny and 27C in Seoul."'], GREEN_B),
        ]

        cards = VGroup(*[card(lines, color) for _, lines, color in steps])
        cards.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        cards.set_width(min(8.4, cards.get_width()))
        cards.move_to(2.0 * RIGHT + 0.35 * DOWN)

        dots = VGroup(*[step_dot(i + 1, steps[i][2]).next_to(cards[i], LEFT, buff=0.2)
                        for i in range(len(steps))])

        notes = {
            1: ("content is None: a request, not an answer", RED_B),
            2: ("we run the real python function", BLUE_B),
            3: ("same id links result to request", GREEN_B),
        }

        for i, (src, _, color) in enumerate(steps):
            arrow = Arrow(src.get_right(), cards[i].get_left(), buff=0.22,
                          stroke_width=3.5, tip_width_ratio=4).set_color(color)
            self.play(ShowCreation(arrow), run_time=0.4)
            self.play(FadeIn(cards[i], shift=0.15 * RIGHT), FadeIn(dots[i]),
                      Indicate(src, color=color, scale_factor=1.05), run_time=0.7)
            if i in notes:
                txt, c = notes[i]
                note = Text(txt, font_size=19, color=c).next_to(cards[i], DOWN, buff=0.1)
                note.align_to(cards[i], LEFT)
                self.play(FadeIn(note), run_time=0.4)
                self.wait(0.4)
                self.play(FadeOut(note), run_time=0.3)
            self.play(FadeOut(arrow), run_time=0.3)

        self.play(Indicate(cards[4], color=GREEN, scale_factor=1.04))

        punch = Text("the model never executes anything itself",
                     font_size=25, color=RED_B).to_edge(DOWN, buff=0.28)
        self.play(FadeIn(punch, shift=0.15 * UP))
        self.wait(1.5)
