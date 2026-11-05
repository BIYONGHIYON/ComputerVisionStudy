# CIFAR-10 KNN 실험 결과

## 실험 조건

CIFAR-10에서 클래스 비율을 유지해 학습 5,000장·테스트 1,000장을 사용했다. 전체 데이터 실험은 아니다. RGB 이미지를 3,072차원 벡터로 표현하고 픽셀을 255로 나누었다. seed는 42이다.

KNN은 train에서 데이터와 label을 저장하고, predict에서 가까운 k개의 이웃을 찾아 majority voting으로 분류했다. k=1, 3, 5, 7, 9와 L1(Manhattan), L2(Euclidean), Cosine을 비교했다.

## 5-fold cross-validation

학습 데이터를 5등분하여 매번 4,000장으로 train, 1,000장으로 validation을 수행했다. 아래는 각 fold의 Validation Accuracy와 5개 fold의 평균이다. 단위는 %이다.

| Distance Metric | k | Fold 1 | Fold 2 | Fold 3 | Fold 4 | Fold 5 | 평균 |
|---|---:|---:|---:|---:|---:|---:|---:|
| L1 (Manhattan) | 1 | 24.20 | 28.80 | 28.10 | 26.90 | 26.50 | 26.90 |
| L1 (Manhattan) | 3 | 24.90 | 26.90 | 25.30 | 26.50 | 27.90 | 26.30 |
| L1 (Manhattan) | 5 | 26.90 | 28.30 | 27.20 | 28.20 | 29.60 | 28.04 |
| L1 (Manhattan) | 7 | 28.70 | 27.40 | 27.70 | 27.10 | 28.50 | 27.88 |
| L1 (Manhattan) | 9 | 28.60 | 28.90 | 28.30 | 27.90 | 29.00 | 28.54 |
| L2 (Euclidean) | 1 | 23.70 | 25.20 | 26.80 | 25.90 | 25.80 | 25.48 |
| L2 (Euclidean) | 3 | 21.50 | 23.90 | 24.80 | 24.80 | 24.20 | 23.84 |
| L2 (Euclidean) | 5 | 25.10 | 27.80 | 26.30 | 26.10 | 25.10 | 26.08 |
| L2 (Euclidean) | 7 | 25.10 | 26.00 | 25.60 | 26.70 | 26.00 | 25.88 |
| L2 (Euclidean) | 9 | 25.90 | 27.50 | 25.30 | 27.10 | 26.70 | 26.50 |
| Cosine | 1 | 27.30 | 28.50 | 28.50 | 26.50 | 27.90 | 27.74 |
| Cosine | 3 | 25.20 | 24.80 | 27.20 | 25.50 | 26.10 | 25.76 |
| Cosine | 5 | 26.20 | 26.70 | 28.40 | 26.50 | 26.40 | 26.84 |
| Cosine | 7 | 27.60 | 28.10 | 27.20 | 25.70 | 26.80 | 27.08 |
| Cosine | 9 | 29.10 | 28.30 | 28.30 | 26.70 | 27.50 | 27.98 |

Validation Accuracy가 가장 높은 **L1, k=9**를 선택했다. 이 설정의 fold 간 표본 표준편차는 0.45%p이다.

## Test 결과

선택한 설정으로 학습 5,000장을 저장하고 별도 test set 1,000장을 평가했다.

| 지표 | 결과 |
|---|---:|
| Accuracy | 30.00% |
| Precision (macro) | 37.20% |
| Recall (macro) | 30.00% |
| F1-score (macro) | 28.61% |

Precision·Recall·F1은 10개 클래스별 지표를 평균했다. 각 클래스의 test 이미지 수가 같아서 Accuracy와 macro Recall이 같다.

## 비교 및 설명

세 Distance Metric 모두 k=9에서 평균 Validation Accuracy가 가장 높았다. k=1보다 여러 이웃의 majority voting을 이용했을 때 성능이 높았지만, k가 커질수록 항상 좋아지지는 않았다. L1의 최고 정확도는 L2보다 2.04%p, Cosine보다 0.56%p 높았다.

L1과 L2는 픽셀 차이를, Cosine은 벡터 방향을 비교하므로 이웃의 순서가 달라질 수 있다. 강의에서 설명한 viewpoint variation, illumination, background clutter는 픽셀 값을 바꾼다. 따라서 픽셀 거리가 가까워도 같은 클래스라는 보장은 없으며, 원시 픽셀 KNN의 성능에는 한계가 있다.

데이터: [CIFAR-10](https://cave.cs.toronto.edu/kriz/cifar.html), Alex Krizhevsky (2009).
