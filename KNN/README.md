# CIFAR-10 KNN

Classify CIFAR-10 images with KNN, compare distance metrics and k values using 5-fold cross-validation, then test the selected setting.

KNN으로 CIFAR-10 이미지를 분류합니다. 5-fold 교차검증으로 거리 함수와 k를 비교한 뒤 선택한 설정을 테스트합니다.

## Algorithm Flow / 알고리즘 흐름

1. **Load and sample / 데이터 준비:** Select 5,000 training and 1,000 test images with balanced class proportions; use seed 42. / 클래스 비율을 유지해 학습 5,000장·테스트 1,000장을 선택하며 seed는 42입니다.
2. **Preprocess / 전처리:** Flatten each RGB image into 3,072 features and divide pixel values by 255. / RGB 이미지를 3,072차원 벡터로 펼치고 픽셀을 255로 나눕니다.
3. **Train / 학습:** Store training images and labels. / 학습 이미지와 정답을 저장합니다.
4. **Predict / 예측:** Compute distances, select the nearest k images and predict by majority vote. Voting ties select the smaller class ID. / 거리를 계산해 가까운 k개 이미지를 선택하고 다수결로 예측합니다. 투표 동률이면 작은 클래스 ID를 선택합니다.
5. **Validate / 검증:** Compare L1 (Manhattan), L2 (Euclidean) and cosine with k=1, 3, 5, 7, 9. Each fold uses 4,000 training and 1,000 validation images. Select the highest mean validation accuracy across five folds. / L1·L2·Cosine과 k=1, 3, 5, 7, 9를 비교합니다. Fold마다 학습 4,000장·검증 1,000장을 사용하고 다섯 fold의 평균 정확도로 설정을 선택합니다.
6. **Test / 테스트:** Use all 5,000 training images with the selected setting and evaluate the separate 1,000-image test subset. / 선택한 설정으로 학습 5,000장을 모두 사용해 별도 테스트 표본 1,000장을 평가합니다.

Code / 코드: [assignment4.py](assignment4.py)

## Results / 실행 결과

### Cross-validation / 교차검증

Mean validation accuracy across five folds (%).

다섯 fold의 평균 검증 정확도(%)입니다.

| k | L1 (Manhattan) | L2 (Euclidean) | Cosine |
|---:|---:|---:|---:|
| 1 | 26.90 | 25.48 | 27.74 |
| 3 | 26.30 | 23.84 | 25.76 |
| 5 | 28.04 | 26.08 | 26.84 |
| 7 | 27.88 | 25.88 | 27.08 |
| 9 | 28.54 | 26.50 | 27.98 |

![Cross-validation accuracy / 교차검증 정확도](results/cv_accuracy.png)

**L1, k=9** achieved the highest mean accuracy of **28.54%**. All three metrics performed best at k=9 among the tested values, but increasing k did not always improve accuracy.

**L1, k=9**가 평균 정확도 **28.54%**로 가장 높았습니다. 세 거리 함수 모두 후보 중 k=9에서 가장 높았지만, k가 커질 때마다 정확도가 좋아지지는 않았습니다.

### Test / 테스트

The selected setting correctly classified 300 of 1,000 separate test images.

선택한 설정으로 별도 테스트 이미지 1,000장 중 300장을 맞혔습니다.


| Setting or metric / 조건 및 지표 | Result / 결과 |
|---|---:|
| Selected setting / 선택한 설정 | L1 (Manhattan), k=9 |
| Mean CV accuracy / 평균 검증 정확도 | 28.54% |
| Test accuracy / 테스트 정확도 | 30.00% |
| Macro precision | 37.20% |
| Macro recall | 30.00% |
| Macro F1 | 28.61% |

These are single-seed results on a CIFAR-10 subset, not the full dataset. Macro metrics average scores across the ten classes. Detailed CSV and JSON records are saved in [results](results).

전체 CIFAR-10이 아닌 부분집합의 단일 seed 결과입니다. Macro 지표는 열 개 클래스의 점수를 평균한 값입니다. 상세 CSV·JSON 기록은 [results](results)에 보관했습니다.

## Data and Run / 데이터 준비 및 실행

From the repository root, install dependencies and download the **CIFAR-10 python version** from the [official page](https://www.cs.toronto.edu/~kriz/cifar.html). The dataset is excluded from the repository. On macOS/Linux:

저장소 루트에서 의존성을 설치하고 [공식 페이지](https://www.cs.toronto.edu/~kriz/cifar.html)의 **CIFAR-10 python version**을 받습니다. 원본 데이터는 저장소에 포함하지 않았습니다. macOS/Linux에서는 다음 명령을 사용합니다.

```bash
python -m pip install -r KNN/requirements.txt
curl -fL https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz -o KNN/cifar-10-python.tar.gz
tar -xzf KNN/cifar-10-python.tar.gz -C KNN
python KNN/assignment4.py
```

Place `data_batch_1`–`data_batch_5`, `test_batch` and `batches.meta` inside `KNN/cifar-10-batches-py/`. Running the script overwrites numerical results; plots and Markdown reports are maintained separately. `knn_2d.png` is a synthetic illustration, not a CIFAR-10 test result.

`KNN/cifar-10-batches-py/` 안에 `data_batch_1`–`data_batch_5`, `test_batch`, `batches.meta`가 있어야 합니다. 실행하면 수치 결과를 덮어쓰며 그래프와 Markdown 보고서는 별도로 관리합니다. `knn_2d.png`는 원리 설명용 가상 예시이며 CIFAR-10 테스트 결과가 아닙니다.
