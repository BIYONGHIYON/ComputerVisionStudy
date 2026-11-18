"""Inspect a random linear classifier on five CIFAR-10 examples."""

import argparse
import csv
import pickle
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
SEED = 42
WEIGHT_STD = 0.01
EXAMPLE_COUNT = 5
MARGIN = 1.0


def load_batch_file(path):
    with path.open("rb") as file:
        return pickle.load(file, encoding="bytes")


def svm_hinge_loss(scores, label):
    # 정답 클래스를 제외한 9개 클래스의 양수 마진만 더한다.
    # Sum the positive margins for the nine other classes.
    margins = np.maximum(0.0, scores - scores[label] + MARGIN)
    margins[label] = 0.0
    return margins.sum()


def softmax(scores):
    # 최댓값을 빼고 지수화한 뒤, 합이 1이 되도록 나눈다.
    # Subtract the maximum, exponentiate, then normalize to sum to one.
    exp_scores = np.exp(scores - scores.max())
    return exp_scores / exp_scores.sum()


def to_rgb(vector):
    # R·G·B 채널 순서로 저장된 벡터를 (32, 32, 3) 이미지로 바꾼다.
    # Convert the channel-first RGB vector to a (32, 32, 3) image.
    return vector.reshape(3, 32, 32).transpose(1, 2, 0)


def save_image_grid(images, captions, path):
    columns = 5
    tile, cell_width, cell_height = 112, 144, 157
    rows = (len(images) + columns - 1) // columns
    canvas = Image.new("RGB", (columns * cell_width, rows * cell_height), "white")
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.load_default(size=13)

    for i, (image, caption) in enumerate(zip(images, captions)):
        row, col = divmod(i, columns)
        x, y = col * cell_width, row * cell_height
        preview = Image.fromarray(image).resize((tile, tile), Image.Resampling.NEAREST)
        canvas.paste(preview, (x + (cell_width - tile) // 2, y + 6))
        for line_number, line in enumerate(caption.splitlines()):
            draw.text((x + cell_width // 2, y + 124 + 16 * line_number), line,
                      font=font, fill="#20262e", anchor="mt")
    canvas.save(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("data_dir", type=Path, nargs="?", default=ROOT / "cifar-10-batches-py",
                        help="Official CIFAR-10 Python folder with test_batch and batches.meta")
    args = parser.parse_args()
    for name in ("test_batch", "batches.meta"):
        if not (args.data_dir / name).is_file():
            parser.error(f"Missing {args.data_dir / name}. See README.md for setup.")

    batch = load_batch_file(args.data_dir / "test_batch")
    metadata = load_batch_file(args.data_dir / "batches.meta")
    class_names = [name.decode("ascii") for name in metadata[b"label_names"]]
    # 테스트 배치에서 이미지와 정답을 앞에서부터 5개씩 가져온다.
    # Take the first five images and labels from the test batch.
    images = batch[b"data"][:EXAMPLE_COUNT]
    labels = batch[b"labels"][:EXAMPLE_COUNT]

    # 시드를 고정하고 클래스별 가중치와 편향을 초기화한다.
    # Fix the seed and initialize the class weights and biases.
    rng = np.random.default_rng(SEED)
    W = rng.normal(0.0, WEIGHT_STD, size=(10, 3072))
    b = np.zeros(10)

    output = ROOT / "results"
    output.mkdir(exist_ok=True)
    losses = []
    captions = []
    with (output / "scores_and_probabilities.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, lineterminator="\n")
        writer.writerow(["test_index", "true_class", "predicted_class", "class",
                         "score", "probability", "probability_sum", "svm_hinge_loss"])
        for index, (pixels, label) in enumerate(zip(images, labels)):
            x = pixels.astype(np.float64) / 255.0
            # 이미지 한 장마다 10개 클래스 점수를 계산하고 가장 높은 클래스를 고른다.
            # Compute ten class scores per image and pick the highest-scoring class.
            scores = W @ x + b
            prediction = int(np.argmax(scores))
            loss = svm_hinge_loss(scores, label)
            probabilities = softmax(scores)
            # 확률 합이 1이고 점수와 확률의 예측 클래스가 같은지 확인한다.
            # Check that probabilities sum to one and give the same prediction as the scores.
            total = probabilities.sum()
            np.testing.assert_allclose(total, 1.0, rtol=0.0, atol=1e-12)
            assert np.argmax(probabilities) == prediction

            truth, predicted = class_names[label], class_names[prediction]
            outcome = "Correct" if prediction == label else "Incorrect"
            captions.append(f"#{index} {truth} -> {predicted}\n{outcome}")
            losses.append(loss)
            print(f"\n#{index} {truth} -> {predicted} ({outcome})")
            for name, score, probability in zip(class_names, scores, probabilities):
                print(f"  {name:10s}  score {score:+.6f}  probability {probability:.6f}")
                writer.writerow([index, truth, predicted, name, f"{score:.12f}",
                                 f"{probability:.12f}", f"{total:.12f}", f"{loss:.12f}"])
            print(f"  Probability sum {total:.12f} | SVM hinge loss {loss:.6f}")

    # 10개 가중치 그림에 같은 색 범위를 쓰고, 0은 중간 회색으로 표시한다.
    # Use the same color scale for all ten weight images, with zero shown in midgray.
    limit = np.abs(W).max()
    weight_pixels = np.rint(127.5 * (W / limit + 1.0)).astype(np.uint8)
    save_image_grid([to_rgb(x) for x in images], captions, output / "examples.png")
    save_image_grid([to_rgb(w) for w in weight_pixels], class_names, output / "weights.png")
    print(f"\nMean SVM hinge loss {np.mean(losses):.6f}")


if __name__ == "__main__":
    main()
