"""CIFAR-10 KNN 과제: 강의의 train / predict 흐름을 따라 구현.

학습 데이터를 저장하고, 가까운 k개 이웃의 다수결로 분류한다.
"""
import csv
import json
import pickle
from pathlib import Path
from time import perf_counter

import numpy as np

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "cifar-10-batches-py"
OUTPUT_DIR = ROOT / "results"
TRAIN_SIZE = 5000  # 0이면 학습 데이터 전체
TEST_SIZE = 1000   # 0이면 테스트 데이터 전체
K_VALUES = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
SEED = 42
METRICS = ["euclidean", "manhattan", "cosine"]


def load_batch(path):
    # 공식 CIFAR-10 배치 파일에서 이미지 배열과 정답을 읽는다.
    with path.open("rb") as stream:
        batch = pickle.load(stream, encoding="bytes")
    x = np.asarray(batch[b"data"])
    y = np.asarray(batch[b"labels"], dtype=np.int64)
    if x.shape != (10000, 3072) or y.shape != (10000,):
        raise ValueError(f"Unexpected CIFAR-10 batch shape: {path}")
    if x.dtype != np.uint8 or np.any((y < 0) | (y > 9)):
        raise ValueError(f"Invalid CIFAR-10 pixels or labels: {path}")
    return x, y


def stratified_sample(y, size, rng):
    """클래스 비율을 유지하면서 중복 없이 실험용 이미지를 고른다."""
    if size == 0 or size >= len(y):
        return np.arange(len(y))
    classes, counts = np.unique(y, return_counts=True)
    targets = size * counts / len(y)
    allocated = np.floor(targets).astype(int)
    order = np.argsort(-(targets - allocated), kind="stable")
    allocated[order[:size - allocated.sum()]] += 1
    indices = np.concatenate([
        rng.permutation(np.flatnonzero(y == label))[:count]
        for label, count in zip(classes, allocated)
    ])
    return rng.permutation(indices)


def stratified_folds(y, rng, n_splits=5):
    """클래스별 이미지를 5등분하여 각 fold의 클래스 비율을 맞춘다."""
    folds = [[] for _ in range(n_splits)]
    for label in np.unique(y):
        indices = rng.permutation(np.flatnonzero(y == label))
        if len(indices) < n_splits:
            raise ValueError("Each class needs at least 5 samples for 5-fold CV.")
        for fold, part in zip(folds, np.array_split(indices, n_splits)):
            fold.extend(part.tolist())
    return [np.array(sorted(fold), dtype=np.int64) for fold in folds]


class KNearestNeighbor:
    """강의의 NearestNeighbor를 k개 이웃의 다수결로 확장한 분류기."""

    def __init__(self, metric="manhattan"):
        if metric not in METRICS:
            raise ValueError("지원하지 않는 거리 함수입니다.")
        self.metric = metric

    def train(self, X, y):
        # KNN의 학습: 가중치를 구하지 않고 이미지와 정답을 기억한다.
        self.X_train = np.asarray(X, dtype=np.float32)
        self.y_train = np.asarray(y, dtype=np.int64)

    def compute_distances(self, image):
        """이미지 한 장과 모든 학습 이미지 사이의 거리를 구한다."""
        distances = np.zeros(len(self.X_train), dtype=np.float32)

        # 한 번에 1,024장씩 계산하여 전체 데이터 실행 시 메모리를 아낀다.
        # 각 묶음 안에서는 강의처럼 NumPy로 모든 픽셀 차이를 계산한다.
        for start in range(0, len(self.X_train), 1024):
            train_images = self.X_train[start:start + 1024]

            if self.metric == "manhattan":
                # L1 = 각 픽셀 차이의 절댓값을 모두 더한 값
                difference = train_images - image
                block_distances = np.sum(np.abs(difference), axis=1)

            elif self.metric == "euclidean":
                # L2 = 각 픽셀 차이를 제곱해서 더한 뒤 제곱근을 취한 값
                difference = train_images - image
                block_distances = np.sqrt(np.sum(difference ** 2, axis=1))

            else:
                # 추가 비교: cosine distance = 1 - 두 벡터의 코사인 유사도
                dot_product = np.sum(train_images * image, axis=1)
                train_norm = np.sqrt(np.sum(train_images ** 2, axis=1))
                image_norm = np.sqrt(np.sum(image ** 2))
                denominator = train_norm * image_norm
                similarity = np.divide(
                    dot_product, denominator,
                    out=np.zeros_like(dot_product), where=denominator != 0,
                )
                block_distances = np.clip(1 - similarity, 0, 2)
                # 영벡터끼리는 거리 0, 영벡터와 비영벡터 사이는 거리 1.
                block_distances[(train_norm == 0) & (image_norm == 0)] = 0

            distances[start:start + len(train_images)] = block_distances

        return distances

    def predict(self, X, k=1):
        """강의의 predict(X)에 이웃 수 k를 추가한 기본 사용법."""
        return self.predict_for_k_values(X, [k])[k]

    def predict_for_k_values(self, X, k_values):
        """같은 거리 계산을 여러 k 실험에 재사용한다."""
        if min(k_values) < 1 or max(k_values) > len(self.y_train):
            raise ValueError("k는 1 이상, 학습 이미지 수 이하여야 합니다.")
        predictions = {}
        for k in k_values:
            predictions[k] = np.zeros(len(X), dtype=np.int64)

        for i in range(len(X)):
            # 1. 새 이미지와 모든 학습 이미지 사이의 거리 계산
            distances = self.compute_distances(X[i])

            # 2. 거리가 작은 순서대로 학습 이미지의 인덱스 정렬
            sorted_indices = np.argsort(distances, kind="stable")

            for k in k_values:
                # 3. 가장 가까운 k개 이웃의 정답 가져오기
                nearest_indices = sorted_indices[:k]
                nearest_labels = self.y_train[nearest_indices]

                # 4. 클래스마다 표를 세고 가장 많은 표를 받은 클래스 선택
                votes = np.bincount(nearest_labels, minlength=10)
                predictions[k][i] = np.argmax(votes)

        return predictions


def evaluate(y_true, y_pred, n_classes=10):
    """혼동행렬에서 Accuracy와 클래스별 Precision, Recall, F1을 계산한다."""
    # 행: 실제 정답 / 열: 모델의 예측
    confusion_matrix = np.zeros((n_classes, n_classes), dtype=np.int64)
    for true_label, predicted_label in zip(y_true, y_pred):
        confusion_matrix[true_label, predicted_label] += 1

    per_class = []
    for label in range(n_classes):
        true_positive = int(confusion_matrix[label, label])
        predicted_count = int(confusion_matrix[:, label].sum())
        actual_count = int(confusion_matrix[label, :].sum())

        # Precision = TP / (TP + FP): 이 클래스로 예측한 것 중 맞은 비율
        precision = true_positive / predicted_count if predicted_count else 0.0
        # Recall = TP / (TP + FN): 실제 이 클래스인 것 중 맞힌 비율
        recall = true_positive / actual_count if actual_count else 0.0
        # F1 = Precision과 Recall의 조화평균
        if precision + recall > 0:
            f1 = 2 * precision * recall / (precision + recall)
        else:
            f1 = 0.0
        per_class.append({"class_id": label, "precision": precision,
                          "recall": recall, "f1": f1, "support": actual_count})

    scores = {
        "accuracy": float(np.mean(y_true == y_pred)),
        "precision_macro": float(np.mean([row["precision"] for row in per_class])),
        "recall_macro": float(np.mean([row["recall"] for row in per_class])),
        "f1_macro": float(np.mean([row["f1"] for row in per_class])),
    }
    return scores, confusion_matrix, per_class


def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)



def main():
    started = perf_counter()
    # 1. 학습 데이터를 읽고 클래스 비율을 유지해 실험용 표본을 고른다.
    batches = [load_batch(DATA_DIR / f"data_batch_{i}") for i in range(1, 6)]
    X = np.concatenate([batch[0] for batch in batches])
    y = np.concatenate([batch[1] for batch in batches])
    rng = np.random.default_rng(SEED)
    train_indices = stratified_sample(y, TRAIN_SIZE, rng)
    X, y = X[train_indices].astype(np.float32) / 255.0, y[train_indices]
    del batches

    # 2. 5-fold cross-validation: 4개 fold로 train, 1개 fold로 validation.
    folds = stratified_folds(y, rng)
    all_indices = np.arange(len(y))
    fold_results = []
    for metric in METRICS:
        for fold_number, validation in enumerate(folds, 1):
            train = np.setdiff1d(all_indices, validation)
            model = KNearestNeighbor(metric)
            model.train(X[train], y[train])
            predictions = model.predict_for_k_values(X[validation], K_VALUES)
            for k in K_VALUES:
                scores, _, _ = evaluate(y[validation], predictions[k])
                fold_results.append({"metric": metric, "k": k,
                                     "fold": fold_number, **scores})
            print(f"{metric}: fold {fold_number}/5 finished", flush=True)

    # 3. 각 설정의 검증 점수를 평균하고 Accuracy가 가장 높은 설정을 선택한다.
    summary = []
    for metric in METRICS:
        for k in K_VALUES:
            group = [row for row in fold_results if row["metric"] == metric and row["k"] == k]
            row = {"metric": metric, "k": k}
            for name in ["accuracy", "precision_macro", "recall_macro", "f1_macro"]:
                values = [item[name] for item in group]
                row[name + "_mean"] = float(np.mean(values))
                row[name + "_std"] = float(np.std(values, ddof=1))
            summary.append(row)
    # 동률이면 작은 k, 거리 이름 순으로 선택한다.
    summary.sort(key=lambda row: (-row["accuracy_mean"], row["k"], row["metric"]))
    best = summary[0]

    # 4. 선택한 설정으로 test set을 평가한다. test 점수로 설정을 고르지 않는다.
    X_test, y_test = load_batch(DATA_DIR / "test_batch")
    test_indices = stratified_sample(y_test, TEST_SIZE, np.random.default_rng(SEED + 1))
    X_test = X_test[test_indices].astype(np.float32) / 255.0
    y_test = y_test[test_indices]
    model = KNearestNeighbor(best["metric"])
    model.train(X, y)
    predicted = model.predict(X_test, k=best["k"])
    scores, confusion_matrix, per_class = evaluate(y_test, predicted)
    with (DATA_DIR / "batches.meta").open("rb") as stream:
        names = pickle.load(stream, encoding="bytes")[b"label_names"]
    for row, name in zip(per_class, names):
        row["class_name"] = name.decode("utf-8")

    # 5. 수치 결과만 저장한다. README와 보고서는 별도 문서로 관리한다.
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    details = OUTPUT_DIR / "details"
    details.mkdir(exist_ok=True)
    write_csv(OUTPUT_DIR / "cv_summary.csv", summary)
    write_csv(details / "cv_folds.csv", fold_results)
    write_csv(details / "test_per_class.csv", per_class)
    np.savetxt(details / "confusion_matrix.csv", confusion_matrix, fmt="%d", delimiter=",")
    write_csv(details / "test_predictions.csv", [
        {"original_test_index": index, "true": truth, "predicted": prediction}
        for index, truth, prediction in zip(test_indices, y_test, predicted)
    ])
    np.savez(
        details / "split_indices.npz",
        train_indices=train_indices,
        test_indices=test_indices,
        **{f"cv_validation_{i}": fold for i, fold in enumerate(folds, 1)},
    )
    result = {"seed": SEED, "train_samples": len(y), "test_samples": len(y_test),
              "ks": K_VALUES, "metrics": METRICS,
              "preprocessing": "raw RGB flattened to 3072 features, float32 / 255",
              "selection": "highest mean CV accuracy; ties: smaller k, then metric name",
              "best_metric": best["metric"], "best_k": best["k"], "test_scores": scores,
              "elapsed_seconds": perf_counter() - started, "numpy_version": np.__version__}
    (OUTPUT_DIR / "result.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"Best: {best['metric']}, k={best['k']}")
    for name, value in scores.items():
        print(f"{name}: {value:.2%}")


if __name__ == "__main__":
    main()
