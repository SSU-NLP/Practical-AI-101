"""Insert manim gif visualizations into the week-1 notebook.
Reads the pristine .원본.ipynb and ALWAYS writes BOTH versions (project rule):
  - 딥러닝기초_PyTorch_전체.ipynb       committed: gifs via relative assets/ (renders on GitHub & local VS Code)
  - 딥러닝기초_PyTorch_전체_배포.ipynb   gitignored: gifs via GitHub raw URL -> upload to Google Drive/Colab
render.sh calls this automatically after rendering, so both stay in sync.
"""
import json, os, shutil

WEEK1 = os.path.join(os.path.dirname(__file__), "..", "week1")
# SRC is the pristine source (no visuals); DST is the actual practice notebook.
# Keeping them separate makes this script safely re-runnable (no double-insert).
SRC = os.path.join(WEEK1, "딥러닝기초_PyTorch_전체.원본.ipynb")
DST = os.path.join(WEEK1, "딥러닝기초_PyTorch_전체.ipynb")          # committed: relative paths
DST_DEPLOY = os.path.join(WEEK1, "딥러닝기초_PyTorch_전체_배포.ipynb")  # gitignored: raw URL, for Drive/Colab

# The notebook is hosted on Google Drive/Colab where relative paths don't resolve,
# so gifs are referenced by absolute GitHub raw URL. The gifs must be pushed to this
# repo/branch/path for the URLs to load. Set to "assets" for local-only (relative) use.
GIF_BASE_URL = "https://raw.githubusercontent.com/SSU-NLP/Practical-AI-101/refs/heads/main/week1/assets"
ASSETS = os.path.join(WEEK1, "assets")
VIDEOS = os.path.join(os.path.dirname(__file__), "videos")

# Each visual is anchored to a UNIQUE markdown-header substring (not a fixed cell
# index) so insertions survive the notebook gaining/losing cells between deploys.
# (anchor_substring, title, gif_basename, korean_caption)
INSERTS = [
    ("## Part 1: 텐서", "텐서 빌드업 (Tensors)", "TensorBuildup",
     "숫자를 모으면 벡터, 벡터(컬럼)를 모으면 행렬, 행렬을 모으면 3D 텐서 — 차원이 쌓이며 텐서가 됩니다."),
    ("형태(shape)", "행렬 곱 (matmul)", "MatMul",
     "두 행렬의 행·열 내적이 결과 한 칸을 만들고, 안쪽 차원이 상쇄되어 출력 모양이 정해집니다."),
    ("### 브로드캐스팅", "브로드캐스팅 (Broadcasting)", "Broadcasting",
     "크기가 1인 차원이 실제로 늘어나(stretch) 같은 모양이 된 뒤 원소별로 더해집니다."),
    ("## Part 2: 자동 미분", "자동 미분 · 역전파 (Backpropagation)", "Backprop",
     "순전파(파랑)는 입력→은닉→출력→손실로 흐르고, backward()는 기울기(빨강)를 손실→출력→은닉→입력으로 거꾸로 흘려 각 층의 가중치 기울기를 연쇄 법칙으로 구합니다."),
    ("### 선형 레이어", "선형 레이어 = 뉴런 = Wx+b", "LinearLayerNeuron",
     "nn.Linear가 입력의 가중합+편향이라는 점, 그리고 그것이 곧 행렬 연산 Wx+b임을 보여줍니다."),
    ("### 커스텀 모듈", "MLP 순전파 (Forward Pass)", "MLPForward",
     "전체 파이프라인(Linear→ReLU→Linear→Sigmoid)을 한눈에 보여준 뒤 각 단계를 하이라이트하며 최종 출력이 어떻게 나오는지 따라갑니다."),
    ("## Part 4: 최적화", "경사 하강법 (Gradient Descent)", "GradientDescent",
     "L(x)=3x² 위의 공이 기울기(6x)의 반대 방향으로 한 걸음씩 내려가 최솟값에 수렴합니다."),
    ("학습 루프(Training Loop)", "학습 루프 · 옵티마이저 (Training Loop)", "TrainingLoop",
     "zero_grad→forward→loss→backward→step 사이클을 돌며 w ← w - η∇ 로 파라미터를 갱신하고, 에폭마다 손실이 줄어듭니다."),
    ("실전 예제 ① — 영화 리뷰 감정 분석", "실전 예제 ① 감정 분석 — 전체 흐름", "SentimentOverview",
     "문장 → 토큰화/인덱스 → 임베딩(L,D) → 평균 풀링(D) → Linear+sigmoid → 긍/부정. 핵심은 '문장 = 단어 임베딩의 평균'입니다."),
    ("실전 예제 ② — Word Window", "실전 예제 ② Word Window — 전체 흐름", "WordWindowOverview",
     "2S+1 슬라이딩 윈도우가 토큰 위를 미끄러지며, 각 윈도우를 embed→flatten→Linear+Tanh→Linear+sigmoid 로 통과시켜 단어별 LOCATION 확률을 냅니다."),
]


def md_cell(title, gif, caption, base):
    note = ("gif는 같은 저장소의 assets/ 에서 로드됩니다 (GitHub·로컬용)" if base == "assets"
            else "gif는 GitHub raw URL에서 로드됩니다 (Drive/Colab 배포용)")
    src = [
        f"### 🎬 시각 자료: {title}\n",
        "\n",
        f"{caption}\n",
        "\n",
        f"![{gif}]({base}/{gif}.gif)\n",
        "\n",
        f"> ManimGL로 제작 · {note}\n",
    ]
    return {"cell_type": "markdown", "metadata": {}, "source": src}


def find_after(cells, anchor):
    """Index of the single markdown cell containing `anchor`. Fails loudly if not unique."""
    hits = [i for i, c in enumerate(cells)
            if c["cell_type"] == "markdown" and anchor in "".join(c["source"])]
    if len(hits) != 1:
        raise SystemExit(f"anchor matched {len(hits)} cells (need exactly 1): {anchor!r}")
    return hits[0]


def build(base, dst):
    with open(SRC, encoding="utf-8") as f:
        nb = json.load(f)
    cells = nb["cells"]
    # resolve anchors against the pristine cells, then insert highest-index-first
    resolved = [(find_after(cells, anchor), title, gif, caption)
                for anchor, title, gif, caption in INSERTS]
    for idx, title, gif, caption in sorted(resolved, key=lambda r: r[0], reverse=True):
        cells.insert(idx + 1, md_cell(title, gif, caption, base))
    with open(dst, "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
    print(f"wrote {os.path.basename(dst)}  (base: {base}, cells: {len(cells)})")


def main():
    os.makedirs(ASSETS, exist_ok=True)
    for _, _, gif, _ in INSERTS:
        src_gif = os.path.join(VIDEOS, f"{gif}.gif")
        if os.path.exists(src_gif):
            shutil.copy(src_gif, os.path.join(ASSETS, f"{gif}.gif"))
        else:
            print(f"  [skip] not rendered yet: {gif}.gif")

    # Project rule: always produce BOTH versions so they never drift apart.
    build("assets", DST)              # committed: relative paths (renders on GitHub & local VS Code)
    build(GIF_BASE_URL, DST_DEPLOY)   # gitignored: GitHub raw URL, upload to Google Drive/Colab


if __name__ == "__main__":
    main()
