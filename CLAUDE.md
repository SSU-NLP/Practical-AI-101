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
./render.sh                 # render every scene -> mp4+gif, then auto-embed BOTH notebooks
./render.sh Backprop        # render only scenes matching the filter (still re-embeds at the end)
Q=-l ./render.sh            # quality: -l fast / -m default(720p) / -hq 1080p
python embed_into_notebook.py   # (re)generate BOTH notebook versions without rendering
```

Verify a scene visually (rendering OK ≠ looks right): render it, then eyeball a frame —
`ffmpeg -y -sseof -0.4 -i videos/<Scene>.mp4 -update 1 frame.png` and Read the png.

## Architecture / data flow

1. **`manim/scenes/*.py`** — one `Scene` subclass per file (`MatMul`, `Backprop`, …). Pure ManimGL.
2. **`manim/render.sh`** — the headless harness. `manimgl` v1.7.2 has no `--format gif` and opens a
   GUI window if run bare, so render.sh renders mp4 with `-w` then palette-converts to gif via ffmpeg.
   Outputs land in `manim/videos/`. The `SCENES` array is the source of truth for what gets rendered.
3. **`manim/embed_into_notebook.py`** — copies gifs into `week1/assets/` and inserts a markdown cell
   (gif + Korean caption) into the notebook. Its `INSERTS` list anchors each visual to a **unique
   section-header substring** (not a fixed cell index), resolved at runtime, so insertions survive the
   notebook gaining/losing cells between deploys; cells are inserted highest-index-first. An anchor that
   matches zero or multiple cells fails loudly. `render.sh` runs it automatically at the end of every render.

### Notebook versions (project rule: always keep BOTH in sync)

Every embed run regenerates **two** notebooks from the one pristine source — never edit either by hand:

- `week1/딥러닝기초_PyTorch_전체.원본.ipynb` — **pristine source**, no visuals. The only notebook you edit
  (or re-export from the course); both versions are built from it. Committed.
- `week1/딥러닝기초_PyTorch_전체.ipynb` — **committed canonical** repo copy. gifs use the relative
  `assets/` path, so they render both in GitHub's notebook preview and in local VS Code/Jupyter.
- `week1/딥러닝기초_PyTorch_전체_배포.ipynb` — **Drive/Colab export, gitignored**. gifs use the absolute
  GitHub raw URL (`GIF_BASE_URL`, `SSU-NLP/Practical-AI-101` `main` `week1/assets/`) — the only form that
  resolves on Colab. Upload this one to Google Drive manually; it is not committed.

`embed_into_notebook.py` reads `.원본` and writes both, so re-running is safe (never double-inserts).
Because the Drive export loads gifs from GitHub raw, **`week1/assets/` must be committed and pushed**
for it to display on Colab — re-render, then push the updated gifs. To repoint the URL, edit `GIF_BASE_URL`.

**Re-syncing from a new course deploy:** when the team ships an updated notebook, overwrite
`…원본.ipynb` with it and re-run the embed (or `./render.sh`). The 10 visuals re-place correctly by
header anchor even though cell indices shift. If a section *header was renamed*, update that anchor in
`INSERTS`; the run aborts with the offending anchor if it no longer matches exactly one cell.

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
