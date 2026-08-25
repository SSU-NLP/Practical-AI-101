"""Full document -> overlapping chunks. Shows size cap and overlap duplication.
Attaches to week3 notebook: '## 5. 문서 쪼개기: 청킹(Chunking)'.
"""
from manimlib import *

CHUNK_W, OVERLAP_W, ROW_Y = 4.2, 0.7, -0.6
CCOLORS = [(BLUE_B, BLUE_E), (GOLD_B, GOLD_E), (GREEN_B, GREEN_E)]


def block(width, label, stroke, fill, font_size=28):
    box = RoundedRectangle(width=width, height=0.9, corner_radius=0.12)
    box.set_stroke(stroke, 2).set_fill(fill, 0.75)
    return VGroup(box, Text(label, font_size=font_size).move_to(box))


class Chunking(Scene):
    def construct(self):
        title = Text("Chunking", font_size=44).to_edge(UP)
        self.play(Write(title))

        # a long document as one wide bar
        doc = block(11.2, "Full Document  (7,000+ chars)", GREY_B, GREY_D).move_to(UP * 1.6)
        self.play(FadeIn(doc, shift=0.2 * DOWN))
        self.wait(0.4)

        # split into 3 chunks whose edges overlap
        centers = [-3.5, 0.0, 3.5]
        chunks = VGroup(*(
            block(CHUNK_W, f"Chunk {i + 1}", s, f).move_to(RIGHT * x + UP * ROW_Y)
            for i, ((s, f), x) in enumerate(zip(CCOLORS, centers))
        ))
        self.play(*(TransformFromCopy(doc[0], c[0]) for c in chunks))
        self.play(*(FadeIn(c[1]) for c in chunks))   # added after the boxes -> text stays on top
        self.wait(0.6)

        # overlap zones where neighbouring chunks share text
        zones, zlabels = VGroup(), VGroup()
        for x in (-1.75, 1.75):
            z = Rectangle(width=OVERLAP_W, height=0.9).move_to(RIGHT * x + UP * ROW_Y)
            z.set_stroke(RED, 3).set_fill(RED, 0.35)
            zones.add(z)
            zlabels.add(Text("overlap", font_size=24, color=RED).next_to(z, DOWN, buff=0.15))
        self.play(ShowCreation(zones), FadeIn(zlabels))
        self.wait(0.8)

        # pull the chunks apart: the overlap text is kept by BOTH neighbours
        copies = VGroup(zones[0].copy(), zones[1].copy())
        self.add(copies)               # one copy stays on each inner edge of chunk 2
        SPREAD = 1.2
        self.play(
            chunks[0].animate.shift(LEFT * SPREAD), chunks[2].animate.shift(RIGHT * SPREAD),
            zones[0].animate.shift(LEFT * SPREAD),    # right edge of chunk 1
            copies[1].animate.shift(RIGHT * SPREAD),  # left edge of chunk 3
            zlabels[0].animate.shift(LEFT * SPREAD), zlabels[1].animate.shift(RIGHT * SPREAD),
        )
        self.wait(2)
