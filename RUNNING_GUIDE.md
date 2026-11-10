# 🎗️ Universal Running & Deployment Guide
### Breast Cancer AI Diagnostic Platform (VGG-16 & Grad-CAM)

This comprehensive guide is designed for **all user profiles** — from non-technical evaluators who want to test the app in a web browser without installing anything, to developers, data scientists, and DevOps engineers running it on macOS, Linux, Windows, Google Colab, or Docker.

---

## 🎯 Quick Navigation: Choose Your Profile

| User Profile | Recommended Running Method | Time to Run |
| :--- | :--- | :--- |
| **1. Non-Technical / Evaluator** | [Instant Cloud Web Access (Zero-Install)](#1-instant-cloud-web-access-zero-install) | 0 seconds |
| **2. One-Click Local User** | [Automated 1-Click Launchers (`run.sh` / `run.bat`)](#2-one-click-local-launchers-macos-linux--windows) | 30 seconds |
| **3. Developer / CLI User** | [Manual Virtual Environment Setup](#3-developer--cli-step-by-step-setup) | 1 minute |
| **4. ML Engineer / Researcher** | [Model Training, Verification & PDF Generation](#4-data-science--ml-operations) | 2 minutes |
| **5. Google Colab User** | [Cloud GPU / Jupyter Notebook](#5-google-colab--cloud-gpu-notebooks) | 1 minute |
| **6. Docker / Container User** | [Production Docker Container](#6-docker-containerized-deployment) | 1 minute |

---

## 1. Instant Cloud Web Access (Zero-Install)

If you just want to test, demonstrate, or grade the application without running any code or installing anything on your computer:

👉 **Live Public Web App**: **[https://brestcancerai.streamlit.app](https://brestcancerai.streamlit.app/)**

### How to use it:
1. Open the URL in any modern browser (Chrome, Safari, Firefox, Edge).
2. Use the left sidebar to select one of the 5 pre-loaded clinical scans:
   - *Benign: Fibroadenoma*
   - *Benign: Simple Cyst*
   - *Benign: Normal Glandular Tissue*
   - *Malignant: Invasive Ductal Carcinoma*
   - *Malignant: Lobulated Tumor*
3. Alternatively, drag and drop your own mammogram or histopathology scan (`.jpg`, `.jpeg`, `.png`).
4. View the real-time **Diagnostic Assessment** (Green Benign / Red Malignant badge + Confidence percentage).
5. Inspect the **Grad-CAM Activation Heatmap** on the right highlighting suspicious morphological features.
6. Adjust the **Alpha Blend Slider** or change the OpenCV colormap (`JET`, `VIRIDIS`, `HOT`, `INFERNO`).
7. Click **"Download Superimposed Scan (PNG)"** to save the diagnostic overlay.

---

## 2. One-Click Local Launchers (macOS, Linux & Windows)

The repository provides automated launcher scripts that automatically verify Python, set up the virtual environment, install missing dependencies, generate test data, and launch the web server.

### On macOS / Linux:
Open your terminal in the project folder and run:
```bash
./run.sh
```
*(If prompted for permissions, run `chmod +x run.sh` once first).*

### On Windows (CMD / File Explorer):
Simply **double-click** the `run.bat` file in your project folder, or run:
```cmd
run.bat
```

The script will handle everything and open your browser automatically at `http://localhost:8501`.

---

## 3. Developer / CLI Step-by-Step Setup

If you prefer to manage your environment manually in your terminal or IDE:

### System Prerequisites
- **Python**: Version **3.9, 3.10, 3.11, or 3.12** installed ([python.org/downloads](https://www.python.org/downloads/)).  
  *(Note: Python 3.14 is not recommended yet as TensorFlow has not released pre-compiled wheels for it).*
- **Git**

---

### Step 1: Clone or Open the Repository
```bash
git clone https://github.com/BhuvanExpo/brestcancerai.git
cd brestcancerai
```

---

### Step 2: Create & Activate Virtual Environment

#### On macOS / Linux (zsh / bash):
```bash
python3 -m venv .venv
source .venv/bin/activate
```
*(When activated, you will see `(.venv)` in your terminal prompt).*

#### On Windows (PowerShell):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
*(If script execution is disabled in PowerShell, run `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned` once).*

#### On Windows (Command Prompt `cmd.exe`):
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

---

### Step 3: Install Required Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

> **macOS Note**: If `pyarrow` was ever installed, uninstall it to prevent macOS C++ mutex conflicts with TensorFlow:
> ```bash
> pip uninstall -y pyarrow
> ```

---

### Step 4: Run the Streamlit Application
```bash
streamlit run app.py
```
Open **[http://localhost:8501](http://localhost:8501)** in your web browser.

---

## 4. Data Science & ML Operations

### A. Run the 5-Stage Automated Verification Suite
To verify model weights, hooks, Grad-CAM gradients, and OpenCV alpha blending:
```bash
python test_pipeline.py
```
**Expected Output**:
```text
[Test 1/5] Loading trained model from: models/vgg16_breast_cancer.keras...
  ✓ Target hook layer 'block5_conv3' verified.
  ✓ Custom head architecture verified: GAP -> Dense(128) -> Dropout(0.5) -> Dense(1).
[Test 2/5] Benign Scan Inference:
  Raw Logit: 0.1514 | Benign Confidence: 84.9%
[Test 3/5] Malignant Scan Inference:
  Raw Logit: 0.8993 | Malignant Confidence: 89.9%
[Test 4/5] Computing Grad-CAM heatmap targeting 'block5_conv3'...
  ✓ Heatmap shape: (14, 14) | Min: 0.0000 | Max: 1.0000
[Test 5/5] Testing OpenCV superimposition (alpha=0.4)...
  ✓ Superimposed overlay verified successfully.

==================================================
  ALL 5 PIPELINE VERIFICATION TESTS PASSED!
==================================================
```

---

### B. Generate or Refresh Synthetic Test Scans
Generates 5 realistic sample scans (Fibroadenoma, Simple Cyst, Normal Parenchyma, Invasive Ductal Carcinoma, Lobulated Tumor):
```bash
python generate_sample_data.py
```

---

### C. Retrain the VGG-16 Model
To run the 10-epoch transfer learning training pipeline and update evaluation assets:
```bash
python train.py --epochs 10 --batch_size 16
```
This automatically updates:
- `models/vgg16_breast_cancer.keras`
- `assets/training_history.png`
- `assets/confusion_matrix.png`
- `assets/classification_report.txt`

---

### D. Compile the PDF Technical & Architectural Report
To compile the formal medical publication-style PDF report with embedded charts:
```bash
python generate_pdf_report.py
```
Outputs: `Breast_Cancer_AI_Diagnostic_Platform_Technical_Report.pdf`.

---

## 5. Google Colab / Cloud GPU Notebooks

You can run this full platform on free Google Colab Tesla T4 GPUs:

1. Open a new notebook at [colab.research.google.com](https://colab.research.google.com/).
2. Change runtime to **GPU** (`Runtime` -> `Change runtime type` -> `T4 GPU`).
3. Run the following single code cell:

```python
# 1. Clone repository
!git clone https://github.com/BhuvanExpo/brestcancerai.git
%cd brestcancerai

# 2. Install dependencies & localtunnel
!pip install -r requirements.txt
!npm install -g localtunnel

# 3. Check public IP for tunnel password
!curl ipv4.icanhazip.com

# 4. Launch Streamlit via public tunnel
!streamlit run app.py & npx localtunnel --port 8501
```

Click the generated `localtunnel` link and enter the public IP printed in step 3 to access the app live!

---

## 6. Docker Containerized Deployment

To deploy in any cloud or Kubernetes cluster with zero host dependencies:

### Build Docker Image
```bash
docker build -t breast-cancer-ai:latest .
```

### Run Docker Container
```bash
docker run -d -p 8501:8501 --name breast-cancer-app breast-cancer-ai:latest
```

Open **`http://localhost:8501`** in your browser.

---

## 7. Universal Troubleshooting & FAQ

### Q1: `zsh: command not found: streamlit` (or bash/cmd equivalent)
* **Root Cause**: You opened a new terminal without activating the project virtual environment. `streamlit` is located inside `.venv/bin/streamlit`.
* **Fix**: Run `source .venv/bin/activate` first, OR run directly:
  ```bash
  .venv/bin/streamlit run app.py
  ```

---

### Q2: Streamlit Cloud Error: `No solution found when resolving dependencies for tensorflow (e.g., cp314)`
* **Root Cause**: Streamlit Community Cloud defaulted to Python 3.14, which does not have pre-compiled C-extension wheels for TensorFlow.
* **Fix**:
  1. On your Streamlit Cloud dashboard, delete the existing app deployment.
  2. Click **Create app** -> select `BhuvanExpo/brestcancerai`.
  3. Click **"Advanced settings"** at the bottom.
  4. Select **Python 3.11** from the dropdown menu and click **Deploy**.

---

### Q3: `Fatal Python error: Aborted` (Exit code 134 / SIGABRT) on macOS
* **Root Cause**: A known C++ binary symbol deadlock between `pyarrow` and `tensorflow` on macOS Apple Silicon.
* **Fix**: Uninstall pyarrow (Streamlit functions completely without it using `narwhals`):
  ```bash
  .venv/bin/pip uninstall -y pyarrow
  ```

---

### Q4: `AttributeError: 'list' object has no attribute 'shape'` in `gradcam.py`
* **Status**: **RESOLVED** in commit `a18afed7`.
* **Details**: Keras 3 on Linux handles multi-output functional models by returning predictions in a list. `gradcam.py` now includes universal unpacking and `tf.convert_to_tensor()` guards compatible with both Keras 2 and Keras 3.

---

### Q5: Missing GUI libraries (`libGL.so.1` or `libgthread-2.0.so.0`) on Linux
* **Fix**: Ensure `packages.txt` exists with:
  ```text
  libgl1
  libglib2.0-0
  ```
  And `requirements.txt` specifies `opencv-python-headless>=4.8.0`.

---

## 📞 Support & Repository Access
- **GitHub Repository**: [https://github.com/BhuvanExpo/brestcancerai](https://github.com/BhuvanExpo/brestcancerai)
- **Live Streamlit App**: [https://brestcancerai.streamlit.app](https://brestcancerai.streamlit.app/)
- **Technical PDF Report**: [Breast_Cancer_AI_Diagnostic_Platform_Technical_Report.pdf](https://github.com/BhuvanExpo/brestcancerai/blob/main/Breast_Cancer_AI_Diagnostic_Platform_Technical_Report.pdf)
