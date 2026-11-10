# 🎗️ Universal IDE & System Running Guide
### Breast Cancer AI Diagnostic Platform (VGG-16 & Grad-CAM)
**Tailored for VS Code, Antigravity IDE, Cursor, macOS, Windows & Cloud**

This guide provides **100% copy-ready commands** and step-by-step instructions specifically optimized for developers and researchers using modern AI/code editors (**VS Code**, **Google Antigravity IDE**, **Cursor**, **Windsurf**, or **PyCharm**) on **macOS** and **Windows**.

---

## ⚡ Fastest Way to Run: Press `F5` in Your IDE

The repository includes pre-configured `.vscode/launch.json` configurations. If you have the project open in **VS Code** or **Antigravity IDE**:

1. Open this folder in your IDE (`File` ➔ `Open Folder...`).
2. Press **`F5`** on your keyboard (or click the **Run and Debug** icon `▶` on the left sidebar).
3. Select **`🎗️ Launch Streamlit Diagnostic App (F5)`**.
4. The IDE terminal will launch the app and open **[http://localhost:8501](http://localhost:8501)** in your browser!

---

## 🎯 Quick Navigation by IDE & Operating System

| Platform & Environment | Recommended Guide | Action |
| :--- | :--- | :--- |
| **🍎 Mac + VS Code / Antigravity IDE** | [Section 1: Mac IDE Guide](#1-macos--vs-code--antigravity-ide-guide) | Integrated Terminal / F5 |
| **🪟 Windows + VS Code / Antigravity IDE** | [Section 2: Windows IDE Guide](#2-windows--vs-code--antigravity-ide-guide) | PowerShell / CMD / F5 |
| **🌐 Non-Technical / Evaluator** | [Section 3: 0-Install Cloud Web App](#3-zero-install-instant-web-app) | Browser Link (0 setup) |
| **🧪 ML Operations & PDF Report** | [Section 4: Data Science & Verification](#4-ml-operations-tests-training--pdf-report) | 1-Line Test Commands |
| **☁️ Google Colab (Cloud GPU)** | [Section 5: Google Colab GPU](#5-google-colab-cloud-gpu-one-block-runner) | Free Tesla T4 GPU |
| **🐳 Docker Container** | [Section 6: Production Docker](#6-docker-containerized-deployment) | 1-Line Container Run |
| **🛠️ IDE Troubleshooting & FAQ** | [Section 7: Troubleshooting](#7-universal-ide-troubleshooting--faq) | Fix Common Errors |

---

## 1. macOS + VS Code / Antigravity IDE Guide

Follow these steps if you are running **VS Code**, **Antigravity IDE**, or **Cursor** on **macOS (Apple Silicon M1/M2/M3/M4 or Intel)**:

### Step 1: Open the Project Folder
In your IDE, go to **`File` ➔ `Open Folder...`** and select the `brest cancer detection` folder.

---

### Step 2: Open the Integrated Terminal
Press the shortcut:
```text
Ctrl + `  (backtick)
```
*(Or click top menu: `Terminal` ➔ `New Terminal`).*

---

### Step 3: Select the Python Interpreter (One-Time Setup)
1. Press **`Cmd + Shift + P`** to open the Command Palette.
2. Type `Python: Select Interpreter` and press **Enter**.
3. Choose the project virtual environment:
   ```text
   Enter interpreter path... ➔ ./.venv/bin/python
   ```
*(VS Code will now auto-activate `.venv` every time you open a new terminal).*

---

### Step 4: Run the App (Copy-Ready One-Liners)

#### 🚀 Option A: Direct One-Liner (No activation needed — Easiest):
Paste this directly into the IDE terminal and press **Enter**:
```bash
.venv/bin/streamlit run app.py
```

#### 🚀 Option B: Complete Setup & Launch (First-Time Run):
```bash
python3 -m venv .venv && source .venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt && pip uninstall -y pyarrow 2>/dev/null; streamlit run app.py
```

#### 🚀 Option C: Using the 1-Click Shell Script:
```bash
chmod +x run.sh && ./run.sh
```

Open **[http://localhost:8501](http://localhost:8501)** in your browser!

---

## 2. Windows + VS Code / Antigravity IDE Guide

Follow these steps if you are running **VS Code** or **Antigravity IDE** on **Windows 10 / Windows 11**:

### Step 1: Open the Project Folder
In your IDE, go to **`File` ➔ `Open Folder...`** and select the cloned project folder.

---

### Step 2: Open the Integrated Terminal
Press:
```text
Ctrl + `  (backtick)
```
*(By default, VS Code on Windows opens a **PowerShell** terminal).*

---

### Step 3: Select the Python Interpreter (One-Time Setup)
1. Press **`Ctrl + Shift + P`** to open the Command Palette.
2. Type `Python: Select Interpreter` and press **Enter**.
3. Select:
   ```text
   Enter interpreter path... ➔ .\.venv\Scripts\python.exe
   ```

---

### Step 4: Run the App in Windows Terminal (Copy-Ready)

#### 🪟 If your IDE Terminal is **PowerShell** (Default):

**First-Time Complete Setup (Copy & Paste Entire Line):**
```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1; python -m pip install --upgrade pip; pip install -r requirements.txt; streamlit run app.py
```

**Daily Run (Copy & Paste):**
```powershell
.\.venv\Scripts\Activate.ps1; streamlit run app.py
```

*Or direct execution without activating:*
```powershell
.\.venv\Scripts\streamlit.exe run app.py
```

> **PowerShell Execution Policy Tip**: If PowerShell shows an error saying *"running scripts is disabled on this system"*, run this one-time command:
> ```powershell
> Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
> ```

---

#### 🪟 If your IDE Terminal is **Command Prompt (`cmd.exe`)**:

**First-Time Complete Setup (Copy & Paste Entire Line):**
```cmd
python -m venv .venv && call .venv\Scripts\activate.bat && python -m pip install --upgrade pip && pip install -r requirements.txt && streamlit run app.py
```

**Daily Run (Copy & Paste):**
```cmd
run.bat
```

Open **[http://localhost:8501](http://localhost:8501)** in your browser!

---

## 3. Zero-Install Instant Web App

For evaluators, instructors, or non-technical users who do not want to install any software or open an IDE:

👉 **Live Public Web App**: **[https://brestcancerai.streamlit.app](https://brestcancerai.streamlit.app/)**

- Zero configuration required.
- Choose between 5 pre-loaded clinical scans or upload your own.
- Real-time diagnostic badge (Benign / Malignant) + Confidence percentage.
- Superimposed Grad-CAM activation heatmap with alpha transparency controls.

---

## 4. ML Operations: Tests, Training & PDF Report

Run these copy-ready commands inside your IDE terminal (macOS, Linux, or Windows):

### A. Run 5-Stage Verification Test Suite
Verifies architecture layers, benign scoring, malignant scoring, Grad-CAM gradients, and OpenCV alpha blending:
- **macOS / Linux**:
  ```bash
  .venv/bin/python test_pipeline.py
  ```
- **Windows**:
  ```powershell
  .\.venv\Scripts\python.exe test_pipeline.py
  ```

---

### B. Generate Synthetic Test Scans
Populates `sample_scans/` with labeled scans (Fibroadenoma, Simple Cyst, Invasive Carcinoma, etc.):
- **macOS / Linux**:
  ```bash
  .venv/bin/python generate_sample_data.py
  ```
- **Windows**:
  ```powershell
  .\.venv\Scripts\python.exe generate_sample_data.py
  ```

---

### C. Retrain the VGG-16 Model (10 Epochs)
Executes transfer learning and updates evaluation curves & confusion matrix:
- **macOS / Linux**:
  ```bash
  .venv/bin/python train.py --epochs 10 --batch_size 16
  ```
- **Windows**:
  ```powershell
  .\.venv\Scripts\python.exe train.py --epochs 10 --batch_size 16
  ```

---

### D. Compile the PDF Technical & Architectural Report
Generates the publication-grade medical report:
- **macOS / Linux**:
  ```bash
  .venv/bin/python generate_pdf_report.py
  ```
- **Windows**:
  ```powershell
  .\.venv\Scripts\python.exe generate_pdf_report.py
  ```
*(Generated report: `Breast_Cancer_AI_Diagnostic_Platform_Technical_Report.pdf`)*.

---

## 5. Google Colab (Cloud GPU One-Block Runner)

To run the full app on Google Colab with a free Tesla T4 GPU:

1. Open [colab.research.google.com](https://colab.research.google.com/).
2. Set runtime: `Runtime` ➔ `Change runtime type` ➔ **T4 GPU**.
3. Paste and run this single block:

```python
# 1. Clone & enter repository
!git clone https://github.com/BhuvanExpo/brestcancerai.git
%cd brestcancerai

# 2. Install dependencies & tunnel
!pip install -r requirements.txt
!npm install -g localtunnel
import urllib.request
print("Your Public IP / Tunnel Password:", urllib.request.urlopen('https://ipv4.icanhazip.com').read().decode('utf8').strip())

# 3. Launch Streamlit via localtunnel
!streamlit run app.py & npx localtunnel --port 8501
```

Click the generated `localtunnel` link and enter the printed IP to access the UI.

---

## 6. Docker Containerized Deployment

Run inside your IDE terminal or system console with Docker installed:

```bash
# Build the production image
docker build -t breast-cancer-ai:latest .

# Run container on port 8501
docker run -d -p 8501:8501 --name breast-cancer-app breast-cancer-ai:latest
```

Access the app at **[http://localhost:8501](http://localhost:8501)**.

---

## 7. Universal IDE Troubleshooting & FAQ

### ❓ Q1: `zsh: command not found: streamlit` (macOS) or `'streamlit' is not recognized` (Windows)
* **Root Cause**: The terminal was opened without activating `.venv`. `streamlit` is inside `.venv/bin/` (macOS) or `.venv\Scripts\` (Windows).
* **Fix**:
  - **macOS**: `.venv/bin/streamlit run app.py`
  - **Windows**: `.\.venv\Scripts\streamlit.exe run app.py`

---

### ❓ Q2: Windows PowerShell: `cannot be loaded because running scripts is disabled on this system`
* **Root Cause**: Windows PowerShell restricts running `.ps1` activation scripts by default.
* **Fix (Run once in PowerShell)**:
  ```powershell
  Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
  ```
  Then reactivate: `.\.venv\Scripts\Activate.ps1`.

---

### ❓ Q3: macOS Exit Code 134 / SIGABRT on importing TensorFlow or Streamlit
* **Root Cause**: `pyarrow` causes a C++ mutex deadlock with TensorFlow on macOS Apple Silicon.
* **Fix**:
  ```bash
  .venv/bin/pip uninstall -y pyarrow
  ```

---

### ❓ Q4: Streamlit Cloud Error: `No solution found for tensorflow (cp314)`
* **Root Cause**: Streamlit Community Cloud defaulted to Python 3.14 which lacks pre-compiled TensorFlow wheels.
* **Fix**:
  1. Go to your [Streamlit Cloud Dashboard](https://share.streamlit.io/).
  2. Click `⋮` next to your app ➔ **Delete app**.
  3. Click **Create app** ➔ select `BhuvanExpo/brestcancerai`.
  4. Click **Advanced settings** at the bottom.
  5. Select **Python 3.11** from the dropdown and click **Deploy**.

---

### ❓ Q5: Port 8501 is already in use
If an earlier session of Streamlit is still running:
- **macOS**: `lsof -ti:8501 | xargs kill -9`
- **Windows**: `Stop-Process -Id (Get-NetTCPConnection -LocalPort 8501).OwningProcess -Force`
- Or run on an alternative port:
  ```bash
  streamlit run app.py --server.port 8502
  ```

---

## 📁 Repository Quick Links
- **GitHub Repository**: [https://github.com/BhuvanExpo/brestcancerai](https://github.com/BhuvanExpo/brestcancerai)
- **Live Streamlit App**: [https://brestcancerai.streamlit.app](https://brestcancerai.streamlit.app/)
- **Technical PDF Report**: [Breast_Cancer_AI_Diagnostic_Platform_Technical_Report.pdf](https://github.com/BhuvanExpo/brestcancerai/blob/main/Breast_Cancer_AI_Diagnostic_Platform_Technical_Report.pdf)
