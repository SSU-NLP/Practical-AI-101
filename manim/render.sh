#!/usr/bin/env bash
# Headless ManimGL render harness: writes mp4, then converts to gif with ffmpeg.
# manimgl v1.7.2 has no --format gif, so we render mp4 (-w) and palette-convert.
# Usage:
#   ./render.sh                 # render every scene below (mp4 + gif)
#   ./render.sh Broadcasting    # render only scenes whose name matches the filter
#   Q=-l ./render.sh            # quality: -l low / -m medium(default) / -hq 1080p
# Outputs: manim/videos/<Scene>.mp4 and manim/videos/<Scene>.gif
set -euo pipefail
cd "$(dirname "$0")"
# venv layout differs per OS: bin/ on macOS+Linux, Scripts/ on Windows (Git Bash)
if [ -f ../.venv/bin/activate ]; then source ../.venv/bin/activate
else source ../.venv/Scripts/activate; fi

Q="${Q:--m}"                 # default medium (720p30): good size/quality for notebook gifs
GIF_FPS="${GIF_FPS:-12}"
GIF_W="${GIF_W:-720}"
FILTER="${1:-}"

# scene file : Scene class
SCENES=(
  "scenes/tensor_buildup.py:TensorBuildup"
  "scenes/broadcasting.py:Broadcasting"
  "scenes/matmul.py:MatMul"
  "scenes/linear_layer.py:LinearLayerNeuron"
  "scenes/mlp_forward.py:MLPForward"
  "scenes/backprop.py:Backprop"
  "scenes/gradient_descent.py:GradientDescent"
  "scenes/training_loop.py:TrainingLoop"
  "scenes/sentiment_overview.py:SentimentOverview"
  "scenes/mean_pooling.py:MeanPooling"
  "scenes/embedding_lookup.py:EmbeddingLookup"
  "scenes/wordwindow_overview.py:WordWindowOverview"
  "scenes/embedding_training.py:EmbeddingTraining"
  # --- week 2 (LLM API / agent) ---
  "scenes/api_round_trip.py:ApiRoundTrip"
  "scenes/messages_context.py:MessagesContext"
  "scenes/function_calling.py:FunctionCalling"
  "scenes/agent_loop.py:AgentLoop"
  # --- week 3 (RAG) --- gif는 week3/assets/ 에 수동 복사 (embed 스크립트 없음)
  "scenes/sentence_embedding.py:SentenceEmbedding"
  "scenes/chunking.py:Chunking"
  "scenes/vector_db.py:VectorDB"
)

to_gif() {  # mp4 -> gif via two-pass palette (crisp text, small size)
  local mp4="$1" gif="${1%.mp4}.gif"
  ffmpeg -y -i "$mp4" \
    -vf "fps=${GIF_FPS},scale=${GIF_W}:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" \
    "$gif" >/dev/null 2>&1
  echo "    gif: $gif"
}

for pair in "${SCENES[@]}"; do
  file="${pair%%:*}"; scene="${pair##*:}"
  [ -n "$FILTER" ] && [[ "$scene" != *"$FILTER"* ]] && continue
  echo "=== $scene ==="
  manimgl "$file" "$scene" -w "$Q"
  to_gif "videos/${scene}.mp4"
done

echo "=== done. outputs in $(pwd)/videos/ ==="
ls -1 videos/*.mp4 videos/*.gif 2>/dev/null || true

# Project rule: always regenerate BOTH notebook versions (deliverable + local preview).
echo "=== embedding into notebooks ==="
python embed_into_notebook.py   # week 1
python embed_week2.py           # week 2 (edits the single notebook in place)
