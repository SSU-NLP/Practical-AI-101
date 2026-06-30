# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A pipeline that produces **ManimGL** animations for a Korean week-1 PyTorch deep-learning
course notebook and embeds them as gifs into that notebook. There is no app to build/test —
the "product" is the rendered visuals and the embedded notebook.

## Setup (required before any render)

```bash
source .venv/bin/activate          # manimgl/ffmpeg need the venv on PATH
# first-time only: python3 -m venv .venv && pip install manimgl
```
Toolchain: `manimgl` v1.7.2 (3b1b, NOT Community Edition), system `ffmpeg`, and LaTeX (MacTeX).
`.venv/` and `manim/videos/` are gitignored.

## Common commands

```bash
cd manim
./render.sh                 # render every scene -> videos/<Scene>.mp4 + .gif
./render.sh Backprop        # render only scenes whose name contains the filter
Q=-l ./render.sh            # quality: -l fast / -m default(720p) / -hq 1080p
python embed_into_notebook.py   # copy gifs to week1/assets/ + insert cells into the notebook
```

Verify a scene visually (rendering OK ≠ looks right): render it, then eyeball a frame —
`ffmpeg -y -sseof -0.4 -i videos/<Scene>.mp4 -update 1 frame.png` and Read the png.

## Architecture / data flow

1. **`manim/scenes/*.py`** — one `Scene` subclass per file (`MatMul`, `Backprop`, …). Pure ManimGL.
2. **`manim/render.sh`** — the headless harness. `manimgl` v1.7.2 has no `--format gif` and opens a
   GUI window if run bare, so render.sh renders mp4 with `-w` then palette-converts to gif via ffmpeg.
   Outputs land in `manim/videos/`. The `SCENES` array is the source of truth for what gets rendered.
3. **`manim/embed_into_notebook.py`** — copies gifs into `week1/assets/` and inserts a markdown cell
   (gif + Korean caption) into the notebook. Its `INSERTS` dict maps **original cell index ->
   (title, gif_basename, caption)**; cells are inserted highest-index-first so earlier indices stay valid.

### Notebook source-of-truth (important)

- `week1/딥러닝기초_PyTorch_전체.원본.ipynb` — **pristine source**, no visuals. Never embed into this.
- `week1/딥러닝기초_PyTorch_전체.ipynb` — **the deliverable**, with visuals embedded.

`embed_into_notebook.py` always reads `.원본` (SRC) and writes the main file (DST), so re-running it
is safe and never double-inserts. gif paths in the notebook are relative (`assets/X.gif`), resolving
when opened from `week1/`. (This is a Colab notebook — relative gifs won't render on Colab without
also uploading `assets/`, or switching to base64-embedded gifs.)

## Adding / editing a scene

1. Write `manim/scenes/<name>.py` with a `Scene` subclass.
2. Add `"scenes/<name>.py:<SceneClass>"` to `SCENES` in `render.sh`.
3. Add an `INSERTS` entry (original cell index -> title/gif/caption) in `embed_into_notebook.py`.
4. Render, eyeball a frame, then re-run the embed.

## ManimGL gotchas (this is ManimGL, not Community Edition)

- Idioms: `from manimlib import *`, `ShowCreation` (not `Create`), `Tex(R"...")` (not `MathTex`),
  `self.frame` (not `self.camera.frame`). The `.claude/skills/manimgl-best-practices/` skill auto-loads
  and documents these; `manim/README.md` has fuller skill/harness notes.
- `Text(...)` does **not** accept `line_spacing`; use `\n` for multi-line.
- `Tex` with multiple substring args can throw a LaTeX error on lone `(`/`)`; prefer a single string
  with `t2c={...}` for per-token coloring.
- Capture a reference position used to rebuild an animated mobject (e.g. a bar's base point) **after**
  positioning it, not before — otherwise transformed copies snap back to the origin.
- **No Korean text inside the videos** (project requirement) — scene labels are English/LaTeX only.
  Korean appears only in the notebook captions written by the embed script.
