# 🎗️ Universal Running & Deployment Guide
### Breast Cancer AI Diagnostic Platform (VGG-16 & Grad-CAM)

This guide provides **100% copy-ready commands** for every operating system and user profile. Copy any command block below and paste it directly into your terminal or browser.

---

## ⚡ Quick Copy-Paste One-Liners (Cheat Sheet)

Click the copy button on any block below and paste directly into your terminal:

### 🍎 macOS / 🐧 Linux (Run Instantly)
```bash
./run.sh
```
*Or without activation (direct one-liner):*
```bash
.venv/bin/streamlit run app.py
```

### 🪟 Windows (Double-Click or Command Prompt)
```cmd
run.bat
```

### 🧪 Run Verification Test Suite (All 5 Checks)
```bash
.venv/bin/python test_pipeline.py
```

### 📄 Re-generate the PDF Technical Report
```bash
.venv/bin/python generate_pdf_report.py
```

### 🌐 Instant 0-Install Cloud Web App (No Terminal Required)
👉 **[https://brestcancerai.streamlit.app](https://brestcancerai.streamlit.app/)**

---

## 🎯 Profile Navigation

| User Profile | Running Method | Time |
| :--- | :--- | :--- |
| **1. Non-Technical / Evaluator** | [Instant Cloud Web Access (Zero-Install)](#1-instant-cloud-web-access-zero-install) | 0 seconds |
| **2. One-Click Local User** | [Automated 1-Click Launchers (`run.sh` / `run.bat`)](#2-one-click-local-launchers-macos-linux--windows) | 5 seconds |
| **3. Developer / CLI User** | [Copy-Ready Step-by-Step Terminal Setup](#3-developer--cli-step-by-step-setup) | 30 seconds |
| **4. ML Engineer / Researcher** | [Training, Verification & PDF Report Generation](#4-data-science--ml-operations) | 1 minute |
| **5. Google Colab User** | [Cloud GPU / Single Notebook Cell](#5-google-colab--cloud-gpu-notebooks) | 1 minute |
| **6. Docker / Container User** | [Production Docker Commands](#6-docker-containerized-deployment) | 1 minute |

---

## 1. Instant Cloud Web Access (Zero-Install)

If you just want to test, demonstrate, or grade the application without installing anything:

👉 **Live Web App**: **[https://brestcancerai.streamlit.app](https://brestcancerai.streamlit.app/)**

### How to use it in your browser:
1. Open [https://brestcancerai.streamlit.app](https://brestcancerai.streamlit.app/) in any web browser.
2. In the left sidebar under **"Quick Test Sample Scans"**, choose a pre-loaded scan:
   - `Benign: Fibroadenoma`
   - `Benign: Simple Cyst`
   - `Benign: Normal Glandular Tissue`
   - `Malignant: Invasive Ductal Carcinoma`
   - `Malignant: Lobulated Tumor`
3. Or drag and drop any breast mammogram / histopathology image (`.jpg`, `.jpeg`, `.png`).
4. Review the **Clinical Assessment** badge (Green for Benign / Red for Malignant) and confidence probability bars.
5. Inspect the **Grad-CAM Heatmap** showing which tissue patterns triggered the neural diagnosis.
6. Adjust the **Heatmap Blend Slider** ($0.1 \le \alpha \le 0.9$) or switch the OpenCV colormap (`JET`, `VIRIDIS`, `HOT`, `INFERNO`).
7. Click **"Download Superimposed Scan (PNG)"** to save the diagnostic output.

---

## 2. One-Click Local Launchers (macOS, Linux & Windows)

Automated scripts that check Python, create `.venv`, install dependencies, and start Streamlit in a single click:

### 🍎 On macOS / 🐧 Linux:
Open Terminal in the project directory and paste:
```bash
chmod +x run.sh && ./run.sh
```

### 🪟 On Windows:
Double-click `run.bat` in File Explorer, or paste into Command Prompt (`cmd.exe`):
```cmd
run.bat
```

Your default browser will automatically open **[http://localhost:8501](http://localhost:8501)**.

---

## 3. Developer / CLI Step-by-Step Setup

If you prefer to run commands manually in your terminal or IDE:

### 🍎 macOS & 🐧 Linux

#### First-Time Complete Setup (Copy-Ready Single Command):
```bash
python3 -m venv .venv && source .venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt && pip uninstall -y pyarrow 2>/dev/null; streamlit run app.py
```

#### Daily Running (Copy-Ready Single Command):
```bash
source .venv/bin/activate && streamlit run app.py
```

*Or direct execution without activating the environment:*
```bash
.venv/bin/streamlit run app.py
```

---

### 🪟 Windows (PowerShell)

#### First-Time Complete Setup (Copy-Ready Single Command):
```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1; python -m pip install --upgrade pip; pip install -r requirements.txt; streamlit run app.py
```
*(Note: If PowerShell says "running scripts is disabled", run `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned` once).*

#### Daily Running (Copy-Ready Single Command):
```powershell
.\.venv\Scripts\Activate.ps1; streamlit run app.py
```

---

### 🪟 Windows (Command Prompt `cmd.exe`)

#### First-Time Complete Setup (Copy-Ready Single Command):
```cmd
python -m venv .venv && call .venv\Scripts\activate.bat && python -m pip install --upgrade pip && pip install -r requirements.txt && streamlit run app.py
```

#### Daily Running (Copy-Ready Single Command):
```cmd
call .venv\Scripts\activate.bat && streamlit run app.py
```

---

## 4. Data Science & ML Operations

All commands below are copy-ready:

### A. Run 5-Stage Verification Suite
Tests model loading, layer hooks, benign/malignant inference, Grad-CAM gradients, and OpenCV overlays:
```bash
.venv/bin/python test_pipeline.py
```
*(On Windows: `.venv\Scripts\python.exe test_pipeline.py`)*

---

### B. Generate Synthetic Clinical Scans
Generates 5 labeled clinical scans in `sample_scans/`:
```bash
.venv/bin/python generate_sample_data.py
```
*(On Windows: `.venv\Scripts\python.exe generate_sample_data.py`)*

---

### C. Retrain the VGG-16 Model
Executes 10-epoch transfer learning, updates weights, and regenerates all evaluation curves:
```bash
.venv/bin/python train.py --epochs 10 --batch_size 16
```
*(On Windows: `.venv\Scripts\python.exe train.py --epochs 10 --batch_size 16`)*

Outputs updated:
- `models/vgg16_breast_cancer.keras`
- `assets/training_history.png`
- `assets/confusion_matrix.png`
- `assets/classification_report.txt`

---

### D. Compile Formal PDF Report
Generates the medical-grade publication report with embedded figures and tables:
```bash
.venv/bin/python generate_pdf_report.py
```
*(On Windows: `.venv\Scripts\python.exe generate_pdf_report.py`)*

Outputs: `Breast_Cancer_AI_Diagnostic_Platform_Technical_Report.pdf` (465 KB).

---

## 5. Google Colab / Cloud GPU Notebooks

Copy and paste this single block into a blank Google Colab code cell:

```python
# Copy and run this entire block in Google Colab (Set Runtime -> GPU -> T4)
!git clone https://github.com/BhuvanExpo/brestcancerai.git
%cd brestcancerai
!pip install -r requirements.txt
!npm install -g localtunnel
import urllib.request
print("Your Tunnel Password / Public IP is:", urllib.request.urlopen('https://ipv4.icanhazip.com').read().decode('utf8').strip())
!streamlit run app.py & npx localtunnel --port 8501
```

Click the generated `localtunnel` link and paste the printed IP address to open the app on cloud GPU!

---

## 6. Docker Containerized Deployment

Run these copy-ready commands in any environment with Docker installed:

### Build the Docker Image:
```bash
docker build -t breast-cancer-ai:latest .
```

### Run the Container:
```bash
docker run -d -p 8501:8501 --name breast-cancer-app breast-cancer-ai:latest
```

### Stop the Container:
```bash
docker stop breast-cancer-app && docker rm breast-cancer-app
```

Access the app at **`http://localhost:8501`**.

---

## 7. Universal Troubleshooting & FAQ

### Q1: `zsh: command not found: streamlit` (or bash/cmd equivalent)
* **Cause**: Your terminal doesn't have the virtual environment activated.
* **Instant Fix (Copy & Paste)**:
  ```bash
  .venv/bin/streamlit run app.py
  ```
  *Or activate first:*
  ```bash
  source .venv/bin/activate && streamlit run app.py
  ```

---

### Q2: Streamlit Cloud Error: `No solution found when resolving dependencies for tensorflow (e.g. cp314)`
* **Cause**: Streamlit Community Cloud defaulted to experimental Python 3.14.
* **Instant Fix**:
  1. Go to your [Streamlit Cloud Dashboard](https://share.streamlit.io/).
  2. Click `⋮` next to your app -> **Delete app**.
  3. Click **Create app** -> select `BhuvanExpo/brestcancerai`.
  4. Click **"Advanced settings"** at the bottom.
  5. Select **Python 3.11** from the dropdown and click **Deploy**.

---

### Q3: `Fatal Python error: Aborted` (Exit code 134 / SIGABRT) on macOS
* **Cause**: `pyarrow` C++ binary mutex collision with TensorFlow on macOS Apple Silicon.
* **Instant Fix (Copy & Paste)**:
  ```bash
  .venv/bin/pip uninstall -y pyarrow
  ```

---

### Q4: Missing GUI libraries (`libGL.so.1` or `libgthread-2.0.so.0`) on Linux
* **Fix**: Run:
  ```bash
  sudo apt-get update && sudo apt-get install -y libgl1 libglib2.0-0
  ```
  *(On Streamlit Cloud, this is handled automatically by [`packages.txt`](file:///Users/bhuvangm/Dev/brest%20cancer%20detection/packages.txt))*.

---

### Q5: How to Stop the Local Server
* In the terminal running Streamlit, press:
  ```text
  Ctrl + C
  ```

---

## 📁 Repository Links
- **GitHub Repository**: [https://github.com/BhuvanExpo/brestcancerai](https://github.com/BhuvanExpo/brestcancerai)
- **Live Streamlit App**: [https://brestcancerai.streamlit.app](https://brestcancerai.streamlit.app/)
- **Technical PDF Report**: [Breast_Cancer_AI_Diagnostic_Platform_Technical_Report.pdf](https://github.com/BhuvanExpo/brestcancerai/blob/main/Breast_Cancer_AI_Diagnostic_Platform_Technical_Report.pdf)
