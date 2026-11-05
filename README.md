# Computer Vision Study

Source code and results for two Introduction to Computer Vision assignments. Each guide explains the algorithm flow and saved results in English and Korean.

컴퓨터비전입문의 두 과제에 대한 소스 코드와 실행 결과입니다. 각 과제 문서에 알고리즘 흐름과 결과를 영어·한국어로 정리했습니다.

| Assignment / 과제 | Guide and code / 설명 및 코드 | Results / 결과 |
|---|---|---|
| Morphological Processing / 형태학적 처리 | [README](Morphological-Techniques/README.md) · [Python](Morphological-Techniques/assignment3.py) | [Comparison / 비교 이미지](Morphological-Techniques/5_comparison.png) |
| CIFAR-10 KNN | [README](KNN/README.md) · [Python](KNN/assignment4.py) | [Tables and plot / 결과 표·그래프](KNN/README.md) |

## Setup / 환경 설정

Use Python 3.10 or later. Run these commands from the repository root.

Python 3.10 이상을 사용하며, 저장소 루트에서 실행합니다.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows, activate with `.venv\Scripts\activate`.

Windows에서는 `.venv\Scripts\activate`로 가상환경을 활성화합니다.

## Run / 실행

```bash
python Morphological-Techniques/assignment3.py
python KNN/assignment4.py
```

For KNN, first follow the [CIFAR-10 download instructions](KNN/README.md). Input and result images for morphology, and numerical results and plots for KNN, are included in the repository.

KNN 실행 전 [CIFAR-10 다운로드 안내](KNN/README.md)를 따라 데이터를 준비합니다. 형태학 과제의 입력·결과 이미지와 KNN의 수치 결과·그래프는 저장소에 포함되어 있습니다.
