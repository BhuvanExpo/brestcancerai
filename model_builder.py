"""
Breast Cancer Diagnostic Model Builder
=======================================
Constructs and compiles the VGG-16 Transfer Learning architecture for
binary classification of histopathological and ultrasound breast scans:
  - Base: Pre-trained VGG-16 (ImageNet weights, convolutional base frozen)
  - Custom Head:
      * GlobalAveragePooling2D
      * Dense(128, activation='relu')
      * Dropout(0.5)
      * Dense(1, activation='sigmoid')
  - Optimizer: Adam(learning_rate=1e-4)
  - Loss: binary_crossentropy
  - Metrics: accuracy, Precision, Recall, AUC
"""

import os
from typing import Tuple

import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications.vgg16 import VGG16


def build_vgg16_breast_cancer_model(
    input_shape: Tuple[int, int, int] = (224, 224, 3),
    learning_rate: float = 1e-4
) -> tf.keras.Model:
    """
    Builds and compiles the transfer learning model.

    Args:
        input_shape: Tuple specifying input image dimensions (H, W, C).
        learning_rate: Learning rate for Adam optimizer.

    Returns:
        tf.keras.Model: Compiled Keras model ready for training or inference.
    """
    # 1. Base convolutional backbone with pre-trained ImageNet weights
    base_model = VGG16(
        weights="imagenet",
        include_top=False,
        input_shape=input_shape
    )

    # 2. Freeze convolutional base to retain generic visual feature extractors
    base_model.trainable = False

    # 3. Custom classification top head
    inputs = base_model.input
    x = base_model.output
    x = layers.GlobalAveragePooling2D(name="global_avg_pool")(x)
    x = layers.Dense(128, activation="relu", name="dense_128")(x)
    x = layers.Dropout(0.5, name="dropout_05")(x)
    outputs = layers.Dense(1, activation="sigmoid", name="predictions")(x)

    # 4. Assemble functional model
    model = models.Model(inputs=inputs, outputs=outputs, name="vgg16_breast_cancer")

    # 5. Compile with standard clinical diagnostic metrics
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
        loss="binary_crossentropy",
        metrics=[
            "accuracy",
            tf.keras.metrics.Precision(name="precision"),
            tf.keras.metrics.Recall(name="recall"),
            tf.keras.metrics.AUC(name="auc"),
        ]
    )

    return model


def save_initial_model(output_path: str = "models/vgg16_breast_cancer.keras") -> tf.keras.Model:
    """
    Builds the model and saves initial weights to disk.

    Args:
        output_path: Destination path for the .keras model artifact.

    Returns:
        tf.keras.Model: The initialized and saved model.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    print(f"[ModelBuilder] Constructing VGG-16 model (frozen base + custom head)...")
    model = build_vgg16_breast_cancer_model()
    model.save(output_path)
    print(f"[ModelBuilder] Model successfully saved to: {output_path}")
    return model


if __name__ == "__main__":
    save_initial_model()
