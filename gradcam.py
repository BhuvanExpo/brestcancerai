"""
Grad-CAM: Visual Explanations via Gradient-weighted Class Activation Mapping
=============================================================================
Targets layer 'block5_conv3' of the VGG-16 backbone to generate visual
explanations highlighting suspicious morphological tissue regions.

Mathematical Formulation:
  1. Neuron importance weights (Global Average Pooling of gradients):
       alpha_k^c = (1 / Z) * sum_i sum_j (d y^c / d A_{i,j}^k)
  2. Weighted combination followed by ReLU:
       L_{Grad-CAM}^c = ReLU( sum_k alpha_k^c * A^k )
  3. Superimposition:
       Overlay = alpha * Heatmap + (1 - alpha) * Original Scan
"""

from typing import Optional, Tuple
import cv2
import numpy as np
import tensorflow as tf


def get_gradcam_submodel(
    model: tf.keras.Model,
    last_conv_layer_name: str = "block5_conv3"
) -> tf.keras.Model:
    """
    Constructs (or retrieves cached) submodel that outputs both the target
    feature maps and the final class predictions for gradient backpropagation.

    Performance Optimization:
      Caches the submodel on the parent model instance to avoid expensive
      re-instantiation of functional computational graphs on repeated inferences.

    Args:
        model: Trained Keras classification model.
        last_conv_layer_name: Target convolutional layer name (default: 'block5_conv3').

    Returns:
        tf.keras.Model: Multi-output submodel [conv_layer_output, final_prediction].
    """
    cache_attr = f"_gradcam_submodel_{last_conv_layer_name}"
    cached = getattr(model, cache_attr, None)
    if cached is not None:
        return cached

    target_layer = model.get_layer(last_conv_layer_name)
    submodel = tf.keras.models.Model(
        inputs=model.inputs,
        outputs=[target_layer.output, model.output]
    )
    setattr(model, cache_attr, submodel)
    return submodel


def compute_gradcam_heatmap(
    img_array: np.ndarray,
    model: tf.keras.Model,
    last_conv_layer_name: str = "block5_conv3",
    pred_index: Optional[int] = None
) -> np.ndarray:
    """
    Computes a normalized Grad-CAM activation heatmap for the given input image.

    Args:
        img_array: Preprocessed batch tensor of shape (1, 224, 224, 3).
        model: Trained Keras model.
        last_conv_layer_name: Target convolutional layer (default: 'block5_conv3').
        pred_index: Target class index:
                    0 = Benign (score = 1 - P(Malignant)),
                    1 = Malignant (score = P(Malignant)).
                    If None, targets the predicted class.

    Returns:
        np.ndarray: 2D float32 heatmap array with values normalized to [0.0, 1.0].
    """
    grad_model = get_gradcam_submodel(model, last_conv_layer_name=last_conv_layer_name)
    img_tensor = tf.cast(img_array, tf.float32)

    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(img_tensor)

        # Handle binary classification with sigmoid output (shape: [1, 1])
        if predictions.shape[-1] == 1:
            score = predictions[0][0]
            if pred_index == 0:
                target_score = 1.0 - score  # Target Benign
            else:
                target_score = score        # Target Malignant
        else:
            if pred_index is None:
                pred_index = tf.argmax(predictions[0])
            target_score = predictions[:, pred_index]

    # Compute gradients of target score with respect to convolutional feature maps
    grads = tape.gradient(target_score, conv_outputs)
    if grads is None:
        raise ValueError(
            f"Gradient computation failed. Ensure '{last_conv_layer_name}' is connected "
            f"to model inputs and outputs."
        )

    # 1. Global Average Pooling across spatial dimensions (height, width)
    # Resulting shape: (num_channels,)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    # 2. Weight feature maps by gradient importance
    feature_maps = conv_outputs[0]
    heatmap = feature_maps @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)

    # 3. Apply ReLU: only retain features that positively correlate with target class
    heatmap = tf.maximum(heatmap, 0.0)

    # 4. Normalize to [0.0, 1.0] for stable visualization
    max_val = tf.math.reduce_max(heatmap)
    if max_val > 0.0:
        heatmap = heatmap / max_val
    else:
        heatmap = tf.zeros_like(heatmap)

    return heatmap.numpy()


def overlay_heatmap(
    img_rgb: np.ndarray,
    heatmap: np.ndarray,
    alpha: float = 0.4,
    colormap: int = cv2.COLORMAP_JET
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Superimposes a color-mapped Grad-CAM heatmap onto the original RGB image.

    Blends using OpenCV addWeighted:
        Overlay = (alpha * Heatmap) + ((1 - alpha) * Original Scan)
    With default alpha=0.4, this yields the standard 0.6 image / 0.4 heatmap blend.

    Args:
        img_rgb: Original image array as uint8 RGB (H, W, 3).
        heatmap: 2D Grad-CAM heatmap normalized to [0.0, 1.0].
        alpha: Weight for heatmap blend (default: 0.4).
        colormap: OpenCV colormap constant (default: cv2.COLORMAP_JET).

    Returns:
        Tuple[np.ndarray, np.ndarray]:
          - superimposed: Blended RGB image uint8 of shape (H, W, 3).
          - colored_heatmap_rgb: Color-mapped heatmap uint8 of shape (H, W, 3).
    """
    height, width = img_rgb.shape[:2]

    # Resize heatmap to match original image dimensions
    heatmap_resized = cv2.resize(heatmap, (width, height))

    # Scale to 8-bit [0, 255]
    heatmap_uint8 = np.uint8(255 * np.clip(heatmap_resized, 0.0, 1.0))

    # Apply colormap (returns BGR) and convert to RGB
    colored_heatmap_bgr = cv2.applyColorMap(heatmap_uint8, colormap)
    colored_heatmap_rgb = cv2.cvtColor(colored_heatmap_bgr, cv2.COLOR_BGR2RGB)

    # Alpha blend: (Heatmap * alpha) + (Original * beta)
    beta = 1.0 - alpha
    superimposed = cv2.addWeighted(colored_heatmap_rgb, alpha, img_rgb, beta, 0.0)

    return superimposed, colored_heatmap_rgb


# ---------------------------------------------------------------------------
# Backwards-compatibility aliases
# ---------------------------------------------------------------------------
make_gradcam_heatmap = compute_gradcam_heatmap
superimpose_heatmap = overlay_heatmap
