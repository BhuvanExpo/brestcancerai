"""
Synthetic Clinical Sample Scan Generator
=========================================
Generates realistic labeled breast imaging scans (Benign & Malignant) for
instantaneous out-of-the-box testing and interactive demonstration.

Simulated Morphologies:
  1. Benign: Fibroadenoma (well-circumscribed, oval hypoechoic lesion)
  2. Benign: Simple Cyst (anechoic fluid with posterior acoustic enhancement)
  3. Benign: Normal Parenchyma (fibroglandular tissue bands)
  4. Malignant: Invasive Ductal Carcinoma (spiculated irregular mass with acoustic shadow)
  5. Malignant: Lobulated Tumor (taller-than-wide microlobulated mass)
"""

import os
from typing import List, Tuple
import numpy as np
from PIL import Image, ImageDraw, ImageFilter


def _generate_tissue_background(
    seed: int,
    size: Tuple[int, int] = (400, 400),
    loc: float = 120.0,
    scale: float = 30.0,
    blur_radius: float = 1.6
) -> Image.Image:
    """Creates a base tissue texture with simulated ultrasound speckle noise."""
    np.random.seed(seed)
    raw = np.random.normal(loc=loc, scale=scale, size=size).clip(20, 220).astype(np.uint8)
    return Image.fromarray(raw).filter(ImageFilter.GaussianBlur(radius=blur_radius))


def _finalize_scan(img: Image.Image, noise_sigma: float = 10.0) -> Image.Image:
    """Adds fine-grain acoustic speckle noise and converts to RGB."""
    size = img.size
    arr = np.array(img, dtype=np.int16)
    noise = np.random.normal(0, noise_sigma, size=(size[1], size[0]))
    final_arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(final_arr).convert("RGB")


def create_fibroadenoma_scan(size: Tuple[int, int] = (400, 400)) -> Image.Image:
    """Simulates a benign fibroadenoma: smooth, oval, circumscribed lesion."""
    img = _generate_tissue_background(seed=42, size=size, loc=115, scale=30)
    draw = ImageDraw.Draw(img)
    draw.ellipse([120, 160, 280, 240], fill=45)
    img = img.filter(ImageFilter.GaussianBlur(radius=2.0))
    return _finalize_scan(img, noise_sigma=10.0)


def create_cyst_scan(size: Tuple[int, int] = (400, 400)) -> Image.Image:
    """Simulates a benign simple cyst: round fluid center + posterior acoustic enhancement."""
    img = _generate_tissue_background(seed=43, size=size, loc=120, scale=32)
    draw = ImageDraw.Draw(img)
    # Anechoic fluid collection
    draw.ellipse([140, 140, 260, 260], fill=25)
    # Posterior acoustic enhancement (bright beam amplification behind fluid)
    draw.rectangle([145, 265, 255, 340], fill=165)
    img = img.filter(ImageFilter.GaussianBlur(radius=2.2))
    return _finalize_scan(img, noise_sigma=8.0)


def create_normal_parenchyma_scan(size: Tuple[int, int] = (400, 400)) -> Image.Image:
    """Simulates normal fibroglandular breast parenchyma bands."""
    img = _generate_tissue_background(seed=44, size=size, loc=130, scale=28, blur_radius=2.0)
    draw = ImageDraw.Draw(img)
    draw.line([(50, 100), (350, 110)], fill=170, width=12)
    draw.line([(40, 180), (360, 195)], fill=175, width=15)
    draw.line([(50, 280), (350, 270)], fill=165, width=10)
    img = img.filter(ImageFilter.GaussianBlur(radius=3.0))
    return _finalize_scan(img, noise_sigma=9.0)


def create_invasive_ductal_scan(size: Tuple[int, int] = (400, 400)) -> Image.Image:
    """Simulates invasive ductal carcinoma: angular spiculated mass + acoustic shadowing."""
    img = _generate_tissue_background(seed=101, size=size, loc=125, scale=38)
    draw = ImageDraw.Draw(img)
    spiculated_poly = [
        (190, 110), (230, 125), (260, 160), (245, 205),
        (265, 245), (235, 280), (195, 290), (165, 265),
        (145, 230), (160, 180), (140, 145), (175, 125)
    ]
    draw.polygon(spiculated_poly, fill=30)
    # Acoustic shadow / beam attenuation directly beneath the dense malignant mass
    draw.polygon([(160, 285), (245, 285), (260, 390), (145, 390)], fill=35)
    img = img.filter(ImageFilter.GaussianBlur(radius=2.5))
    return _finalize_scan(img, noise_sigma=12.0)


def create_lobulated_tumor_scan(size: Tuple[int, int] = (400, 400)) -> Image.Image:
    """Simulates a microlobulated, taller-than-wide malignant neoplasm."""
    img = _generate_tissue_background(seed=102, size=size, loc=118, scale=35)
    draw = ImageDraw.Draw(img)
    # Taller-than-wide primary lesion with satellite microlobulations
    draw.ellipse([155, 110, 245, 275], fill=28)
    draw.ellipse([140, 170, 180, 230], fill=32)
    draw.ellipse([220, 150, 260, 210], fill=30)
    img = img.filter(ImageFilter.GaussianBlur(radius=2.0))
    return _finalize_scan(img, noise_sigma=10.0)


def generate_synthetic_samples(output_dir: str = "sample_scans") -> List[str]:
    """
    Generates and saves all labeled synthetic breast scans to disk.

    Args:
        output_dir: Directory where sample scans will be saved.

    Returns:
        List of generated file paths.
    """
    os.makedirs(output_dir, exist_ok=True)

    scans = {
        "benign_scan_01_fibroadenoma.png": create_fibroadenoma_scan(),
        "benign_scan_02_cyst.png": create_cyst_scan(),
        "benign_scan_03_normal_parenchyma.png": create_normal_parenchyma_scan(),
        "malignant_scan_01_invasive_ductal.png": create_invasive_ductal_scan(),
        "malignant_scan_02_lobulated.png": create_lobulated_tumor_scan(),
    }

    # Maintain backwards-compatibility filenames
    scans["benign_sample.png"] = scans["benign_scan_01_fibroadenoma.png"]
    scans["malignant_sample.png"] = scans["malignant_scan_01_invasive_ductal.png"]

    saved_paths = []
    print(f"[SampleGenerator] Generating sample scans in '{output_dir}/'...")
    for filename, img in scans.items():
        dest = os.path.join(output_dir, filename)
        img.save(dest)
        saved_paths.append(dest)
        print(f"  ✓ Saved: {dest}")

    return saved_paths


if __name__ == "__main__":
    generate_synthetic_samples()
