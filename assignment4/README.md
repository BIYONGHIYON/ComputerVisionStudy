# CIFAR-10 KNN

## Data Preparation and Execution / 데이터 준비 및 실행

Use Python 3.10 or later. Run the commands from the repository root.

Python 3.10 이상을 사용합니다. 아래 명령은 저장소 루트에서 실행합니다.

```bash
python -m pip install -r assignment4/requirements.txt
```

Download and extract **CIFAR-10 python version** from the [official CIFAR-10 page](https://www.cs.toronto.edu/~kriz/cifar.html). The original dataset is not included in this repository.

[CIFAR-10 공식 페이지](https://www.cs.toronto.edu/~kriz/cifar.html)의 **CIFAR-10 python version**을 다운로드해 압축을 풉니다. 원본 데이터는 저장소에 포함하지 않았습니다.

On macOS/Linux, download and extract it with:

macOS/Linux에서는 다음 명령으로 준비할 수 있습니다.

```bash
curl -fL https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz -o assignment4/cifar-10-python.tar.gz
tar -xzf assignment4/cifar-10-python.tar.gz -C assignment4
```

The following files must be present:

다음 파일들이 있어야 합니다.

```text
assignment4/cifar-10-batches-py/
├── batches.meta
├── data_batch_1
├── data_batch_2
├── data_batch_3
├── data_batch_4
├── data_batch_5
└── test_batch
```

```bash
python assignment4/assignment4.py
```

Running the script overwrites the numerical result files in `results/`.

실행하면 `results/`의 수치 결과 파일을 덮어씁니다.

Configure `TRAIN_SIZE`, `TEST_SIZE`, `K_VALUES` and `METRICS` at the top of `assignment4.py`. The defaults use 5,000 training and 1,000 test images. Set both `TRAIN_SIZE` and `TEST_SIZE` to 0 to use the full dataset.

실험 설정은 `assignment4.py` 상단의 `TRAIN_SIZE`, `TEST_SIZE`, `K_VALUES`, `METRICS`에서 변경합니다. 기본값은 학습 5,000장·테스트 1,000장입니다. `TRAIN_SIZE`와 `TEST_SIZE`를 0으로 바꾸면 전체 데이터를 사용합니다.

## Implementation / 구현

- **train**: Stores training images and labels. / 학습 이미지와 label을 저장합니다.
- **Distance metric / 거리 함수**: Compares L1 (Manhattan), L2 (Euclidean) and cosine. / L1(Manhattan), L2(Euclidean), Cosine을 비교합니다.
- **predict**: Selects the k nearest neighbors and predicts a label by majority vote. / 거리가 가까운 k개의 이웃을 선택하고 majority voting으로 label을 예측합니다.
- **5-fold cross-validation / 5겹 교차검증**: Trains on four folds and validates on the remaining fold, rotating through all five folds. Selects k and the distance metric by mean validation accuracy. / 학습 데이터를 5등분하고, 4개 fold로 train·1개 fold로 validation을 수행합니다. 5번의 평균 Accuracy로 k와 Distance Metric을 선택합니다.
- **test**: Evaluates only the selected setting on a separate test set. / 선택한 설정만 별도 test set에서 평가합니다.

Precision, recall and F1 are calculated per class and macro-averaged. A voting tie is resolved by choosing the smaller label ID.

Precision·Recall·F1은 클래스별로 계산한 뒤 macro 평균합니다. 투표 동률이면 작은 label 번호를 선택합니다.

## Data Representation and Sampling / 데이터 표현과 표본 선택

Each 32×32 RGB image is represented by 3,072 features in the official batch's channel-first flattened order. Pixels are converted to `float32` and divided by 255, giving values in [0, 1]. There is no learned feature extractor, image augmentation or per-image standardization. Uniform scaling does not change neighbor rankings for L1 or L2 and does not change cosine distance for nonzero vectors.

32×32 RGB 이미지를 공식 배치의 채널 우선 평탄화 순서에 따라 3,072개 특징으로 표현합니다. 픽셀은 `float32`로 바꾸고 255로 나누어 [0, 1] 범위로 변환합니다. 학습된 특징 추출기, 데이터 증강, 이미지별 표준화는 사용하지 않습니다. 모든 픽셀에 동일한 배율을 적용하므로 L1·L2의 이웃 순위는 바뀌지 않으며, 영벡터가 아닌 벡터의 Cosine 거리도 동일합니다.

The default stratified sample contains 500 training and 100 test images per class. Training sampling and fold construction use one generator initialized with `SEED=42`; test sampling uses a separate generator initialized with `SEED+1=43`. All distance metrics use the same five training folds.

기본 층화 표본은 클래스당 학습 500장, 테스트 100장입니다. 학습 표본 선택과 fold 구성은 `SEED=42`로 초기화한 하나의 난수 생성기를 순서대로 사용하며, 테스트 표본은 `SEED+1=43`인 별도 생성기로 선택합니다. 모든 거리 함수에 같은 다섯 학습 fold를 적용합니다.

## Distance and Voting / 거리 계산과 다수결

For feature vectors $x$ and $z$, the distance functions are:

특징 벡터 $x$, $z$에 사용하는 거리 함수는 다음과 같습니다.

$$
d_{L1}(x,z)=\sum_j|x_j-z_j|,\qquad d_{L2}(x,z)=\sqrt{\sum_j(x_j-z_j)^2}
$$

$$
d_{cos}(x,z)=1-\frac{x\cdot z}{\|x\|_2\|z\|_2}
$$

`compute_distances()` processes up to 1,024 training images at a time to limit temporary array sizes. For each query, `predict_for_k_values()` computes distances once, stably sorts all training indices, and reuses that order for every requested k. `np.bincount()` counts the neighbor labels and `np.argmax()` selects the winning class. Equal vote counts select the smallest class ID; equal distances retain the order of training samples. For cosine distance, two zero vectors have distance 0 and a zero/nonzero pair has distance 1.

`compute_distances()`는 임시 배열 크기를 줄이기 위해 학습 이미지를 최대 1,024장씩 처리합니다. `predict_for_k_values()`는 질의 이미지마다 거리를 한 번 계산하고 학습 인덱스를 안정 정렬한 뒤, 같은 순서를 모든 k에 재사용합니다. `np.bincount()`로 이웃의 클래스별 표를 세고 `np.argmax()`로 예측합니다. 투표 동률은 가장 작은 클래스 ID로 결정하고, 거리 동률은 학습 표본 순서를 유지합니다. Cosine 거리에서 영벡터끼리는 0, 영벡터와 비영벡터 사이는 1로 처리합니다.

## Validation and Final Test / 검증과 최종 테스트

1. Split the 5,000 training samples into five stratified folds. / 학습 표본 5,000장을 다섯 개의 층화 fold로 나눕니다.
2. For each distance metric, rotate the validation fold: train on 4,000 samples and predict the remaining 1,000 for every k. / 거리 함수별로 검증 fold를 교체하며 4,000장을 저장하고 나머지 1,000장을 각 k로 예측합니다.
3. Average the five validation accuracies for each of 15 combinations (3 metrics × 5 k values). The detailed CSV contains 75 fold-level records. / 15개 조합(거리 3개 × k 5개)의 검증 정확도를 각각 다섯 번 평균합니다. 상세 CSV에는 fold별 결과 75개가 기록됩니다.
4. Select the highest mean accuracy. Ties prefer smaller k, then the metric name in lexical order. / 평균 정확도가 가장 높은 조합을 선택합니다. 동률이면 작은 k, 그다음 거리 함수 이름의 사전순으로 결정합니다.
5. Store all 5,000 training samples using the selected setting and evaluate the separate 1,000-image test subset once. Test scores do not select the setting. / 선택된 설정으로 학습 표본 5,000장을 모두 저장하고 별도 테스트 표본 1,000장을 한 번 평가합니다. 테스트 점수는 설정 선택에 사용하지 않습니다.

## Evaluation Metrics / 평가 지표

For each class, TP counts correct predictions of that class, FP counts other classes predicted as it, and FN counts its samples predicted as another class.

클래스별 TP는 해당 클래스를 맞힌 수, FP는 다른 클래스를 해당 클래스로 예측한 수, FN은 해당 클래스를 다른 클래스로 예측한 수입니다.

$$
\mathrm{Precision}=\frac{TP}{TP+FP},\quad \mathrm{Recall}=\frac{TP}{TP+FN},\quad F1=\frac{2PR}{P+R}
$$

Accuracy is the fraction of all test samples classified correctly. Macro metrics average the ten class-level scores with equal weight; macro F1 is the mean of per-class F1 values, not the F1 calculated from macro precision and recall. The code assigns 0 when a metric's denominator is 0. In `confusion_matrix.csv`, rows are true classes and columns are predicted classes, in class ID order 0–9.

Accuracy는 전체 테스트 표본 중 정답의 비율입니다. Macro 지표는 열 개 클래스의 점수를 같은 가중치로 평균합니다. Macro F1은 클래스별 F1의 평균이며, macro Precision과 Recall로 다시 계산한 F1이 아닙니다. 코드에서는 분모가 0인 지표를 0으로 처리합니다. `confusion_matrix.csv`의 행은 실제 클래스, 열은 예측 클래스이며 클래스 ID 0–9 순서입니다.

## Computational Cost and Limitations / 계산 비용과 한계

KNN stores training data rather than optimizing weights. With N training samples and D features, distance evaluation costs O(ND) per query; this implementation also sorts all N distances in O(N log N). Chunking reduces temporary memory, but every query still compares against all training samples. Full-dataset execution can therefore take substantially longer than the saved subset experiment.

KNN은 가중치를 최적화하는 대신 학습 데이터를 저장합니다. 학습 표본 수가 N, 특징 수가 D일 때 질의당 거리 계산 비용은 O(ND)이며, 이 구현은 전체 거리 정렬에 O(N log N)을 추가로 사용합니다. 묶음 처리는 임시 메모리를 줄이지만 질의마다 모든 학습 표본을 비교하는 점은 같습니다. 전체 데이터 실행은 저장된 부분집합 실험보다 훨씬 오래 걸릴 수 있습니다.

The saved comparison uses one seed and raw pixels. It does not establish that L1 or k=9 is universally best, or that larger k always helps. Different sample draws, representations or candidate k values may change the selected setting.

저장된 비교는 원시 픽셀과 단일 seed를 사용했습니다. L1이나 k=9가 항상 최선이거나 k를 늘릴수록 항상 좋아진다는 결론은 아닙니다. 표본 선택, 특징 표현, 후보 k가 달라지면 선택되는 설정도 달라질 수 있습니다.

## Result Files / 결과 파일

- `results/report.md`: Manually written result summary / 직접 작성한 결과 요약
- `results/cv_summary.csv`: Cross-validation results for each setting / 설정별 cross-validation 결과
- `results/result.json`: Experiment settings and test results / 실험 설정과 test 결과
- `results/details/`: Per-fold and per-class metrics, confusion matrix and detailed records / fold별 지표, 클래스별 지표, confusion matrix 등 상세 기록

The code saves numerical results only. Markdown documents are maintained manually and must be updated if experiment settings change.

코드는 수치 결과만 저장합니다. Markdown 문서는 자동 생성하지 않으므로 실험 조건을 바꾸면 직접 수정해야 합니다.

## Saved Results / 저장된 결과

With 5,000 training images, 1,000 test images and seed 42, L1 (Manhattan), k=9 was selected. Mean cross-validation accuracy was 28.54%, and test accuracy was 30.00%. These are subset results, not results on the full CIFAR-10 dataset.

학습 5,000장·테스트 1,000장, seed 42에서 L1 (Manhattan), k=9가 선택됐습니다. 평균 교차검증 정확도는 28.54%, 테스트 정확도는 30.00%입니다. 전체 CIFAR-10 실험 결과가 아닙니다.

![Cross-validation accuracy](results/cv_accuracy.png)

See the [result report](results/report.md) for per-fold accuracy and test metrics. `results/knn_2d.png` is a synthetic 2D illustration of KNN, not a visualization of CIFAR-10 test results.

[결과 보고서](results/report.md)에서 fold별 정확도와 테스트 지표를 확인할 수 있습니다. `results/knn_2d.png`는 KNN 원리를 설명하는 2차원 예시이며, CIFAR-10의 테스트 결과를 나타내는 그림은 아닙니다.

`assignment4.py` saves numerical results. Plot images, `details/test_predictions.csv`, `details/split_indices.npz` and the additional metadata in the result JSON are retained experiment artifacts and are not regenerated by running the current script alone.

`assignment4.py`는 수치 결과를 저장합니다. 그래프 이미지, `details/test_predictions.csv`, `details/split_indices.npz`와 결과 JSON의 추가 메타데이터는 기존 실험에서 보관한 자료로, 현재 스크립트 실행만으로 재생성되지 않습니다.
