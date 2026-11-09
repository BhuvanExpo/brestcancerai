"""
Breast Cancer AI Diagnostic Web Application
===========================================
Streamlit web interface featuring:
  - Transfer Learning with VGG-16 (ImageNet base, custom classification head)
  - Explainable AI via Grad-CAM (Targeting 'block5_conv3')
  - Interactive OpenCV colormap & alpha blending controls
  - Real-time diagnostic risk assessment (Benign vs. Malignant)
  - Medical metrics, training asset visualizer, and clinical disclaimer
"""

from dataclasses import dataclass
import io
import os
from typing import Dict, Optional, Tuple

import cv2
import numpy as np
from PIL import Image
import streamlit as st
import tensorflow as tf
from tensorflow.keras.applications.vgg16 import preprocess_input

from gradcam import compute_gradcam_heatmap, overlay_heatmap
from model_builder import save_initial_model

# ---------------------------------------------------------------------------
# Configuration Constants
# ---------------------------------------------------------------------------
MODEL_PATH: str = "models/vgg16_breast_cancer.keras"
TARGET_LAYER: str = "block5_conv3"
ASSETS_DIR: str = "assets"
INPUT_RESOLUTION: Tuple[int, int] = (224, 224)

SAMPLE_SCANS_MAP: Dict[str, str] = {
    "Benign: Fibroadenoma": "sample_scans/benign_scan_01_fibroadenoma.png",
    "Benign: Simple Cyst": "sample_scans/benign_scan_02_cyst.png",
    "Benign: Normal Glandular Tissue": "sample_scans/benign_scan_03_normal_parenchyma.png",
    "Malignant: Invasive Ductal Carcinoma": "sample_scans/malignant_scan_01_invasive_ductal.png",
    "Malignant: Lobulated Tumor": "sample_scans/malignant_scan_02_lobulated.png",
}

COLORMAP_OPTIONS: Dict[str, int] = {
    "COLORMAP_JET (Standard)": cv2.COLORMAP_JET,
    "COLORMAP_VIRIDIS": cv2.COLORMAP_VIRIDIS,
    "COLORMAP_HOT": cv2.COLORMAP_HOT,
    "COLORMAP_INFERNO": cv2.COLORMAP_INFERNO,
}


@dataclass
class SidebarSettings:
    """Encapsulates user-selected sidebar settings."""
    alpha_blend: float
    colormap: int
    selected_sample: str


# ---------------------------------------------------------------------------
# Styling & Theme
# ---------------------------------------------------------------------------
def inject_custom_styles() -> None:
    """Injects custom CSS for modern clinical UI styling."""
    st.markdown("""
    <style>
        .main-title {
            font-size: 2.2rem;
            font-weight: 800;
            color: #0F172A;
            margin-bottom: 0.1rem;
        }
        .sub-title {
            font-size: 1.05rem;
            color: #475569;
            margin-bottom: 1.6rem;
        }
        .badge-benign {
            background: linear-gradient(135deg, #10B981, #059669);
            color: #FFFFFF;
            padding: 0.65rem 1.4rem;
            border-radius: 50px;
            font-weight: 700;
            font-size: 1.15rem;
            display: inline-block;
            box-shadow: 0 4px 12px rgba(16, 185, 129, 0.35);
            margin: 0.5rem 0;
        }
        .badge-malignant {
            background: linear-gradient(135deg, #EF4444, #DC2626);
            color: #FFFFFF;
            padding: 0.65rem 1.4rem;
            border-radius: 50px;
            font-weight: 700;
            font-size: 1.15rem;
            display: inline-block;
            box-shadow: 0 4px 12px rgba(239, 68, 68, 0.35);
            margin: 0.5rem 0;
        }
        .metric-card {
            background: #F8FAFC;
            border: 1px solid #E2E8F0;
            border-radius: 10px;
            padding: 1.0rem;
            margin-top: 0.8rem;
        }
        .disclaimer-banner {
            background: #FFFBEB;
            border-left: 5px solid #F59E0B;
            padding: 0.9rem 1.2rem;
            border-radius: 6px;
            font-size: 0.88rem;
            color: #92400E;
            line-height: 1.5;
            margin-top: 1.0rem;
        }
    </style>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Cached Resource Loaders
# ---------------------------------------------------------------------------
@st.cache_resource(show_spinner="Loading VGG-16 neural model into memory...")
def load_diagnostic_model() -> tf.keras.Model:
    """
    Loads and caches the compiled VGG-16 model artifact.
    If the checkpoint is missing, initializes and serializes an initial instance.
    """
    if not os.path.exists(MODEL_PATH):
        st.info(f"Model checkpoint not found at `{MODEL_PATH}`. Initializing new base...")
        save_initial_model(MODEL_PATH)

    return tf.keras.models.load_model(MODEL_PATH)


@st.cache_data
def load_sample_scan(filepath: str) -> Optional[Image.Image]:
    """Caches loaded PIL sample scans to eliminate redundant disk I/O."""
    if os.path.exists(filepath):
        return Image.open(filepath).convert("RGB")
    return None


# ---------------------------------------------------------------------------
# Image Preprocessing & Parameter Utilities
# ---------------------------------------------------------------------------
def preprocess_scan(
    pil_image: Image.Image,
    target_size: Tuple[int, int] = INPUT_RESOLUTION
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Converts any input scan to an RGB numpy array and prepares normalized batch tensor.

    Args:
        pil_image: Uploaded or selected PIL Image.
        target_size: Expected model input resolution (H, W).

    Returns:
        Tuple[np.ndarray, np.ndarray]:
          - img_rgb: uint8 array of shape (target_size[0], target_size[1], 3).
          - preprocessed_batch: float32 batch tensor of shape (1, H, W, 3) normalized for VGG-16.
    """
    if pil_image.mode != "RGB":
        pil_image = pil_image.convert("RGB")

    resized_pil = pil_image.resize(target_size, Image.Resampling.BILINEAR)
    img_rgb = np.array(resized_pil, dtype=np.uint8)

    batch_tensor = np.expand_dims(img_rgb.astype(np.float32), axis=0)
    preprocessed_batch = preprocess_input(batch_tensor.copy())

    return img_rgb, preprocessed_batch


def get_model_parameters_summary(model: tf.keras.Model) -> Tuple[int, int, int]:
    """
    Extracts parameter counts compatible across Keras 2 and Keras 3.

    Returns:
        Tuple[int, int, int]: (total_params, trainable_params, non_trainable_params)
    """
    total = model.count_params()
    trainable = sum(int(np.prod(w.shape)) for w in model.trainable_weights)
    non_trainable = sum(int(np.prod(w.shape)) for w in model.non_trainable_weights)
    return total, trainable, non_trainable


# ---------------------------------------------------------------------------
# View Components
# ---------------------------------------------------------------------------
def render_sidebar() -> SidebarSettings:
    """Renders the sidebar controls and returns user configurations."""
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/2966/2966327.png", width=64)
        st.title("Diagnostic AI Controls")

        st.markdown("### 🔬 Model Configuration")
        st.markdown(f"""
        - **Backbone**: VGG-16 (ImageNet, frozen)
        - **Target Layer**: `{TARGET_LAYER}`
        - **Custom Head**: GAP + Dense(128) + Dropout(0.5) + Sigmoid(1)
        - **Resolution**: `224 × 224 × 3`
        """)

        st.markdown("---")
        st.markdown("### 🎛️ Grad-CAM Overlay Settings")
        alpha_blend = st.slider(
            "Heatmap Blend (Alpha)",
            min_value=0.1,
            max_value=0.9,
            value=0.4,
            step=0.05,
            help="0.4 produces standard 0.6 image / 0.4 heatmap blend."
        )

        cmap_label = st.selectbox(
            "OpenCV Colormap",
            options=list(COLORMAP_OPTIONS.keys()),
            index=0
        )
        selected_colormap = COLORMAP_OPTIONS[cmap_label]

        st.markdown("---")
        st.markdown("### 🧪 Quick Test Sample Scans")
        sample_options = ["Upload your own scan"] + list(SAMPLE_SCANS_MAP.keys())
        selected_sample = st.radio("Choose a sample scan or upload:", options=sample_options, index=0)

    return SidebarSettings(
        alpha_blend=alpha_blend,
        colormap=selected_colormap,
        selected_sample=selected_sample
    )


def render_header() -> None:
    """Displays page title and clinical description."""
    st.markdown('<div class="main-title">🎗️ Breast Cancer AI Diagnostic Web Platform</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-title">'
        'Transfer Learning (VGG-16) with Interpretable Layer-wise Grad-CAM Activation Heatmaps'
        '</div>',
        unsafe_allow_html=True
    )


def resolve_active_scan(
    uploaded_file,
    selected_sample: str
) -> Tuple[Optional[Image.Image], str]:
    """Determines active image from either user upload or sidebar selection."""
    if uploaded_file is not None:
        try:
            return Image.open(uploaded_file), uploaded_file.name
        except Exception as e:
            st.error(f"Error reading uploaded file: {e}")
            return None, ""

    if selected_sample != "Upload your own scan":
        filepath = SAMPLE_SCANS_MAP.get(selected_sample, "")
        img = load_sample_scan(filepath)
        if img is not None:
            return img, selected_sample
        st.warning(f"Sample scan file `{filepath}` not found. Please upload a scan.")

    return None, ""


def render_prediction_column(
    active_scan: Image.Image,
    scan_name: str,
    is_malignant: bool,
    confidence_pct: float,
    prob_malignant: float,
    prob_benign: float
) -> None:
    """Renders left column: input preview, diagnostic badge, and confidence bars."""
    st.subheader("📷 Original Scan & Prediction")
    st.image(active_scan, caption=f"Scan: {scan_name}", use_container_width=True)

    st.markdown("#### Clinical Assessment")
    if is_malignant:
        st.markdown(
            f'<div class="badge-malignant">🔴 MALIGNANT — {confidence_pct:.1f}% Confidence</div>',
            unsafe_allow_html=True
        )
        st.error(
            f"**Suspicious Tissue Pattern.** The convolutional network flagged morphological features "
            f"indicative of malignancy with **{confidence_pct:.1f}%** confidence."
        )
    else:
        st.markdown(
            f'<div class="badge-benign">🟢 BENIGN — {confidence_pct:.1f}% Confidence</div>',
            unsafe_allow_html=True
        )
        st.success(
            f"**Non-Malignant Characteristics.** The convolutional network identified benign / non-malignant tissue "
            f"characteristics with **{confidence_pct:.1f}%** confidence."
        )

    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown("**Confidence Probability Breakdown**")
    st.progress(float(prob_malignant), text=f"Malignancy Risk: {prob_malignant * 100:.1f}%")
    st.progress(float(prob_benign), text=f"Benign Probability: {prob_benign * 100:.1f}%")
    st.caption(f"Sigmoid Output Logit: `{prob_malignant:.4f}` | Decision Threshold: `0.50`")
    st.markdown('</div>', unsafe_allow_html=True)


def render_gradcam_column(
    superimposed_scan: np.ndarray,
    alpha_blend: float,
    diagnosis_label: str,
    scan_name: str
) -> None:
    """Renders right column: Grad-CAM heatmap, activation interpretation, and download."""
    st.subheader("🔥 Grad-CAM Explainability (Suspicious Regions)")
    st.image(
        superimposed_scan,
        caption=f"Superimposed Grad-CAM ({1.0 - alpha_blend:.1f} Scan / {alpha_blend:.1f} Heatmap)",
        use_container_width=True
    )

    st.markdown("#### Tissue Activation Analysis")
    st.info(
        f"**Gradient Backpropagation targeting layer `{TARGET_LAYER}`:**\n\n"
        f"- **Warm Colors (Red / Yellow)**: Highlight critical focal zones where feature activations "
        f"strongly swayed the model toward predicting **{diagnosis_label}**.\n"
        f"- **Cool Colors (Blue / Dark Blue)**: Receptive fields that had minimal or background influence."
    )

    result_pil = Image.fromarray(superimposed_scan)
    buf = io.BytesIO()
    result_pil.save(buf, format="PNG")
    st.download_button(
        label="💾 Download Superimposed Scan (PNG)",
        data=buf.getvalue(),
        file_name=f"gradcam_{diagnosis_label.lower()}_{scan_name}.png",
        mime="image/png"
    )


def render_metrics_and_architecture_expander(model: tf.keras.Model) -> None:
    """Renders expandable section containing architecture stats, assets, and disclaimer."""
    with st.expander("📊 Model Architecture Parameters, Training Metrics & Clinical Disclaimer", expanded=False):
        tab_arch, tab_metrics, tab_disclaimer = st.tabs([
            "🧠 Architecture Parameters",
            "📈 Evaluation Metrics & Assets",
            "⚠️ Clinical Disclaimer"
        ])

        with tab_arch:
            st.markdown("### Neural Architecture Specifications")
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("""
                - **Backbone**: Pre-trained VGG-16 (ImageNet weights)
                - **Convolutional Base**: Frozen (`trainable = False`)
                - **Target Convolutional Layer**: `block5_conv3` (512 feature channels, 14×14 spatial resolution)
                - **Input Dimensions**: `(224, 224, 3)`
                """)
            with col_b:
                st.markdown("""
                - **Pooling**: `GlobalAveragePooling2D`
                - **Dense Classifier**: `Dense(128, activation='relu')`
                - **Regularization**: `Dropout(0.5)`
                - **Output Head**: `Dense(1, activation='sigmoid')` (Benign: 0, Malignant: 1)
                - **Optimization**: Adam (`lr=1e-4`), Binary Cross-Entropy
                """)

            total_p, trainable_p, non_trainable_p = get_model_parameters_summary(model)
            st.markdown(f"""
            | Parameter Category | Count |
            | :--- | :--- |
            | **Total Parameters** | {total_p:,} |
            | **Trainable Parameters (Custom Top Head)** | {trainable_p:,} |
            | **Non-Trainable Parameters (Frozen VGG-16 Backbone)** | {non_trainable_p:,} |
            """)

        with tab_metrics:
            st.markdown("### Validation Performance & Evaluation Assets")
            col_m1, col_m2 = st.columns(2)

            history_fig = os.path.join(ASSETS_DIR, "training_history.png")
            cm_fig = os.path.join(ASSETS_DIR, "confusion_matrix.png")
            report_file = os.path.join(ASSETS_DIR, "classification_report.txt")

            with col_m1:
                if os.path.exists(history_fig):
                    st.image(history_fig, caption="Loss & Accuracy Training History", use_container_width=True)
                else:
                    st.caption("Training history asset not found. Run `python train.py` to generate.")

            with col_m2:
                if os.path.exists(cm_fig):
                    st.image(cm_fig, caption="Validation Confusion Matrix", use_container_width=True)
                else:
                    st.caption("Confusion matrix asset not found. Run `python train.py` to generate.")

            if os.path.exists(report_file):
                st.markdown("#### Classification Report")
                with open(report_file, "r") as f:
                    st.code(f.read(), language="text")

        with tab_disclaimer:
            st.markdown("""
            <div class="disclaimer-banner">
                <strong>⚠️ Medical Diagnostic Disclaimer:</strong><br>
                This application is an engineering demonstration of Transfer Learning and Explainable AI (Grad-CAM).
                It is designed strictly for research, educational, and workflow evaluation purposes.<br>
                It is <strong>NOT</strong> an FDA-cleared or CE-marked medical device and must never be utilized as a sole
                substitute for professional radiological assessment, biopsy confirmation, or clinical decision-making.
            </div>
            """, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Application Entry Point
# ---------------------------------------------------------------------------
def main() -> None:
    """Main application orchestrator."""
    st.set_page_config(
        page_title="Breast Cancer AI Diagnostic Platform | VGG-16 & Grad-CAM",
        page_icon="🎗️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    inject_custom_styles()
    settings = render_sidebar()
    render_header()

    try:
        model = load_diagnostic_model()
    except Exception as e:
        st.error(f"Failed to load diagnostic model: {e}")
        st.stop()

    uploaded_file = st.file_uploader(
        "Drag and drop or upload a breast histopathology or mammogram scan (JPG, JPEG, PNG)",
        type=["jpg", "jpeg", "png"],
        help="Supports standard radiological scans and histopathology slides."
    )

    active_scan, scan_name = resolve_active_scan(uploaded_file, settings.selected_sample)

    if active_scan is not None:
        img_rgb_224, preprocessed_batch = preprocess_scan(active_scan)

        with st.spinner("Executing neural inference and computing Grad-CAM gradients..."):
            predictions = model.predict(preprocessed_batch, verbose=0)
            prob_malignant = float(predictions[0][0])
            prob_benign = 1.0 - prob_malignant
            is_malignant = prob_malignant >= 0.5
            diagnosis_label = "Malignant" if is_malignant else "Benign"
            confidence_pct = (prob_malignant if is_malignant else prob_benign) * 100.0

            # Compute Grad-CAM heatmap targeting layer block5_conv3
            target_class_idx = 1 if is_malignant else 0
            heatmap = compute_gradcam_heatmap(
                preprocessed_batch,
                model,
                last_conv_layer_name=TARGET_LAYER,
                pred_index=target_class_idx
            )

            superimposed_scan, _ = overlay_heatmap(
                img_rgb_224,
                heatmap,
                alpha=settings.alpha_blend,
                colormap=settings.colormap
            )

        col_left, col_right = st.columns([1, 1], gap="large")

        with col_left:
            render_prediction_column(
                active_scan=active_scan,
                scan_name=scan_name,
                is_malignant=is_malignant,
                confidence_pct=confidence_pct,
                prob_malignant=prob_malignant,
                prob_benign=prob_benign
            )

        with col_right:
            render_gradcam_column(
                superimposed_scan=superimposed_scan,
                alpha_blend=settings.alpha_blend,
                diagnosis_label=diagnosis_label,
                scan_name=scan_name
            )
    else:
        st.info("👈 Please upload a breast scan (JPG/JPEG/PNG) or select one of the labeled sample scans from the sidebar.")

    render_metrics_and_architecture_expander(model)


if __name__ == "__main__":
    main()
