# CIFAR-10 KNN Experiment Results / 실험 결과

## Experimental Setup / 실험 조건

We used stratified subsets of CIFAR-10: 5,000 training images and 1,000 test images, with seed 42. This is not a full-dataset experiment. Each RGB image was flattened into a 3,072-dimensional vector and its pixel values were divided by 255.

CIFAR-10에서 클래스 비율을 유지해 학습 5,000장·테스트 1,000장을 사용했다. 전체 데이터 실험은 아니다. RGB 이미지를 3,072차원 벡터로 표현하고 픽셀을 255로 나누었다. seed는 42이다.

KNN stores images and labels during training, then classifies a query using a majority vote among its k nearest neighbors. We compared k=1, 3, 5, 7, 9 and L1 (Manhattan), L2 (Euclidean) and cosine distances.

KNN은 train에서 데이터와 label을 저장하고, predict에서 가까운 k개의 이웃을 찾아 majority voting으로 분류했다. k=1, 3, 5, 7, 9와 L1(Manhattan), L2(Euclidean), Cosine을 비교했다.

## 5-fold Cross-validation / 5겹 교차검증

The training subset was divided into five folds. Each run used 4,000 images for training and 1,000 for validation. The table lists validation accuracy for each fold and the five-fold mean, in percent.

학습 데이터를 5등분하여 매번 4,000장으로 train, 1,000장으로 validation을 수행했다. 아래는 각 fold의 Validation Accuracy와 5개 fold의 평균이다. 단위는 %이다.

| Distance Metric | k | Fold 1 | Fold 2 | Fold 3 | Fold 4 | Fold 5 | Mean / 평균 |
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

**L1, k=9** achieved the highest mean validation accuracy and was selected. Its sample standard deviation across folds was 0.45 percentage points.

Validation Accuracy가 가장 높은 **L1, k=9**를 선택했다. 이 설정의 fold 간 표본 표준편차는 0.45%p이다.

## Test Results / 테스트 결과

The selected configuration stored all 5,000 training images and was evaluated on a separate set of 1,000 test images.

선택한 설정으로 학습 5,000장을 저장하고 별도 test set 1,000장을 평가했다.

| Metric / 지표 | Result / 결과 |
|---|---:|
| Accuracy | 30.00% |
| Precision (macro) | 37.20% |
| Recall (macro) | 30.00% |
| F1-score (macro) | 28.61% |

Precision, recall and F1 were macro-averaged over the 10 classes. Accuracy equals macro recall here because every class has the same number of test images.

Precision·Recall·F1은 10개 클래스별 지표를 평균했다. 각 클래스의 test 이미지 수가 같아서 Accuracy와 macro Recall이 같다.

## Comparison and Discussion / 비교 및 설명

For all three distance metrics, k=9 produced the highest mean validation accuracy among the tested k values. Voting over multiple neighbors improved on k=1, but accuracy did not increase monotonically with k. The best L1 validation accuracy exceeded the best L2 result by 2.04 percentage points and the best cosine result by 0.56 percentage points.

세 Distance Metric 모두 k=9에서 평균 Validation Accuracy가 가장 높았다. k=1보다 여러 이웃의 majority voting을 이용했을 때 성능이 높았지만, k가 커질수록 항상 좋아지지는 않았다. L1의 최고 정확도는 L2보다 2.04%p, Cosine보다 0.56%p 높았다.

L1 and L2 compare pixel differences, while cosine compares vector directions, so they may rank neighbors differently. Viewpoint variation, illumination and background clutter change pixel values. Small pixel distance therefore does not guarantee that two images belong to the same class, limiting KNN based on raw pixels.

L1과 L2는 픽셀 차이를, Cosine은 벡터 방향을 비교하므로 이웃의 순서가 달라질 수 있다. 강의에서 설명한 viewpoint variation, illumination, background clutter는 픽셀 값을 바꾼다. 따라서 픽셀 거리가 가까워도 같은 클래스라는 보장은 없으며, 원시 픽셀 KNN의 성능에는 한계가 있다.

## Per-class Results / 클래스별 결과

The following values come from [test_per_class.csv](details/test_per_class.csv). Each class contains 100 test images. Precision and recall can differ substantially even with equal class support because prediction counts differ.

다음 값은 [test_per_class.csv](details/test_per_class.csv)에서 가져왔습니다. 각 클래스의 테스트 표본은 100장입니다. 클래스별 표본 수가 같아도 해당 클래스로 예측한 수는 다르므로 Precision과 Recall은 크게 다를 수 있습니다.

| Class ID | Class / 클래스 | Precision (%) | Recall (%) | F1 (%) | Support / 표본 수 |
|---|---|---:|---:|---:|---:|
| 0 | airplane / 비행기 | 36.21 | 63.00 | 45.99 | 100 |
| 1 | automobile / 자동차 | 53.57 | 15.00 | 23.44 | 100 |
| 2 | bird / 새 | 17.60 | 41.00 | 24.62 | 100 |
| 3 | cat / 고양이 | 20.75 | 11.00 | 14.38 | 100 |
| 4 | deer / 사슴 | 20.88 | 38.00 | 26.95 | 100 |
| 5 | dog / 개 | 32.79 | 20.00 | 24.84 | 100 |
| 6 | frog / 개구리 | 32.91 | 26.00 | 29.05 | 100 |
| 7 | horse / 말 | 60.00 | 18.00 | 27.69 | 100 |
| 8 | ship / 배 | 39.55 | 53.00 | 45.30 | 100 |
| 9 | truck / 트럭 | 57.69 | 15.00 | 23.81 | 100 |

Airplane recall is 63%, but its precision is 36.21%: 174 images were predicted as airplanes and 63 were correct. Horse precision is 60%, but recall is 18%: only 30 images were predicted as horses and 18 were correct. A high precision alone therefore does not imply that most actual examples of that class are found.

비행기의 Recall은 63%이지만 Precision은 36.21%입니다. 비행기로 예측한 174장 중 63장이 정답이었습니다. 말의 Precision은 60%이지만 Recall은 18%입니다. 말로 예측한 30장 중 18장은 정답이지만 실제 말 100장 중 18장만 찾았습니다. 따라서 Precision만 높다고 해당 클래스의 실제 표본을 대부분 찾았다고 볼 수 없습니다.

## Confusion Matrix Reading / 혼동행렬 해석

Open [confusion_matrix.csv](details/confusion_matrix.csv) with rows as true labels and columns as predicted labels. The diagonal sums to 300 correct predictions; the remaining 700 predictions are errors. Class IDs match the table above.

[confusion_matrix.csv](details/confusion_matrix.csv)의 행은 실제 정답, 열은 예측 클래스입니다. 대각선 합은 정답 300장이고 나머지 700장은 오분류입니다. 클래스 ID는 위 표와 같습니다.

| True → predicted / 실제 → 예측 | Count / 표본 수 |
|---|---:|
| deer → bird / 사슴 → 새 | 35 |
| dog → bird / 개 → 새 | 29 |
| frog → bird / 개구리 → 새 | 29 |
| horse → bird / 말 → 새 | 29 |
| frog → deer / 개구리 → 사슴 | 26 |

These are the five largest off-diagonal entries. Bird was predicted 233 times, with 41 correct predictions, producing recall of 41% and precision of 17.60%. This documents a prediction imbalance in this run. The counts alone do not identify whether background, color or another image property caused it.

위 표는 대각선을 제외하고 가장 큰 다섯 항목입니다. 새로 예측한 표본은 233장이고 이 중 정답은 41장이어서 Recall은 41%, Precision은 17.60%입니다. 이 실행에서 특정 클래스로 예측이 몰리는 현상을 확인할 수 있습니다. 다만 이 수치만으로 배경, 색상 등 어떤 영상 특성이 원인인지 판단할 수는 없습니다.

## Scope of the Findings / 결과 해석 범위

The selected setting won among the 15 candidates on the saved folds. Fold standard deviation measures variation across those folds, not uncertainty across independent random seeds. The test accuracy is a single evaluation on the saved subset. No confidence interval, repeated-seed comparison or learned-feature baseline was evaluated here.

선택된 설정은 저장된 fold에서 15개 후보 중 가장 높은 평균 정확도를 얻었습니다. Fold 표준편차는 해당 fold 사이의 변동이며 독립적인 여러 seed에 대한 불확실성이 아닙니다. 테스트 정확도는 저장된 부분집합에서 한 번 평가한 값입니다. 이 과제에서는 신뢰구간, 여러 seed 반복 비교, 학습된 특징을 사용하는 기준 모델을 평가하지 않았습니다.

Dataset / 데이터: [CIFAR-10](https://cave.cs.toronto.edu/kriz/cifar.html), Alex Krizhevsky (2009).
