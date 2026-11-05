# Computer Vision Study

Source code and saved results for the Introduction to Computer Vision assignments. Documentation is provided in English and Korean.

컴퓨터비전입문 과제의 소스 코드와 실행 결과를 정리한 저장소입니다.

| Assignment / 과제 | Source and guide / 코드 및 설명 | Results / 실행 결과 |
|---|---|---|
| Morphological processing / 형태학적 이미지 처리 | [assignment3](assignment3/README.md) · [Python source / 코드](assignment3/assignment3.py) | [Input and four results / 입력 및 결과](assignment3/5_comparison.png) |
| CIFAR-10 KNN | [assignment4](assignment4/README.md) · [Python source / 코드](assignment4/assignment4.py) | [Report / 결과 보고서](assignment4/results/report.md) · [Cross-validation CSV / 교차검증 CSV](assignment4/results/cv_summary.csv) |

## Repository Guide / 저장소 구성

Start with the assignment README for the method and execution steps, then open its saved results. Each assignment keeps its code and results together so that it can be reviewed without rerunning the experiment.

과제별 README에서 원리와 실행 방법을 확인한 뒤 저장된 결과를 열어볼 수 있습니다. 과제별로 코드와 결과를 함께 배치해 실험을 다시 실행하지 않아도 내용을 확인할 수 있도록 했습니다.

```text
ComputerVisionStudy/
├── README.md
├── requirements.txt
├── assignment3/
│   ├── README.md
│   ├── requirements.txt
│   ├── assignment3.py
│   ├── 0_binary.png
│   └── 1_dilation.png ... 5_comparison.png
└── assignment4/
    ├── README.md
    ├── requirements.txt
    ├── assignment4.py
    └── results/
        ├── report.md
        ├── result.json
        ├── cv_summary.csv
        ├── cv_accuracy.png
        ├── knn_2d.png
        └── details/
```

- **Morphological processing / 형태학적 처리:** Compare how a fixed neighborhood changes foreground shapes, removes small bright objects and fills small dark gaps. / 일정한 이웃 영역을 기준으로 전경 모양이 바뀌고 작은 흰 잡음과 검은 틈이 처리되는 과정을 비교합니다.
- **KNN / K-최근접 이웃:** Implement distance computation and majority voting, choose hyperparameters using validation data, and evaluate the selected setting on held-out test data. / 거리 계산과 다수결 분류를 구현하고, 검증 데이터로 설정을 선택한 뒤 별도 테스트 데이터에서 평가합니다.

## Setup / 환경 설정

Use Python 3.10 or later. Run the following commands from the repository root.

Python 3.10 이상을 사용합니다. 아래 명령은 저장소 루트에서 실행합니다.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows, activate the virtual environment with `.venv\Scripts\activate`.

Windows에서는 가상환경 활성화 명령으로 `.venv\Scripts\activate`를 사용합니다.

## 1. Morphological Processing / 형태학적 이미지 처리

Dilation, erosion, opening and closing are implemented with NumPy using a 7×7 square structuring element. The input and individual output images are included.

NumPy로 Dilation, Erosion, Opening, Closing을 구현했습니다. 모든 연산은 7×7 정사각형 구조 요소를 사용합니다. 입력 이미지와 개별 결과 이미지가 포함되어 있습니다.

```bash
python assignment3/assignment3.py
```

![Morphological processing comparison / 형태학적 처리 비교](assignment3/5_comparison.png)

## 2. KNN

KNN classifies CIFAR-10 images using raw RGB pixels. We compared k=1, 3, 5, 7, 9 and L1, L2 and cosine distances using 5-fold cross-validation, then evaluated the selected setting on a separate test set.

CIFAR-10의 원시 RGB 픽셀을 사용한 KNN 분류입니다. k=1, 3, 5, 7, 9와 L1, L2, Cosine 거리를 5-fold cross-validation으로 비교한 후, 선택한 설정을 별도 테스트 데이터에서 평가했습니다.

| Setting or metric / 조건 또는 지표 | Saved result / 저장된 결과 |
|---|---|
| Samples / 표본 수 | 5,000 training / 학습, 1,000 test / 테스트 |
| Seed | 42 |
| Selected setting / 선택된 설정 | L1 (Manhattan), k=9 |
| Mean CV accuracy / 평균 교차검증 정확도 | 28.54% |
| Test accuracy / 테스트 정확도 | 30.00% |

These results use a subset of CIFAR-10, not the full dataset. The original dataset is excluded from this repository; follow the [data preparation and execution guide](assignment4/README.md) to download it.

전체 CIFAR-10 데이터 실험 결과가 아닙니다. CIFAR-10 원본 데이터는 저장소에 포함하지 않았으며, [데이터 준비 및 실행 방법](assignment4/README.md)을 따라 다운로드합니다.

```bash
python assignment4/assignment4.py
```

![Cross-validation accuracy / 교차검증 정확도](assignment4/results/cv_accuracy.png)

Detailed CSV, JSON, report and image files are included in [results](assignment4/results). Running the script overwrites the numerical result files.

상세 결과는 [results](assignment4/results)에 CSV, JSON, 보고서와 이미지로 포함되어 있습니다. 실행하면 수치 결과 파일을 다시 저장합니다.
