"""Insert manim gif visualizations into the week-2 notebook.

Unlike week 1 there is no pristine `.원본` source: the week-2 notebook is edited
directly (by several people), so this script edits it IN PLACE and is safe to
re-run — every inserted cell is tagged, and tagged cells are removed before the
fresh ones go in.

The notebook is uploaded to Colab, where relative paths do not resolve, so gifs
are referenced by absolute GitHub raw URL. The gifs must be committed and pushed
to that branch/path for the images to load.
"""
import json, os, shutil

WEEK2 = os.path.join(os.path.dirname(__file__), "..", "week2")
NOTEBOOK = os.path.join(WEEK2, "2차_LLM_API_Agent_실습.ipynb")
ASSETS = os.path.join(WEEK2, "assets")
VIDEOS = os.path.join(os.path.dirname(__file__), "videos")

# Branch the gifs are served from. Keep in sync with where week2/assets lives.
BRANCH = "main"
GIF_BASE_URL = ("https://raw.githubusercontent.com/SSU-NLP/Practical-AI-101"
                f"/refs/heads/{BRANCH}/week2/assets")

TAG = "<!-- manim-visual -->"   # marks our cells so re-runs replace instead of duplicate

# (anchor_substring, title, gif_basename, korean_caption)
INSERTS = [
    ("## 3. 첫 번째 응답 받기", "API 요청과 응답 한 번 왕복", "ApiRoundTrip",
     "내 노트북이 `messages` 를 담아 요청을 보내면 서버의 모델이 답변 하나를 돌려줍니다. "
     "서버는 이 호출을 기억하지 않으며, 주고받은 토큰 수만큼 비용이 발생합니다."),
    ("## 6. 대화 이어가기", "대화 맥락은 매번 다시 보낸다", "MessagesContext",
     "턴이 늘어날 때마다 `messages` 리스트 전체를 다시 전송합니다. "
     "모델의 답변(assistant)까지 쌓아야 맥락이 이어지고, 그만큼 prompt 토큰과 비용도 함께 늘어납니다."),
    ("## 7. 함수 호출(Function Calling)", "함수 호출 5단계", "FunctionCalling",
     "질문 → 모델의 호출 요청(`tool_calls`) → 우리 코드가 실제 실행 → `role:\"tool\"` 로 결과 전달 → 최종 답변. "
     "모델은 어떤 함수를 어떤 인자로 부를지 정할 뿐, 실행은 언제나 우리 코드가 합니다."),
    ("## 9. 에이전트(Agent)", "에이전트 루프", "AgentLoop",
     "도구 호출 요청이 없어질 때까지 같은 왕복을 반복합니다. "
     "모델이 스스로 도구를 골라 쓰다가 더 부를 도구가 없으면 최종 답변을 내고 루프가 끝납니다."),
]


def md_cell(title, gif, caption):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "id": f"viz-{gif.lower()}",
        "source": [
            f"{TAG}\n",
            f"### 🎬 시각 자료: {title}\n",
            "\n",
            f"{caption}\n",
            "\n",
            f"![{gif}]({GIF_BASE_URL}/{gif}.gif)\n",
            "\n",
            "> ManimGL로 제작 · gif는 GitHub raw URL에서 로드됩니다 (Colab 배포용)\n",
        ],
    }


def find_anchor(cells, anchor):
    """Index of the single markdown cell containing `anchor`. Fails loudly if not unique."""
    hits = [i for i, c in enumerate(cells)
            if c["cell_type"] == "markdown" and anchor in "".join(c["source"])]
    if len(hits) != 1:
        raise SystemExit(f"anchor matched {len(hits)} cells (need exactly 1): {anchor!r}")
    return hits[0]


def main():
    os.makedirs(ASSETS, exist_ok=True)
    for _, _, gif, _ in INSERTS:
        src = os.path.join(VIDEOS, f"{gif}.gif")
        if os.path.exists(src):
            shutil.copy(src, os.path.join(ASSETS, f"{gif}.gif"))
        else:
            print(f"  [skip] not rendered yet: {gif}.gif")

    with open(NOTEBOOK, encoding="utf-8") as f:
        nb = json.load(f)

    # drop previously inserted cells so this stays re-runnable
    before = len(nb["cells"])
    nb["cells"] = [c for c in nb["cells"] if TAG not in "".join(c["source"])]
    removed = before - len(nb["cells"])

    cells = nb["cells"]
    resolved = [(find_anchor(cells, anchor), title, gif, caption)
                for anchor, title, gif, caption in INSERTS]
    for idx, title, gif, caption in sorted(resolved, key=lambda r: r[0], reverse=True):
        cells.insert(idx + 1, md_cell(title, gif, caption))

    with open(NOTEBOOK, "w", encoding="utf-8", newline="\n") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print(f"week2 notebook: -{removed} old / +{len(INSERTS)} visual cells (total {len(cells)})")


if __name__ == "__main__":
    main()
