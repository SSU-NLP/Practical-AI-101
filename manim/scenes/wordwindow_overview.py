"""실전 예제 ② Word Window Classification — Overview (flow).
Motivates the sliding window via AMBIGUITY: the SAME token 'jordan' is a LOCATION
in one context and a person in another. Only the surrounding window (context)
distinguishes them — a static word-only rule cannot.
Tokenizer is lower().split(), so both 'jordan's are the identical token.
Sentences are arranged so jordan's window ends the row, leaving clear space on the
right for the classifier + prediction (no overlap with trailing tokens).
Attaches to the Word Window Classification example section.
"""
from manimlib import *

PAD_C = GREY_D
TOK_C = BLUE_D
KEY_C = YELLOW
JX = -2.0  # x where the 'jordan' box is aligned in both rows


def tok_box(label, color, w=1.2, h=0.7, fs=22):
    box = Rectangle(width=w, height=h).set_stroke(WHITE, 1.3).set_fill(color, 0.3)
    t = Text(str(label), font_size=fs).move_to(box)
    return VGroup(box, t)


class WordWindowOverview(Scene):
    def construct(self):
        title = Text("Word window classification", font_size=40).to_edge(UP)
        sub = Text("same word 'jordan' — the window (context) decides", font_size=26, color=YELLOW)
        sub.next_to(title, DOWN, buff=0.15)
        self.play(Write(title), FadeIn(sub))

        def make_row(tokens, ji, y):
            boxes = VGroup(*[tok_box(t, KEY_C if i == ji else TOK_C)
                             for i, t in enumerate(tokens)]).arrange(RIGHT, buff=0.1)
            boxes.scale(0.85).move_to(UP * y)
            boxes.shift(RIGHT * (JX - boxes[ji].get_x()))
            return boxes

        # jordan's window is the LAST 3 tokens -> nothing to its right to collide with
        A = ["we", "travel", "to", "jordan", "today"]   # window = to / jordan / today
        B = ["michael", "jordan", "scored"]             # window = michael / jordan / scored
        ja, jb = 3, 1
        rowA = make_row(A, ja, 1.3)
        rowB = make_row(B, jb, -1.5)

        def classify(row, j, prob, verdict, vcolor, clf_text):
            win = SurroundingRectangle(VGroup(row[j - 1], row[j], row[j + 1]), buff=0.05).set_stroke(KEY_C, 4)
            arr = Arrow(win.get_right(), win.get_right() + RIGHT * 2.3, buff=0.12, stroke_width=3)
            clf = Text(clf_text, font_size=18).next_to(arr, UP, buff=0.05)
            probbox = tok_box(f"p = {prob:.2f}", vcolor, w=1.7, h=0.8, fs=24).next_to(arr, RIGHT, buff=0.15)
            vlab = Text(verdict, font_size=22, color=vcolor).next_to(probbox, UP, buff=0.15)
            return win, VGroup(arr, clf), probbox, vlab

        # Row A: jordan = LOCATION
        self.play(FadeIn(rowA, lag_ratio=0.08))
        winA, clfA, probA, vlabA = classify(rowA, ja, 0.93, "LOCATION", GREEN, "window\nclassifier")
        self.play(ShowCreation(winA))
        self.play(GrowArrow(clfA[0]), FadeIn(clfA[1]))
        self.play(FadeIn(probA), FadeIn(vlabA))
        self.wait(0.3)

        # Row B: jordan = person
        self.play(FadeIn(rowB, lag_ratio=0.08))
        winB, clfB, probB, vlabB = classify(rowB, jb, 0.06, "person (not a place)", RED, "same\nclassifier")
        self.play(ShowCreation(winB))
        self.play(GrowArrow(clfB[0]), FadeIn(clfB[1]))
        self.play(FadeIn(probB), FadeIn(vlabB))
        self.wait(0.3)

        # Link the two identical 'jordan' tokens
        link = DashedLine(rowA[ja].get_bottom(), rowB[jb].get_top(), buff=0.05).set_stroke(KEY_C, 3)
        link_lab = Text("identical token", font_size=20, color=KEY_C).next_to(link, LEFT, buff=0.2)
        self.play(ShowCreation(link), FadeIn(link_lab))
        self.play(Indicate(rowA[ja], color=KEY_C), Indicate(rowB[jb], color=KEY_C))

        arch = Text("classifier:  window -> embed -> flatten -> Linear+Tanh -> Linear -> sigmoid",
                    font_size=20, color=GREY_B)
        punch = Text("the word alone can't decide — the window (context) does",
                     font_size=26).to_edge(DOWN)
        arch.next_to(punch, UP, buff=0.2)
        self.play(FadeIn(arch))
        self.play(Write(punch))
        self.wait(1.5)
