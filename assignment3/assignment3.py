from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

########################################################

# path
folder = Path(__file__).resolve().parent
input_path = folder / "0_binary.png"
dilation_path = folder / "1_dilation.png"
erosion_path = folder / "2_erosion.png"
opening_path = folder / "3_opening.png"
closing_path = folder / "4_closing.png"
comparison_path = folder / "5_comparison.png"

########################################################


def dilation(image, kernel):
    height, width = image.shape
    pad_y = kernel.shape[0] // 2
    pad_x = kernel.shape[1] // 2

    # zero padding
    padded = np.pad(image, ((pad_y, pad_y), (pad_x, pad_x)))
    result = np.zeros_like(image)

    for y, x in np.argwhere(kernel):
        # maximum pixel value
        result = np.maximum(result, padded[y : y + height, x : x + width])

    return result


def erosion(image, kernel):
    height, width = image.shape
    pad_y = kernel.shape[0] // 2
    pad_x = kernel.shape[1] // 2

    # zero padding
    padded = np.pad(image, ((pad_y, pad_y), (pad_x, pad_x)))
    result = np.full_like(image, 255)

    for y, x in np.argwhere(kernel):
        # minimum pixel value
        result = np.minimum(result, padded[y : y + height, x : x + width])

    return result


def morphology_results(image, kernel):
    pad_y = kernel.shape[0] // 2
    pad_x = kernel.shape[1] // 2
    padded = np.pad(
        image,
        ((pad_y, pad_y), (pad_x, pad_x)),
        constant_values=0,
    )

    dilation_padded = dilation(padded, kernel)
    erosion_padded = erosion(padded, kernel)

    # opening: erosion 후 dilation
    opening_padded = dilation(erosion_padded, kernel)

    # closing: dilation 후 erosion
    closing_padded = erosion(dilation_padded, kernel)

    return (
        dilation_padded[pad_y:-pad_y, pad_x:-pad_x],
        erosion_padded[pad_y:-pad_y, pad_x:-pad_x],
        opening_padded[pad_y:-pad_y, pad_x:-pad_x],
        closing_padded[pad_y:-pad_y, pad_x:-pad_x],
    )


# 잎 전체에 모든 방향으로 같은 기준을 적용하도록 7x7 정사각형 SE 사용
structuring_element = np.ones((7, 7), dtype=np.uint8)

# 검은 배경을 유지하며 입력을 0과 255의 이진 영상으로 변환
source = Image.open(input_path).convert("RGBA")
black_background = Image.new("RGBA", source.size, (0, 0, 0, 255))
binary_image = np.asarray(
    Image.alpha_composite(black_background, source).convert("L")
)
binary_image = np.where(binary_image >= 128, 255, 0).astype(np.uint8)

# 작은 흰 잡음과 잎 안의 검은 틈이 보여 형태학적 변화를 비교하기 적합한 이진 영상
(
    dilated,
    eroded,
    opening,
    closing,
) = morphology_results(binary_image, structuring_element)

# save
Image.fromarray(dilated).save(dilation_path)
Image.fromarray(eroded).save(erosion_path)
Image.fromarray(opening).save(opening_path)
Image.fromarray(closing).save(closing_path)

########################################################

# 처리 단계 비교 이미지
images = [
    binary_image,
    dilated,
    eroded,
    opening,
    closing,
]

titles = [
    "0. Input",
    "1. Dilation 7x7",
    "2. Erosion 7x7",
    "3. Opening 7x7",
    "4. Closing 7x7",
]

panel_width = 320
panel_height = 220
cell_width = 340
cell_height = 258
sheet = Image.new("RGB", (cell_width * 3 + 20, cell_height * 2 + 20), "white")
draw = ImageDraw.Draw(sheet)
font = ImageFont.load_default(size=17)

for index, (image, title) in enumerate(zip(images, titles)):
    column = index % 3
    row = index // 3
    x = 10 + column * cell_width
    y = 10 + row * cell_height
    draw.text((x, y), title, fill="black", font=font)
    preview = Image.fromarray(image).convert("RGB").resize(
        (panel_width, panel_height), Image.Resampling.LANCZOS
    )
    sheet.paste(preview, (x, y + 26))

sheet.save(comparison_path)

print("All four morphological results and the comparison were saved.")
