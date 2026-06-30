"""Insert manim gif visualizations into the week-1 notebook (non-destructive).
Reads the original .ipynb, inserts a markdown cell after each target cell,
writes a new *_시각자료.ipynb next to it. Gifs are referenced as assets/<name>.gif.
"""
import json, os, shutil

WEEK1 = os.path.join(os.path.dirname(__file__), "..", "week1")
# SRC is the pristine source (no visuals); DST is the actual practice notebook.
# Keeping them separate makes this script safely re-runnable (no double-insert).
SRC = os.path.join(WEEK1, "딥러닝기초_PyTorch_전체.원본.ipynb")
DST = os.path.join(WEEK1, "딥러닝기초_PyTorch_전체.ipynb")
ASSETS = os.path.join(WEEK1, "assets")
VIDEOS = os.path.join(os.path.dirname(__file__), "videos")

# after_cell_index : (title, gif_basename, korean_caption)
INSERTS = {
    5: ("텐서 빌드업 (Tensors)", "TensorBuildup",
        "숫자를 모으면 벡터, 벡터(컬럼)를 모으면 행렬, 행렬을 모으면 3D 텐서 — 차원이 쌓이며 텐서가 됩니다."),
    20: ("행렬 곱 (matmul)", "MatMul",
         "두 행렬의 행·열 내적이 결과 한 칸을 만들고, 안쪽 차원이 상쇄되어 출력 모양이 정해집니다."),
    37: ("브로드캐스팅 (Broadcasting)", "Broadcasting",
         "크기가 1인 차원이 실제로 늘어나(stretch) 같은 모양이 된 뒤 원소별로 더해집니다."),
    58: ("자동 미분 · 역전파 (Backpropagation)", "Backprop",
         "순전파(파랑)는 입력→은닉→출력→손실로 흐르고, backward()는 기울기(빨강)를 손실→출력→은닉→입력으로 거꾸로 흘려 각 층의 가중치 기울기를 연쇄 법칙으로 구합니다."),
    70: ("선형 레이어 = 뉴런 = Wx+b", "LinearLayerNeuron",
         "nn.Linear가 입력의 가중합+편향이라는 점, 그리고 그것이 곧 행렬 연산 Wx+b임을 보여줍니다."),
    81: ("MLP 순전파 (Forward Pass)", "MLPForward",
         "전체 파이프라인(Linear→ReLU→Linear→Sigmoid)을 한눈에 보여준 뒤 각 단계를 하이라이트하며 최종 출력이 어떻게 나오는지 따라갑니다."),
    91: ("경사 하강법 (Gradient Descent)", "GradientDescent",
         "L(x)=3x² 위의 공이 기울기(6x)의 반대 방향으로 한 걸음씩 내려가 최솟값에 수렴합니다."),
    98: ("학습 루프 · 옵티마이저 (Training Loop)", "TrainingLoop",
         "zero_grad→forward→loss→backward→step 사이클을 돌며 w ← w - η∇ 로 파라미터를 갱신하고, 에폭마다 손실이 줄어듭니다."),
    105: ("실전 예제 ① 감정 분석 — 전체 흐름", "SentimentOverview",
          "문장 → 토큰화/인덱스 → 임베딩(L,D) → 평균 풀링(D) → Linear+sigmoid → 긍/부정. 핵심은 '문장 = 단어 임베딩의 평균'입니다."),
    125: ("실전 예제 ② Word Window — 전체 흐름", "WordWindowOverview",
          "2S+1 슬라이딩 윈도우가 토큰 위를 미끄러지며, 각 윈도우를 embed→flatten→Linear+Tanh→Linear+sigmoid 로 통과시켜 단어별 LOCATION 확률을 냅니다."),
}


def md_cell(title, gif, caption):
    src = [
        f"### 🎬 시각 자료: {title}\n",
        "\n",
        f"{caption}\n",
        "\n",
        f"![{gif}](assets/{gif}.gif)\n",
        "\n",
        f"> 고화질 영상: [`manim/videos/{gif}.mp4`](../manim/videos/{gif}.mp4) · ManimGL로 제작\n",
    ]
    return {"cell_type": "markdown", "metadata": {}, "source": src}


def main():
    os.makedirs(ASSETS, exist_ok=True)
    for _, gif, _ in INSERTS.values():
        shutil.copy(os.path.join(VIDEOS, f"{gif}.gif"), os.path.join(ASSETS, f"{gif}.gif"))

    with open(SRC, encoding="utf-8") as f:
        nb = json.load(f)
    cells = nb["cells"]

    # insert from highest index downward so earlier indices stay valid
    for after in sorted(INSERTS, reverse=True):
        title, gif, caption = INSERTS[after]
        cells.insert(after + 1, md_cell(title, gif, caption))

    with open(DST, "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
    print("wrote", DST)
    print("cells:", len(cells), "(+%d)" % len(INSERTS))


if __name__ == "__main__":
    main()
