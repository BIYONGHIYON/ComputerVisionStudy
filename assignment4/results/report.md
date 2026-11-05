# CIFAR-10 KNN Results / 실험 결과

## Setup / 실험 조건

- **Data / 데이터:** 5,000 training and 1,000 test images, sampled with balanced class proportions. / 클래스 비율을 유지한 학습 5,000장·테스트 1,000장.
- **Input / 입력:** Raw RGB pixels flattened to 3,072 features and divided by 255. / 원시 RGB 픽셀을 3,072차원으로 펼친 뒤 255로 나눔.
- **Seed:** 42.
- **Comparison / 비교:** L1, L2, cosine; k=1, 3, 5, 7, 9.
- **Validation / 검증:** Five folds, each with 4,000 training and 1,000 validation images. / 5-fold, 매번 학습 4,000장·검증 1,000장.

## Cross-validation Results / 교차검증 결과

Mean validation accuracy across five folds (%). Detailed fold results: [cv_folds.csv](details/cv_folds.csv).

다섯 fold의 평균 검증 정확도(%)입니다. Fold별 결과: [cv_folds.csv](details/cv_folds.csv).

| k | L1 (Manhattan) | L2 (Euclidean) | Cosine |
|---:|---:|---:|---:|
| 1 | 26.90 | 25.48 | 27.74 |
| 3 | 26.30 | 23.84 | 25.76 |
| 5 | 28.04 | 26.08 | 26.84 |
| 7 | 27.88 | 25.88 | 27.08 |
| 9 | 28.54 | 26.50 | 27.98 |

**L1, k=9** achieved the highest mean accuracy of **28.54%** and was selected. All three metrics performed best at k=9 among the tested values, but accuracy did not improve at every increase in k.

**L1, k=9**가 평균 정확도 **28.54%**로 가장 높아 선택했습니다. 세 거리 함수 모두 후보 중 k=9에서 가장 높았지만, k가 커질 때마다 정확도가 좋아지지는 않았습니다.

![Cross-validation accuracy / 교차검증 정확도](cv_accuracy.png)

## Test Results / 테스트 결과

The selected setting used all 5,000 training images and correctly classified 300 of 1,000 separate test images.

선택한 설정에 학습 5,000장을 모두 사용했으며, 별도 테스트 이미지 1,000장 중 300장을 맞혔습니다.

| Metric / 지표 | Result / 결과 |
|---|---:|
| Accuracy | 30.00% |
| Precision (macro) | 37.20% |
| Recall (macro) | 30.00% |
| F1-score (macro) | 28.61% |

Macro metrics average the scores of the ten classes. This is a single-seed subset experiment; the result does not establish that L1 or k=9 is always best. Raw pixel similarity can also be affected by viewpoint, lighting and background.

Macro 지표는 열 개 클래스의 점수를 평균한 값입니다. 단일 seed의 부분집합 실험이므로 L1이나 k=9가 항상 최선이라는 의미는 아닙니다. 원시 픽셀의 유사도는 시점·조명·배경의 영향도 받습니다.

Detailed records / 상세 기록: [settings and scores / 설정·점수](result.json) · [CV summary / 검증 요약](cv_summary.csv) · [per-class scores / 클래스별 지표](details/test_per_class.csv) · [confusion matrix / 혼동행렬](details/confusion_matrix.csv).
