# Morphological Processing / 형태학적 이미지 처리

## Input Image / 입력 이미지

작은 잡음과 틈이 있는 이진 꽃 이미지를 사용해 각 연산의 효과를 비교합니다.

This binary flower image has small noise and gaps, so the effects are easy to see.

![Original binary image / 원본 이진 이미지](0_binary.png)

## Methods / 처리 방법

코드: [assignment3.py](assignment3.py). 모든 연산은 7×7 정사각형 구조 요소를 사용합니다.

Code: [assignment3.py](assignment3.py). All methods use a 7×7 square structuring element.

- **Dilation / 팽창:** Expands white regions. / 흰 영역을 확장합니다.
- **Erosion / 침식:** Shrinks white regions. / 흰 영역을 축소합니다.
- **Opening / 열림:** Erosion followed by dilation removes small white noise, but may thin the petals. / 침식 후 팽창하여 작은 흰 잡음을 제거하지만 꽃잎이 가늘어질 수 있습니다.
- **Closing / 닫힘:** Dilation followed by erosion fills small black gaps and thickens the petals. / 팽창 후 침식하여 작은 검은 틈을 메우고 꽃잎을 두껍게 만듭니다.

## Results / 실행 결과

Individual results / 개별 결과: [Dilation](1_dilation.png) · [Erosion](2_erosion.png) · [Opening](3_opening.png) · [Closing](4_closing.png)

![Input and results / 입력 및 처리 결과](5_comparison.png)

## Run / 실행 방법

Python 3.10 이상을 사용하고, 저장소 루트에서 실행합니다.

Use Python 3.10 or later. From the repository root:

```bash
python -m pip install -r assignment3/requirements.txt
python assignment3/assignment3.py
```

포함된 `0_binary.png`를 입력으로 사용합니다. 실행하면 이 폴더에 네 결과 이미지와 `5_comparison.png`를 저장하며 기존 결과를 덮어씁니다. NumPy로 형태학 연산을 수행하고 Pillow로 이미지를 읽고 저장하며 비교 이미지를 구성합니다.

The included `0_binary.png` is the input. The script saves the four result images and `5_comparison.png` in this folder, replacing the existing results. NumPy performs the morphological operations; Pillow loads, saves and arranges the images.
