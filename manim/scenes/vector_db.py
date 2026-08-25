"""Vector DB concept: chunks are embedded and stored once (indexing),
then every question is embedded and the k nearest vectors are fetched (search).
Attaches to week3 notebook: '## 6. 벡터 DB' intro.
"""
from manimlib import *

BOX_C = RIGHT * 3.9 + DOWN * 0.4
CCOLORS = [(BLUE_B, BLUE_E), (GOLD_B, GOLD_E), (GREEN_B, GREEN_E)]
GREY_DOTS = [(-1.7, 1.5), (-0.6, 1.7), (0.9, 1.6), (1.7, 1.0), (-1.9, 0.6),
             (0.2, 0.9), (1.3, 0.2), (-1.2, -0.6), (-0.3, -1.0), (0.8, -0.9),
             (1.8, -1.4), (-1.6, -1.5), (-0.5, -1.8), (1.0, -1.9), (1.9, 0.3)]
CHUNK_DOTS = [(-0.9, 0.8), (-0.55, 0.3), (-1.25, 0.2)]   # same-doc chunks cluster


def block(width, label, stroke, fill, font_size=26, height=0.7):
    box = RoundedRectangle(width=width, height=height, corner_radius=0.12)
    box.set_stroke(stroke, 2).set_fill(fill, 0.75)
    return VGroup(box, Text(label, font_size=font_size).move_to(box))


def dot(offset, radius, color):
    d = Dot(BOX_C + RIGHT * offset[0] + UP * offset[1], radius=radius)
    d.set_fill(color, 1).set_stroke(width=0)
    return d


class VectorDB(Scene):
    def construct(self):
        title = Text("Vector DB in RAG", font_size=44).to_edge(UP)
        self.play(Write(title))

        # the DB: a box that will hold one dot per chunk vector
        db = RoundedRectangle(width=4.8, height=4.6, corner_radius=0.2)
        db.set_stroke(GREY_B, 2).set_fill(GREY_E, 0.35).move_to(BOX_C)
        db_label = Text("Vector DB", font_size=30, color=GREY_B).next_to(db, UP, buff=0.15)
        self.play(FadeIn(db), FadeIn(db_label))

        # ── phase 1: indexing (once) ─────────────────────────────
        cap1 = Text("1) Indexing", font_size=32, color=BLUE_B)
        cap1.move_to(LEFT * 4.3 + UP * 2.6)
        chunks = VGroup(*(
            block(2.6, f"Chunk {i + 1}", s, f).move_to(LEFT * 4.6 + UP * (1.5 - 0.9 * i))
            for i, (s, f) in enumerate(CCOLORS)
        ))
        more = VGroup(*(Dot(radius=0.04, fill_color=GREY_B) for _ in range(3)))
        more.arrange(DOWN, buff=0.14).next_to(chunks, DOWN, buff=0.2)
        arrow1 = Arrow(chunks.get_right() + RIGHT * 0.1, db.get_left() + LEFT * 0.1, buff=0)
        embed1 = Text("embed", font_size=26, color=GREY_B).next_to(arrow1, UP, buff=0.1)
        self.play(FadeIn(cap1), LaggedStartMap(FadeIn, chunks, lag_ratio=0.2), FadeIn(more))
        self.play(GrowArrow(arrow1), FadeIn(embed1))

        # each chunk flies in as one vector (dot); grey dots are the other 297
        cdots = VGroup(*(dot(p, 0.1, s) for (s, _), p in zip(CCOLORS, CHUNK_DOTS)))
        gdots = VGroup(*(dot(p, 0.07, GREY_C) for p in GREY_DOTS))
        self.play(*(TransformFromCopy(c[0], d) for c, d in zip(chunks, cdots)))
        self.play(LaggedStartMap(FadeIn, gdots, lag_ratio=0.08, run_time=1.2))
        stored = Text("one vector per chunk", font_size=26, color=GREY_B).next_to(db, DOWN, buff=0.15)
        self.play(FadeIn(stored))
        self.wait(0.8)

        # ── phase 2: search (every question) ─────────────────────
        idx_group = VGroup(cap1, chunks, more, arrow1, embed1)
        self.play(idx_group.animate.set_opacity(0.25), FadeOut(stored))
        cap2 = Text("2) Search - every question", font_size=32, color=YELLOW)
        cap2.move_to(LEFT * 3.9 + DOWN * 1.85)
        q = block(3.2, "Question", YELLOW, GREY_D).move_to(LEFT * 4.6 + DOWN * 2.6)
        arrow2 = Arrow(q.get_right() + RIGHT * 0.1, db.get_corner(DL) + UP * 0.9 + LEFT * 0.1, buff=0)
        embed2 = Text("embed", font_size=26, color=GREY_B).next_to(arrow2, DOWN, buff=0.1)
        self.play(FadeIn(cap2), FadeIn(q))
        self.play(GrowArrow(arrow2), FadeIn(embed2))

        # the question becomes a vector too, landing inside the same space
        qdot = Dot(BOX_C + LEFT * 0.9 + UP * 0.45, radius=0.12)
        qdot.set_fill(YELLOW, 1).set_stroke(width=0)
        self.play(TransformFromCopy(q[0], qdot))
        self.wait(0.4)

        # highlight the k nearest vectors
        rings = VGroup(*(
            Circle(radius=0.22, stroke_color=YELLOW, stroke_width=3).move_to(d)
            for d in cdots
        ))
        near = Text("3 nearest vectors", font_size=26, color=YELLOW).next_to(db, DOWN, buff=0.15)
        self.play(ShowCreation(rings), FadeIn(near))
        self.wait(0.6)

        # ...and their chunks come back out
        out = VGroup(*(
            block(2.1, f"Chunk {i + 1}", s, f, font_size=22, height=0.55)
            for i, (s, f) in enumerate(CCOLORS)
        ))
        out.arrange(RIGHT, buff=0.25).move_to(RIGHT * 3.2 + DOWN * 3.55)
        out_label = Text("their chunks -> into the prompt", font_size=26, color=YELLOW)
        out_label.next_to(out, LEFT, buff=0.35)
        self.play(*(TransformFromCopy(d, o) for d, o in zip(cdots, out)))
        self.play(FadeIn(out_label))
        self.wait(2)
