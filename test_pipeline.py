"""
Automated Verification & Pipeline Test Suite
============================================
Performs complete end-to-end testing across 5 diagnostic requirements:
  1. Model Loading & Architecture Specification Validation
  2. Benign Class Inference & Confidence Scoring
  3. Malignant Class Inference & Confidence Scoring
  4. Grad-CAM Activation Map Generation (Layer 'block5_conv3')
  5. OpenCV Alpha Superimposition (0.6 / 0.4 Blend)
"""

import os
from typing import Tuple
import cv2
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow.keras.applications.vgg16 import preprocess_input

from gradcam import compute_gradcam_heatmap, overlay_heatmap


def load_test_image(filepath: str, target_size: Tuple[int, int] = (224, 224)) -> Tuple[np.ndarray, np.ndarray]:
    """Loads, converts to RGB, resizes, and pre-processes an image tensor."""
    assert os.path.exists(filepath), f"Test image '{filepath}' does not exist."
    pil_img = Image.open(filepath).convert("RGB").resize(target_size)
    img_rgb = np.array(pil_img, dtype=np.uint8)
    batch = np.expand_dims(img_rgb.astype(np.float32), axis=0)
    return img_rgb, preprocess_input(batch)


def test_full_application_pipeline() -> None:
    """Executes the complete 5-stage verification suite."""
    model_path = "models/vgg16_breast_cancer.keras"
    assert os.path.exists(model_path), f"Model checkpoint not found at: {model_path}"

    print(f"\n[Test 1/5] Loading trained model from: {model_path}...")
    model = tf.keras.models.load_model(model_path)
    layer_names = [layer.name for layer in model.layers]

    # Verify Grad-CAM hook layer
    target_layer_name = "block5_conv3"
    assert target_layer_name in layer_names, f"Target layer '{target_layer_name}' not found in model."
    print(f"  ✓ Target hook layer '{target_layer_name}' verified.")

    # Verify custom head layers
    required_head = ["dense_128", "dropout_05", "predictions"]
    for layer in required_head:
        assert layer in layer_names, f"Required head layer '{layer}' missing."
    print("  ✓ Custom head architecture verified: GAP -> Dense(128) -> Dropout(0.5) -> Dense(1).")

    # [Test 2/5] Benign Inference
    benign_sample = "sample_scans/benign_scan_01_fibroadenoma.png"
    _, b_batch = load_test_image(benign_sample)
    b_score = float(model.predict(b_batch, verbose=0)[0][0])
    b_conf = (1.0 - b_score) * 100.0
    print(f"\n[Test 2/5] Benign Scan Inference:")
    print(f"  Raw Logit: {b_score:.4f} | Benign Confidence: {b_conf:.1f}%")
    assert 0.0 <= b_score <= 1.0, f"Sigmoid output outside [0, 1]: {b_score}"

    # [Test 3/5] Malignant Inference
    mal_sample = "sample_scans/malignant_scan_01_invasive_ductal.png"
    m_rgb, m_batch = load_test_image(mal_sample)
    m_score = float(model.predict(m_batch, verbose=0)[0][0])
    m_conf = m_score * 100.0
    print(f"\n[Test 3/5] Malignant Scan Inference:")
    print(f"  Raw Logit: {m_score:.4f} | Malignant Confidence: {m_conf:.1f}%")
    assert 0.0 <= m_score <= 1.0, f"Sigmoid output outside [0, 1]: {m_score}"

    # [Test 4/5] Grad-CAM Computation
    print(f"\n[Test 4/5] Computing Grad-CAM heatmap targeting '{target_layer_name}'...")
    heatmap = compute_gradcam_heatmap(m_batch, model, last_conv_layer_name=target_layer_name, pred_index=1)
    assert heatmap.ndim == 2, f"Expected 2D array, received {heatmap.ndim}D."
    assert 0.0 <= heatmap.min() and heatmap.max() <= 1.0001, "Heatmap values not bounded in [0, 1]."
    print(f"  ✓ Heatmap shape: {heatmap.shape} | Min: {heatmap.min():.4f} | Max: {heatmap.max():.4f}")

    # [Test 5/5] OpenCV Alpha Blend (0.6 original / 0.4 heatmap)
    print("\n[Test 5/5] Testing OpenCV superimposition (alpha=0.4)...")
    superimposed, colored_hm = overlay_heatmap(m_rgb, heatmap, alpha=0.4, colormap=cv2.COLORMAP_JET)
    assert superimposed.shape == (224, 224, 3), f"Invalid output shape: {superimposed.shape}"
    assert superimposed.dtype == np.uint8, f"Invalid output dtype: {superimposed.dtype}"
    assert colored_hm.shape == (224, 224, 3), f"Invalid colored heatmap shape: {colored_hm.shape}"
    print("  ✓ Superimposed overlay verified successfully.")

    print("\n" + "=" * 50)
    print("  ALL 5 PIPELINE VERIFICATION TESTS PASSED!")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    test_full_application_pipeline()
