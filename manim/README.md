# manim 시각 자료 (ManimGL / 3b1b)

1주차 실습 노트북용 애니메이션을 [3b1b/manim (ManimGL)](https://github.com/3b1b/manim)으로 제작·렌더링하는 작업 공간.

## 1. Skill — 어떻게 manim을 쓰는가 (정의)

`from manimlib import *` · `manimgl` CLI를 쓰는 **ManimGL**(커뮤니티판 `manim`과 비호환).
사용법 정의는 설치된 스킬에 들어있다:

- 위치: [`.claude/skills/manimgl-best-practices/`](../.claude/skills/manimgl-best-practices/)
- 출처: [`adithya-s-k/manim_skill`](https://github.com/adithya-s-k/manim_skill) (인터넷에 공개된 ManimGL 전용 Claude 스킬을 그대로 사용)
- 핵심 규칙: `ShowCreation`(≠Create), `Tex(R"...")`(≠MathTex), `self.frame`(≠self.camera.frame), `manimgl` CLI.
  `rules/*.md`(mobjects·animations·tex·camera…)와 `examples/*.py`에 상세.

> 라이선스: 스킬의 **예제 코드는 CC BY-NC-SA 4.0(비상업)**. 그래서 이 폴더의 씬들은 예제를 복사하지 않고
> ManimGL API 관용구만 참고해 **새로 작성**했다. ManimGL 라이브러리 자체는 MIT.

## 2. Harness — 헤드리스 렌더 러너

`manimgl`은 v1.7.2에 `--format gif`가 없고, 그냥 실행하면 GUI 창을 연다.
[`render.sh`](render.sh)가 이를 감싸 **창 없이 mp4 렌더 → ffmpeg로 gif 변환**까지 한다.

```bash
source ../.venv/bin/activate     # 처음 1회: python3 -m venv ../.venv && pip install manimgl
./render.sh                      # 5개 씬 전부 (mp4 + gif)
./render.sh Broadcasting         # 이름으로 필터
Q=-l ./render.sh                 # 빠른 미리보기 품질 (-l 저화질 / -m 기본 / -hq 1080p)
```

출력: `videos/<Scene>.mp4`, `videos/<Scene>.gif`.
필요 도구: `ffmpeg`, LaTeX(MacTeX) — 둘 다 시스템에 설치돼 있어야 함.

## 3. 씬 (13개, 고차원 연산 시각화)

| 파일 | Scene | 개념 | 노트북 위치 |
|---|---|---|---|
| `scenes/tensor_buildup.py` | `TensorBuildup` | 스칼라→벡터→행렬→3D 텐서 | ## Part 1 텐서 |
| `scenes/matmul.py` | `MatMul` | (3,2)@(2,4)→(3,4) 행·열 내적 | 행렬 형태(shape) |
| `scenes/broadcasting.py` | `Broadcasting` | (3,1)+(1,4)→(3,4) 차원 늘어남 | ### 브로드캐스팅 |
| `scenes/backprop.py` | `Backprop` | 신경망 역전파 (forward 파랑 / backward 빨강) | ## Part 2 자동 미분 |
| `scenes/linear_layer.py` | `LinearLayerNeuron` | 뉴런 ↔ Wx+b | ### 선형 레이어 |
| `scenes/mlp_forward.py` | `MLPForward` | 전체 파이프라인 + 단계별 하이라이트 | ### 커스텀 모듈 |
| `scenes/gradient_descent.py` | `GradientDescent` | L=3x² 경사 하강 | ## Part 4 최적화 |
| `scenes/training_loop.py` | `TrainingLoop` | 학습 루프 사이클 + SGD 갱신 | ### 학습 루프 |
| `scenes/sentiment_overview.py` | `SentimentOverview` | 감정분석 전체 흐름(임베딩 평균) | Part 2 실전예제 ① |
| `scenes/mean_pooling.py` | `MeanPooling` | 평균 풀링 = 화살표들의 무게중심 | 임베딩 평균 풀링 |
| `scenes/embedding_lookup.py` | `EmbeddingLookup` | nn.Embedding = 룩업 테이블(word→index→행) | 단어를 임베딩으로 변환 |
| `scenes/wordwindow_overview.py` | `WordWindowOverview` | 슬라이딩 윈도우 = 문맥으로 jordan 구분 | Part 3 실전예제 ② |
| `scenes/embedding_training.py` | `EmbeddingTraining` | 문맥이 임베딩을 두 쪽으로 학습시킴 | WW PCA 보너스 |

씬 추가: `scenes/`에 `.py` 작성 → `render.sh`의 `SCENES` 배열에 한 줄 추가.

## 4. 노트북 임베드

[`embed_into_notebook.py`](embed_into_notebook.py)가 gif를 `week1/assets/`로 복사하고
각 섹션 헤더 바로 아래에 시각 자료 마크다운 셀을 삽입한
`week1/딥러닝기초_PyTorch_전체_시각자료.ipynb`(원본 비파괴 사본)를 만든다.

```bash
python embed_into_notebook.py
```
