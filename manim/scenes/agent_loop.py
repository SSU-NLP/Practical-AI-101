"""The agent loop: keep calling the model until it stops requesting tools.
Two iterations (get_weather, then calculate) and then the exit branch.
Attaches to notebook: '## 9. 에이전트(Agent) 루프 만들기'.
"""
from manimlib import *

MONO = "Consolas"


def node(text, color, w=3.0, h=1.0, font_size=21):
    box = RoundedRectangle(width=w, height=h, corner_radius=0.13)
    box.set_fill(GREY_E, 1).set_stroke(color, 2)
    label = Text(text, font=MONO, font_size=font_size, color=color).move_to(box)
    return VGroup(box, label)


class AgentLoop(Scene):
    def construct(self):
        title = Text("Agent loop: repeat until no tool is requested",
                     font_size=34).to_edge(UP, buff=0.35)
        self.play(Write(title))

        ask = node("call the model", YELLOW_B, w=3.4)
        check = node("tool_calls ?", WHITE, w=3.0, h=0.9)
        run = node("run the function", BLUE_B, w=3.4)
        done = node("final answer", GREEN_B, w=3.0)

        ask.move_to(3.0 * LEFT + 1.75 * UP)
        check.move_to(3.0 * LEFT + 0.35 * UP)
        run.move_to(3.0 * LEFT + 1.35 * DOWN)
        done.move_to(0.65 * RIGHT + 0.35 * UP)

        a1 = Arrow(ask.get_bottom(), check.get_top(), buff=0.08, stroke_width=4, tip_width_ratio=4)
        a2 = Arrow(check.get_bottom(), run.get_top(), buff=0.08, stroke_width=4, tip_width_ratio=4)
        a2.set_color(BLUE_B)
        a3 = Arrow(check.get_right(), done.get_left(), buff=0.08, stroke_width=4, tip_width_ratio=4)
        a3.set_color(GREEN_B)

        yes = Text("yes", font=MONO, font_size=19, color=BLUE_B).next_to(a2, LEFT, buff=0.12)
        no = Text("no", font=MONO, font_size=19, color=GREEN_B).next_to(a3, UP, buff=0.1)

        # feedback edge: run -> back up to the model
        back = VMobject().set_points_as_corners([
            run.get_left(),
            run.get_left() + 1.2 * LEFT,
            ask.get_left() + 1.2 * LEFT,
            ask.get_left(),
        ]).set_stroke(BLUE_B, 3)
        back_lab = Text('append\nrole:"tool"', font=MONO, font_size=17, color=BLUE_B)
        back_lab.move_to(np.array([run.get_left()[0] - 1.2, ask.get_top()[1] + 0.45, 0]))

        self.play(FadeIn(ask), FadeIn(check), FadeIn(run), FadeIn(done))
        self.play(ShowCreation(a1), ShowCreation(a2), ShowCreation(a3),
                  FadeIn(yes), FadeIn(no))
        self.play(ShowCreation(back), FadeIn(back_lab))
        self.wait(0.3)

        # --- the running log on the right ---
        q = Text('"weather in Seoul, and 25 x 4 ?"', font=MONO, font_size=19, color=GREY_A)
        q.to_edge(RIGHT, buff=0.45).shift(2.5 * UP)
        self.play(FadeIn(q))

        log = VGroup()
        turns = [
            ('turn 1  get_weather("Seoul")', '-> "sunny, 27C"', BLUE_B),
            ('turn 2  calculate("25*4")', '-> "100"', BLUE_B),
            ('turn 3  no tool_calls', '-> final answer', GREEN_B),
        ]

        def highlight(mobs, color):
            return AnimationGroup(*[Indicate(m, color=color, scale_factor=1.06) for m in mobs])

        for i, (head, tail, color) in enumerate(turns):
            line = VGroup(
                Text(head, font=MONO, font_size=18, color=color),
                Text(tail, font=MONO, font_size=18, color=GREY_A),
            ).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
            if len(log) == 0:
                line.next_to(q, DOWN, buff=0.45).align_to(q, LEFT)
            else:
                line.next_to(log, DOWN, buff=0.32).align_to(log, LEFT)

            self.play(highlight([ask], YELLOW), run_time=0.5)
            self.play(highlight([check], WHITE), run_time=0.4)
            if color is BLUE_B:
                self.play(ShowPassingFlash(a2.copy().set_stroke(BLUE, 6)), run_time=0.5)
                self.play(highlight([run], BLUE), FadeIn(line, shift=0.15 * RIGHT))
                self.play(ShowPassingFlash(back.copy().set_stroke(BLUE, 6)), run_time=0.9)
            else:
                self.play(ShowPassingFlash(a3.copy().set_stroke(GREEN, 6)), run_time=0.5)
                self.play(highlight([done], GREEN), FadeIn(line, shift=0.15 * RIGHT))
            log.add(line)

        guard = Text("max_turns caps the loop", font=MONO, font_size=20, color=RED_B)
        guard.next_to(log, DOWN, buff=0.5).align_to(log, LEFT)
        self.play(FadeIn(guard))
        self.wait(1.5)
