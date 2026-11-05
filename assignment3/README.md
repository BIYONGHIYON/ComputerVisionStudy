# Assignment

## Image

This binary flower image has small noise and gaps, so the effects are easy to see.

![Original binary image](0_binary.png)

## Methods

Code: [assignment3.py](assignment3.py). All methods use a 7×7 square structuring element.

- **Dilation:** Expands white regions.
- **Erosion:** Shrinks white regions.
- **Opening:** Removes small white noise, but may thin the petals.
- **Closing:** Fills small black gaps and thickens the petals.

## Results

Individual results: [Dilation](1_dilation.png) · [Erosion](2_erosion.png) · [Opening](3_opening.png) · [Closing](4_closing.png)

![Input and results](5_comparison.png)

## Run

Use Python 3.10 or later. From the repository root:

```bash
python -m pip install -r assignment3/requirements.txt
python assignment3/assignment3.py
```

The included `0_binary.png` is the input. The script saves the four result images and `5_comparison.png` in this folder, replacing the existing results. NumPy performs the morphological operations; Pillow loads, saves and arranges the images.
