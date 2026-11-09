# 🎗️ Production-Ready Breast Cancer Classification Web Application
### Transfer Learning (VGG-16) & Grad-CAM Explainability

An end-to-end medical computer vision application designed to classify histopathological and mammogram scans into **"Benign"** vs. **"Malignant"** with high sensitivity and clinical interpretability using **Grad-CAM (Gradient-weighted Class Activation Mapping)**.

---

## 🏗️ System Architecture & Specifications

1. **Backbone**:
   - Pre-trained **VGG-16** convolutional neural network initialized with **ImageNet** weights.
   - Convolutional base is frozen (`trainable = False`) to preserve rich low-level and mid-level feature representations.
2. **Custom Top Head**:
   - `GlobalAveragePooling2D()`
   - `Dense(128, activation='relu')`
   - `Dropout(0.5)`
   - `Dense(1, activation='sigmoid')` (Output: 0 = Benign, 1 = Malignant)
3. **Training Pipeline**:
   - Input shape: `(224, 224, 3)`
   - Optimizer: `Adam(learning_rate=1e-4)`
   - Loss Function: `binary_crossentropy`
   - Evaluation Metrics: `accuracy`, `Precision`, `Recall`, `AUC`
4. **Explainable AI (Grad-CAM)**:
   - Target layer: `block5_conv3` (the deepest convolutional layer in VGG-16 block 5).
   - Computes activation gradients via `tf.GradientTape`, applies channel-wise global average pooling, applies ReLU, and normalizes to $[0, 1]$.
   - Generates an OpenCV heatmap (`cv2.COLORMAP_JET`) with a **0.6 image / 0.4 heatmap blend** via `cv2.addWeighted`.

---

## 📁 Project Directory Structure

```text
├── app.py                      # Production Streamlit diagnostic dashboard
├── train.py                    # Standalone training script (CPU/GPU/Colab)
├── gradcam.py                  # Grad-CAM explainability & OpenCV overlay functions
├── model_builder.py            # VGG-16 architecture definition & model initialization
├── generate_sample_data.py      # Helper generating 5 labeled synthetic test scans
├── test_pipeline.py            # Automated end-to-end verification test suite
├── requirements.txt            # Pinned compatible versions for all dependencies
├── models/
│   └── vgg16_breast_cancer.keras  # Saved trained model artifact (57 MB)
├── assets/
│   ├── training_history.png    # Epochs vs Loss & Accuracy plots
│   ├── confusion_matrix.png    # Validation confusion matrix heatmap (TN, FP, FN, TP)
│   └── classification_report.txt # Detailed precision, recall, F1-score & sensitivity
├── data/
│   ├── train/                  # Training set (benign/ & malignant/)
│   └── val/                    # Validation set (benign/ & malignant/)
└── sample_scans/
    ├── benign_scan_01_fibroadenoma.png
    ├── benign_scan_02_cyst.png
    ├── benign_scan_03_normal_parenchyma.png
    ├── malignant_scan_01_invasive_ductal.png
    └── malignant_scan_02_lobulated.png
```

---

## 🚀 Quick Start Guide

### 1. Environment Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Generate Sample Data (Out-of-the-Box Testing)

```bash
python generate_sample_data.py
```

### 3. Run the Standalone Training Pipeline

Trains for 10 epochs, generates the model checkpoint and all diagnostic asset artifacts:

```bash
python train.py --epochs 10
```

This generates:
- `models/vgg16_breast_cancer.keras`
- `assets/training_history.png`
- `assets/confusion_matrix.png`
- `assets/classification_report.txt`

### 4. Launch the Streamlit Diagnostic Web App

```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## 🖥️ Streamlit Dashboard Features

- **Cached Model Loading**: Cached via `@st.cache_resource` for zero-lag subsequent predictions.
- **Drag-and-Drop Scanner**: Accepts `.jpg`, `.jpeg`, and `.png` scans with real-time preprocessing.
- **Quick Test Presets**: Select from 5 labeled ultrasound sample scans right from the sidebar.
- **Two-Column Responsive Layout**:
  - **Left Column**: High-resolution scan preview + bold diagnosis badge (`🟢 BENIGN` / `🔴 MALIGNANT`) + dual confidence meters.
  - **Right Column**: Superimposed Grad-CAM activation map highlighting suspicious lesion morphology.
- **Detailed Parameter Expander**:
  - Tab 1: Architecture specs, layer shapes, parameter counts.
  - Tab 2: Training history curves, confusion matrix, and classification report.
  - Tab 3: Medical decision-support disclaimer.

---

## 🔬 Explainability Mathematics (Grad-CAM)

1. Compute gradient of target class score $y^c$ with respect to feature map $A^k$ of `block5_conv3`:
   $$\alpha_k^c = \frac{1}{Z} \sum_{i=1}^u \sum_{j=1}^v \frac{\partial y^c}{\partial A_{i, j}^k}$$
2. Take the weighted sum of feature maps followed by ReLU:
   $$L_{\text{Grad-CAM}}^c = \text{ReLU}\left(\sum_k \alpha_k^c A^k\right)$$
3. Resize to input dimensions $(224, 224)$ and overlay onto original scan $I$:
   $$I_{\text{blended}} = 0.6 \cdot I_{\text{scan}} + 0.4 \cdot I_{\text{heatmap}}$$

---

## ⚠️ Clinical Disclaimer

This software is developed strictly for research, benchmarking, and educational purposes. It has not been evaluated by the FDA or regulatory health authorities and must never substitute for clinical radiological evaluation or histological biopsy confirmation.
