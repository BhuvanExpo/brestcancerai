"""
Breast Cancer Model Training Pipeline
======================================
Automated training, evaluation, and asset generation script for the
VGG-16 Transfer Learning Breast Cancer Diagnostic model.

Pipeline Stages:
  1. Dataset Verification & Synthetic Ingestion Fallback
  2. tf.data Pipeline Optimization (Caching + Autotune Prefetching)
  3. Transfer Learning Architecture Assembly (via model_builder.py)
  4. 10-Epoch Model Fitting
  5. Weight Serialization ('models/vgg16_breast_cancer.keras')
  6. Diagnostic Visualizations & Reporting:
       - 'assets/training_history.png' (Loss & Accuracy curves)
       - 'assets/confusion_matrix.png' (Seaborn heatmap with TN, FP, FN, TP)
       - 'assets/classification_report.txt' (Sensitivity, Specificity, PPV, NPV)
"""

import argparse
import os
from typing import List, Tuple

import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for headless environments
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix
import tensorflow as tf
from tensorflow.keras.applications.vgg16 import preprocess_input

from model_builder import build_vgg16_breast_cancer_model


def create_synthetic_dataset_if_needed(
    train_dir: str,
    val_dir: str,
    num_train: int = 30,
    num_val: int = 10
) -> None:
    """
    Creates synthetic labeled breast scans if local training directories
    are empty, enabling zero-setup verification and testing.

    Args:
        train_dir: Target training dataset folder.
        val_dir: Target validation dataset folder.
        num_train: Number of scans per class for training.
        num_val: Number of scans per class for validation.
    """
    for split_dir in [train_dir, val_dir]:
        os.makedirs(os.path.join(split_dir, "benign"), exist_ok=True)
        os.makedirs(os.path.join(split_dir, "malignant"), exist_ok=True)

    # Check if adequate samples already exist
    train_benign = len(os.listdir(os.path.join(train_dir, "benign")))
    train_mal = len(os.listdir(os.path.join(train_dir, "malignant")))
    if train_benign >= 5 and train_mal >= 5:
        print(f"[Data] Found existing dataset: {train_benign} benign, {train_mal} malignant scans.")
        return

    print("[Data] Generating synthetic training and validation dataset...")

    def _render_scan(is_malignant: bool, seed: int, size: Tuple[int, int] = (224, 224)) -> Image.Image:
        np.random.seed(seed)
        base = np.random.normal(loc=120, scale=30, size=size).clip(20, 220).astype(np.uint8)
        img = Image.fromarray(base).filter(ImageFilter.GaussianBlur(radius=1.5))
        draw = ImageDraw.Draw(img)

        if not is_malignant:
            # Benign: circumscribed hypoechoic oval lesion
            cx, cy = np.random.randint(90, 134), np.random.randint(90, 134)
            rx, ry = np.random.randint(25, 45), np.random.randint(18, 30)
            draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=np.random.randint(35, 55))
            img = img.filter(ImageFilter.GaussianBlur(radius=1.8))
        else:
            # Malignant: irregular, spiculated mass with acoustic shadow
            cx, cy = np.random.randint(90, 134), np.random.randint(80, 120)
            num_pts = np.random.randint(8, 14)
            pts = []
            for i in range(num_pts):
                angle = 2.0 * np.pi * i / num_pts
                r = np.random.randint(25, 50)
                pts.append((int(cx + r * np.cos(angle)), int(cy + r * np.sin(angle))))
            draw.polygon(pts, fill=np.random.randint(20, 40))
            # Acoustic shadowing beneath mass
            draw.polygon([(cx - 25, cy + 30), (cx + 25, cy + 30), (cx + 35, 220), (cx - 35, 220)], fill=30)
            img = img.filter(ImageFilter.GaussianBlur(radius=2.0))

        noisy = np.clip(np.array(img, dtype=np.int16) + np.random.normal(0, 10, size=size), 0, 255).astype(np.uint8)
        return Image.fromarray(noisy).convert("RGB")

    # Generate training split
    for i in range(num_train):
        _render_scan(False, seed=1000 + i).save(os.path.join(train_dir, "benign", f"synthetic_benign_{i:03d}.png"))
        _render_scan(True, seed=2000 + i).save(os.path.join(train_dir, "malignant", f"synthetic_malignant_{i:03d}.png"))

    # Generate validation split
    for i in range(num_val):
        _render_scan(False, seed=3000 + i).save(os.path.join(val_dir, "benign", f"synthetic_benign_val_{i:03d}.png"))
        _render_scan(True, seed=4000 + i).save(os.path.join(val_dir, "malignant", f"synthetic_malignant_val_{i:03d}.png"))

    print(f"[Data] Created {num_train * 2} training scans and {num_val * 2} validation scans.")


def load_dataset(
    train_dir: str,
    val_dir: str,
    img_size: Tuple[int, int] = (224, 224),
    batch_size: int = 16
) -> Tuple[tf.data.Dataset, tf.data.Dataset, List[str]]:
    """
    Builds optimized tf.data.Dataset pipelines with VGG-16 normalization, caching,
    and autotuned prefetching.

    Args:
        train_dir: Training data directory path.
        val_dir: Validation data directory path.
        img_size: Target image dimensions (H, W).
        batch_size: Batch size for training and validation.

    Returns:
        Tuple containing (train_dataset, validation_dataset, class_names).
    """
    train_raw = tf.keras.utils.image_dataset_from_directory(
        train_dir,
        image_size=img_size,
        batch_size=batch_size,
        label_mode="binary",
        shuffle=True,
        seed=42
    )

    val_raw = tf.keras.utils.image_dataset_from_directory(
        val_dir,
        image_size=img_size,
        batch_size=batch_size,
        label_mode="binary",
        shuffle=False,
        seed=42
    )

    class_names = train_raw.class_names
    print(f"[Data] Detected classes: {class_names}")

    def _normalize_batch(images: tf.Tensor, labels: tf.Tensor) -> Tuple[tf.Tensor, tf.Tensor]:
        return preprocess_input(images), labels

    # Optimize pipeline: normalize -> cache -> prefetch
    train_ds = (
        train_raw
        .map(_normalize_batch, num_parallel_calls=tf.data.AUTOTUNE)
        .cache()
        .prefetch(buffer_size=tf.data.AUTOTUNE)
    )

    val_ds = (
        val_raw
        .map(_normalize_batch, num_parallel_calls=tf.data.AUTOTUNE)
        .cache()
        .prefetch(buffer_size=tf.data.AUTOTUNE)
    )

    return train_ds, val_ds, class_names


def plot_training_history(history: tf.keras.callbacks.History, output_path: str) -> None:
    """
    Plots training and validation Loss and Accuracy across epochs and saves as PNG.

    Args:
        history: Keras History object from model.fit().
        output_path: Destination path for the plot image.
    """
    epochs_range = range(1, len(history.history["loss"]) + 1)
    fig, (ax_loss, ax_acc) = plt.subplots(1, 2, figsize=(14, 5))

    # Loss subplot
    ax_loss.plot(epochs_range, history.history["loss"], "o-", label="Train Loss", color="#1f77b4", linewidth=2)
    ax_loss.plot(epochs_range, history.history["val_loss"], "s--", label="Val Loss", color="#ff7f0e", linewidth=2)
    ax_loss.set_title("Binary Cross-Entropy Loss vs. Epochs", fontsize=13, fontweight="bold")
    ax_loss.set_xlabel("Epoch", fontsize=11)
    ax_loss.set_ylabel("Loss", fontsize=11)
    ax_loss.grid(True, linestyle="--", alpha=0.6)
    ax_loss.legend(loc="upper right", frameon=True)

    # Accuracy subplot
    ax_acc.plot(epochs_range, history.history["accuracy"], "o-", label="Train Accuracy", color="#2ca02c", linewidth=2)
    ax_acc.plot(epochs_range, history.history["val_accuracy"], "s--", label="Val Accuracy", color="#d62728", linewidth=2)
    ax_acc.set_title("Classification Accuracy vs. Epochs", fontsize=13, fontweight="bold")
    ax_acc.set_xlabel("Epoch", fontsize=11)
    ax_acc.set_ylabel("Accuracy", fontsize=11)
    ax_acc.grid(True, linestyle="--", alpha=0.6)
    ax_acc.legend(loc="lower right", frameon=True)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def evaluate_and_save_metrics(
    model: tf.keras.Model,
    val_ds: tf.data.Dataset,
    cm_path: str,
    report_path: str
) -> None:
    """
    Evaluates the model on validation data, generates a 2x2 confusion matrix heatmap,
    and computes sensitivity, specificity, PPV, and NPV.

    Args:
        model: Trained Keras model.
        val_ds: Preprocessed validation dataset.
        cm_path: Output path for confusion matrix PNG.
        report_path: Output path for classification report text file.
    """
    y_true_list = []
    y_pred_probs_list = []

    for images, labels in val_ds:
        preds = model.predict(images, verbose=0)
        y_true_list.extend(labels.numpy().flatten())
        y_pred_probs_list.extend(preds.flatten())

    y_true = np.array(y_true_list, dtype=int)
    y_pred_probs = np.array(y_pred_probs_list, dtype=float)
    y_pred = (y_pred_probs >= 0.5).astype(int)

    # 1. Confusion Matrix
    cm = confusion_matrix(y_true, y_pred)
    total_samples = len(y_true)

    if cm.shape == (2, 2):
        tn, fp, fn, tp = cm.ravel()
        labels_text = np.array([
            [f"True Benign (TN)\n{tn}\n({(tn / total_samples * 100):.1f}%)",
             f"False Malignant (FP)\n{fp}\n({(fp / total_samples * 100):.1f}%)"],
            [f"False Benign (FN)\n{fn}\n({(fn / total_samples * 100):.1f}%)",
             f"True Malignant (TP)\n{tp}\n({(tp / total_samples * 100):.1f}%)"]
        ])
    else:
        tn = fp = fn = tp = 0
        labels_text = np.array([[str(val) for val in row] for row in cm])

    plt.figure(figsize=(7, 6))
    sns.heatmap(
        cm,
        annot=labels_text,
        fmt="",
        cmap="Blues",
        cbar=True,
        xticklabels=["Predicted Benign", "Predicted Malignant"],
        yticklabels=["Actual Benign", "Actual Malignant"],
        annot_kws={"fontsize": 11, "fontweight": "bold"}
    )
    plt.title("Confusion Matrix (Benign vs. Malignant)", fontsize=14, fontweight="bold", pad=12)
    plt.ylabel("Ground Truth Class", fontsize=12)
    plt.xlabel("Model Prediction", fontsize=12)
    plt.tight_layout()
    plt.savefig(cm_path, dpi=300)
    plt.close()
    print(f"[Metrics] Saved confusion matrix to: {cm_path}")

    # 2. Classification Report & Clinical Diagnostics
    target_names = ["Benign (0)", "Malignant (1)"] if len(np.unique(y_true)) > 1 else None
    report_str = classification_report(
        y_true,
        y_pred,
        target_names=target_names,
        digits=4,
        zero_division=0
    )

    with open(report_path, "w") as f:
        f.write("=" * 65 + "\n")
        f.write("      BREAST CANCER CLASSIFICATION REPORT (VGG-16)\n")
        f.write("=" * 65 + "\n\n")
        f.write(report_str)
        f.write("\n" + "=" * 65 + "\n")
        if cm.shape == (2, 2):
            sensitivity = tp / (tp + fn + 1e-9)
            specificity = tn / (tn + fp + 1e-9)
            ppv = tp / (tp + fp + 1e-9)
            npv = tn / (tn + fn + 1e-9)
            f.write(f"Diagnostic Sensitivity (Recall): {sensitivity:.4f}\n")
            f.write(f"Diagnostic Specificity:         {specificity:.4f}\n")
            f.write(f"Positive Predictive Value (PPV): {ppv:.4f}\n")
            f.write(f"Negative Predictive Value (NPV): {npv:.4f}\n")
            f.write("=" * 65 + "\n")

    print(f"[Metrics] Saved classification report to: {report_path}")
    print("\n" + report_str)


def train_pipeline(
    data_root: str = "data",
    model_save_path: str = "models/vgg16_breast_cancer.keras",
    assets_dir: str = "assets",
    epochs: int = 10,
    batch_size: int = 16
) -> None:
    """
    Executes the complete training workflow from data loading to artifact export.

    Args:
        data_root: Root dataset directory containing train/ and val/ folders.
        model_save_path: File path to save the trained model (.keras).
        assets_dir: Directory where evaluation plots and reports are saved.
        epochs: Number of training epochs.
        batch_size: Batch size for training.
    """
    os.makedirs(os.path.dirname(model_save_path), exist_ok=True)
    os.makedirs(assets_dir, exist_ok=True)

    train_dir = os.path.join(data_root, "train")
    val_dir = os.path.join(data_root, "val")

    # Step 1: Ensure dataset availability
    create_synthetic_dataset_if_needed(train_dir, val_dir)

    # Step 2: Ingest and pre-process datasets
    train_ds, val_ds, _ = load_dataset(train_dir, val_dir, img_size=(224, 224), batch_size=batch_size)

    # Step 3: Build model architecture
    print("\n[Train] Assembling VGG-16 transfer learning model...")
    model = build_vgg16_breast_cancer_model(input_shape=(224, 224, 3), learning_rate=1e-4)
    model.summary()

    # Step 4: Fit model
    print(f"\n[Train] Starting training routine ({epochs} epochs)...")
    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs,
        verbose=1
    )

    # Step 5: Save weights
    print(f"\n[Train] Serializing model weights to: {model_save_path}")
    model.save(model_save_path)
    print("  ✓ Model saved successfully.")

    # Step 6: Plot loss and accuracy curves
    history_plot_path = os.path.join(assets_dir, "training_history.png")
    plot_training_history(history, history_plot_path)
    print(f"  ✓ Saved history curves to: {history_plot_path}")

    # Step 7: Evaluate and generate metrics
    cm_plot_path = os.path.join(assets_dir, "confusion_matrix.png")
    report_file_path = os.path.join(assets_dir, "classification_report.txt")
    evaluate_and_save_metrics(model, val_ds, cm_plot_path, report_file_path)

    print("\n✓ Training pipeline completed successfully!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Breast Cancer VGG-16 Transfer Learning Model")
    parser.add_argument("--data_dir", type=str, default="data", help="Root directory containing dataset")
    parser.add_argument("--model_path", type=str, default="models/vgg16_breast_cancer.keras", help="Model destination path")
    parser.add_argument("--assets_dir", type=str, default="assets", help="Assets output directory")
    parser.add_argument("--epochs", type=int, default=10, help="Number of training epochs (default: 10)")
    parser.add_argument("--batch_size", type=int, default=16, help="Batch size (default: 16)")
    args = parser.parse_args()

    train_pipeline(
        data_root=args.data_dir,
        model_save_path=args.model_path,
        assets_dir=args.assets_dir,
        epochs=args.epochs,
        batch_size=args.batch_size
    )
