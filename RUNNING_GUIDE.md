# 🎗️ Universal Running & Deployment Guide
# 🎗️ Universal IDE & System Running Guide
### Breast Cancer AI Diagnostic Platform (VGG-16 & Grad-CAM)
**Tailored for VS Code, Antigravity IDE, Cursor, macOS, Windows & Cloud**

This guide provides **100% copy-ready commands** for every operating system and user profile. Copy any command block below and paste it directly into your terminal or browser.
This guide provides **100% copy-ready commands** and step-by-step instructions specifically optimized for developers and researchers using modern AI/code editors (**VS Code**, **Google Antigravity IDE**, **Cursor**, **Windsurf**, or **PyCharm**) on **macOS** and **Windows**.

---

## ⚡ Quick Copy-Paste One-Liners (Cheat Sheet)
## ⚡ Fastest Way to Run: Press `F5` in Your IDE

Click the copy button on any block below and paste directly into your terminal:
The repository includes pre-configured `.vscode/launch.json` configurations. If you have the project open in **VS Code** or **Antigravity IDE**:

### 🍎 macOS / 🐧 Linux (Run Instantly)
```bash
./run.sh
```
*Or without activation (direct one-liner):*
```bash
.venv/bin/streamlit run app.py
```
1. Open this folder in your IDE (`File` ➔ `Open Folder...`).
2. Press **`F5`** on your keyboard (or click the **Run and Debug** icon `▶` on the left sidebar).
3. Select **`🎗️ Launch Streamlit Diagnostic App (F5)`**.
4. The IDE terminal will launch the app and open **[http://localhost:8501](http://localhost:8501)** in your browser!

### 🪟 Windows (Double-Click or Command Prompt)
```cmd
run.bat
```
---

### 🧪 Run Verification Test Suite (All 5 Checks)
```bash
.venv/bin/python test_pipeline.py
```
## 🎯 Quick Navigation by IDE & Operating System

| Platform & Environment | Recommended Guide | Action |
| :--- | :--- | :--- |
| **🍎 Mac + VS Code / Antigravity IDE** | [Section 1: Mac IDE Guide](#1-macos--vs-code--antigravity-ide-guide) | Integrated Terminal / F5 |
| **🪟 Windows + VS Code / Antigravity IDE** | [Section 2: Windows IDE Guide](#2-windows--vs-code--antigravity-ide-guide) | PowerShell / CMD / F5 |
| **🌐 Non-Technical / Evaluator** | [Section 3: 0-Install Cloud Web App](#3-zero-install-instant-web-app) | Browser Link (0 setup) |
| **🧪 ML Operations & Verification** | [Section 4: Data Science & Verification](#4-ml-operations-tests--training) | 1-Line Test Commands |
| **☁️ Google Colab (Cloud GPU)** | [Section 5: Google Colab GPU](#5-google-colab-cloud-gpu-one-block-runner) | Free Tesla T4 GPU |
| **🐳 Docker Container** | [Section 6: Production Docker](#6-docker-containerized-deployment) | 1-Line Container Run |
| **🛠️ IDE Troubleshooting & FAQ** | [Section 7: Troubleshooting](#7-universal-ide-troubleshooting--faq) | Fix Common Errors |

### 🌐 Instant 0-Install Cloud Web App (No Terminal Required)
👉 **[https://brestcancerai.streamlit.app](https://brestcancerai.streamlit.app/)**

---

## 🎯 Profile Navigation
## 1. macOS + VS Code / Antigravity IDE Guide

| User Profile | Running Method | Time |
| :--- | :--- | :--- |
| **1. Non-Technical / Evaluator** | [Instant Cloud Web Access (Zero-Install)](#1-instant-cloud-web-access-zero-install) | 0 seconds |
| **2. One-Click Local User** | [Automated 1-Click Launchers (`run.sh` / `run.bat`)](#2-one-click-local-launchers-macos-linux--windows) | 5 seconds |
| **3. Developer / CLI User** | [Copy-Ready Step-by-Step Terminal Setup](#3-developer--cli-step-by-step-setup) | 30 seconds |
| **4. ML Engineer / Researcher** | [Training & Pipeline Verification](#4-data-science--ml-operations) | 1 minute |
| **5. Google Colab User** | [Cloud GPU / Single Notebook Cell](#5-google-colab--cloud-gpu-notebooks) | 1 minute |
| **6. Docker / Container User** | [Production Docker Commands](#6-docker-containerized-deployment) | 1 minute |
Follow these steps if you are running **VS Code**, **Antigravity IDE**, or **Cursor** on **macOS (Apple Silicon M1/M2/M3/M4 or Intel)**:

### Step 1: Open the Project Folder
In your IDE, go to **`File` ➔ `Open Folder...`** and select the `brest cancer detection` folder.

---

## 1. Instant Cloud Web Access (Zero-Install)
### Step 2: Open the Integrated Terminal
Press the shortcut:
```text
Ctrl + `  (backtick)
```
*(Or click top menu: `Terminal` ➔ `New Terminal`).*

If you just want to test, demonstrate, or grade the application without installing anything:
---

👉 **Live Web App**: **[https://brestcancerai.streamlit.app](https://brestcancerai.streamlit.app/)**
### Step 3: Select the Python Interpreter (One-Time Setup)
1. Press **`Cmd + Shift + P`** to open the Command Palette.
2. Type `Python: Select Interpreter` and press **Enter**.
3. Choose the project virtual environment:
   ```text
   Enter interpreter path... ➔ ./.venv/bin/python
   ```
*(VS Code will now auto-activate `.venv` every time you open a new terminal).*

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
### Step 4: Run the App (Copy-Ready One-Liners)

Automated scripts that check Python, create `.venv`, install dependencies, and start Streamlit in a single click:
#### 🚀 Option A: Direct One-Liner (No activation needed — Easiest):
Paste this directly into the IDE terminal and press **Enter**:
```bash
.venv/bin/streamlit run app.py
```

### 🍎 On macOS / 🐧 Linux:
Open Terminal in the project directory and paste:
#### 🚀 Option B: Complete Setup & Launch (First-Time Run):
```bash
chmod +x run.sh && ./run.sh
python3 -m venv .venv && source .venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt && pip uninstall -y pyarrow 2>/dev/null; streamlit run app.py
```

### 🪟 On Windows:
Double-click `run.bat` in File Explorer, or paste into Command Prompt (`cmd.exe`):
```cmd
run.bat
#### 🚀 Option C: Using the 1-Click Shell Script:
```bash
chmod +x run.sh && ./run.sh
```

Your default browser will automatically open **[http://localhost:8501](http://localhost:8501)**.
Open **[http://localhost:8501](http://localhost:8501)** in your browser!

---

## 3. Developer / CLI Step-by-Step Setup
## 2. Windows + VS Code / Antigravity IDE Guide

If you prefer to run commands manually in your terminal or IDE:
Follow these steps if you are running **VS Code** or **Antigravity IDE** on **Windows 10 / Windows 11**:

### 🍎 macOS & 🐧 Linux
### Step 1: Open the Project Folder
In your IDE, go to **`File` ➔ `Open Folder...`** and select the cloned project folder.

#### First-Time Complete Setup (Copy-Ready Single Command):
```bash
python3 -m venv .venv && source .venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt && pip uninstall -y pyarrow 2>/dev/null; streamlit run app.py
```
---

#### Daily Running (Copy-Ready Single Command):
```bash
source .venv/bin/activate && streamlit run app.py
### Step 2: Open the Integrated Terminal
Press:
```text
Ctrl + `  (backtick)
```
*(By default, VS Code on Windows opens a **PowerShell** terminal).*

*Or direct execution without activating the environment:*
```bash
.venv/bin/streamlit run app.py
```
---

### Step 3: Select the Python Interpreter (One-Time Setup)
1. Press **`Ctrl + Shift + P`** to open the Command Palette.
2. Type `Python: Select Interpreter` and press **Enter**.
3. Select:
   ```text
   Enter interpreter path... ➔ .\.venv\Scripts\python.exe
   ```

---

### 🪟 Windows (PowerShell)
### Step 4: Run the App in Windows Terminal (Copy-Ready)

#### First-Time Complete Setup (Copy-Ready Single Command):
#### 🪟 If your IDE Terminal is **PowerShell** (Default):

**First-Time Complete Setup (Copy & Paste Entire Line):**
```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1; python -m pip install --upgrade pip; pip install -r requirements.txt; streamlit run app.py
```
*(Note: If PowerShell says "running scripts is disabled", run `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned` once).*

#### Daily Running (Copy-Ready Single Command):
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

### 🪟 Windows (Command Prompt `cmd.exe`)
#### 🪟 If your IDE Terminal is **Command Prompt (`cmd.exe`)**:

#### First-Time Complete Setup (Copy-Ready Single Command):
**First-Time Complete Setup (Copy & Paste Entire Line):**
```cmd
python -m venv .venv && call .venv\Scripts\activate.bat && python -m pip install --upgrade pip && pip install -r requirements.txt && streamlit run app.py
```

#### Daily Running (Copy-Ready Single Command):
**Daily Run (Copy & Paste):**
```cmd
call .venv\Scripts\activate.bat && streamlit run app.py
run.bat
```

Open **[http://localhost:8501](http://localhost:8501)** in your browser!

---

## 4. Data Science & ML Operations
## 3. Zero-Install Instant Web App

All commands below are copy-ready:
For evaluators, instructors, or non-technical users who do not want to install any software or open an IDE:

### A. Run 5-Stage Verification Suite
Tests model loading, layer hooks, benign/malignant inference, Grad-CAM gradients, and OpenCV overlays:
```bash
.venv/bin/python test_pipeline.py
```
*(On Windows: `.venv\Scripts\python.exe test_pipeline.py`)*
👉 **Live Public Web App**: **[https://brestcancerai.streamlit.app](https://brestcancerai.streamlit.app/)**

- Zero configuration required.
- Choose between 5 pre-loaded clinical scans or upload your own.
- Real-time diagnostic badge (Benign / Malignant) + Confidence percentage.
- Superimposed Grad-CAM activation heatmap with alpha transparency controls.

---

### B. Generate Synthetic Clinical Scans
Generates 5 labeled clinical scans in `sample_scans/`:
```bash
.venv/bin/python generate_sample_data.py
```
*(On Windows: `.venv\Scripts\python.exe generate_sample_data.py`)*
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

### C. Retrain the VGG-16 Model
Executes 10-epoch transfer learning, updates weights, and regenerates all evaluation curves:
```bash
.venv/bin/python train.py --epochs 10 --batch_size 16
```
*(On Windows: `.venv\Scripts\python.exe train.py --epochs 10 --batch_size 16`)*
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

Outputs updated:
- `models/vgg16_breast_cancer.keras`
- `assets/training_history.png`
- `assets/confusion_matrix.png`
- `assets/classification_report.txt`
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

## 5. Google Colab (Cloud GPU One-Block Runner)

Copy and paste this single block into a blank Google Colab code cell:
To run the full app on Google Colab with a free Tesla T4 GPU:

1. Open [colab.research.google.com](https://colab.research.google.com/).
2. Set runtime: `Runtime` ➔ `Change runtime type` ➔ **T4 GPU**.
3. Paste and run this single block:

```python
# Copy and run this entire block in Google Colab (Set Runtime -> GPU -> T4)
# 1. Clone & enter repository
!git clone https://github.com/BhuvanExpo/brestcancerai.git
%cd brestcancerai

# 2. Install dependencies & tunnel
!pip install -r requirements.txt
!npm install -g localtunnel
import urllib.request
print("Your Tunnel Password / Public IP is:", urllib.request.urlopen('https://ipv4.icanhazip.com').read().decode('utf8').strip())
print("Your Public IP / Tunnel Password:", urllib.request.urlopen('https://ipv4.icanhazip.com').read().decode('utf8').strip())

# 3. Launch Streamlit via localtunnel
!streamlit run app.py & npx localtunnel --port 8501
```

Click the generated `localtunnel` link and paste the printed IP address to open the app on cloud GPU!
Click the generated `localtunnel` link and enter the printed IP to access the UI.

---

## 6. Docker Containerized Deployment

Run these copy-ready commands in any environment with Docker installed:
Run inside your IDE terminal or system console with Docker installed:

### Build the Docker Image:
```bash
# Build the production image
docker build -t breast-cancer-ai:latest .
```

### Run the Container:
```bash
# Run container on port 8501
docker run -d -p 8501:8501 --name breast-cancer-app breast-cancer-ai:latest
```

### Stop the Container:
```bash
docker stop breast-cancer-app && docker rm breast-cancer-app
```
Access the app at **[http://localhost:8501](http://localhost:8501)**.

Access the app at **`http://localhost:8501`**.

---

## 7. Universal Troubleshooting & FAQ
## 7. Universal IDE Troubleshooting & FAQ

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
### ❓ Q1: `zsh: command not found: streamlit` (macOS) or `'streamlit' is not recognized` (Windows)
* **Root Cause**: The terminal was opened without activating `.venv`. `streamlit` is inside `.venv/bin/` (macOS) or `.venv\Scripts\` (Windows).
* **Fix**:
  - **macOS**: `.venv/bin/streamlit run app.py`
  - **Windows**: `.\.venv\Scripts\streamlit.exe run app.py`

---

### Q2: Streamlit Cloud Error: `No solution found when resolving dependencies for tensorflow (e.g. cp314)`
* **Cause**: Streamlit Community Cloud defaulted to experimental Python 3.14.
* **Instant Fix**:
  1. Go to your [Streamlit Cloud Dashboard](https://share.streamlit.io/).
  2. Click `⋮` next to your app -> **Delete app**.
  3. Click **Create app** -> select `BhuvanExpo/brestcancerai`.
  4. Click **"Advanced settings"** at the bottom.
  5. Select **Python 3.11** from the dropdown and click **Deploy**.
### ❓ Q2: Windows PowerShell: `cannot be loaded because running scripts is disabled on this system`
* **Root Cause**: Windows PowerShell restricts running `.ps1` activation scripts by default.
* **Fix (Run once in PowerShell)**:
  ```powershell
  Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
  ```
  Then reactivate: `.\.venv\Scripts\Activate.ps1`.

---

### Q3: `Fatal Python error: Aborted` (Exit code 134 / SIGABRT) on macOS
* **Cause**: `pyarrow` C++ binary mutex collision with TensorFlow on macOS Apple Silicon.
* **Instant Fix (Copy & Paste)**:
### ❓ Q3: macOS Exit Code 134 / SIGABRT on importing TensorFlow or Streamlit
* **Root Cause**: `pyarrow` causes a C++ mutex deadlock with TensorFlow on macOS Apple Silicon.
* **Fix**:
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
### ❓ Q4: Streamlit Cloud Error: `No solution found for tensorflow (cp314)`
* **Root Cause**: Streamlit Community Cloud defaulted to Python 3.14 which lacks pre-compiled TensorFlow wheels.
* **Fix**:
  1. Go to your [Streamlit Cloud Dashboard](https://share.streamlit.io/).
  2. Click `⋮` next to your app ➔ **Delete app**.
  3. Click **Create app** ➔ select `BhuvanExpo/brestcancerai`.
  4. Click **Advanced settings** at the bottom.
  5. Select **Python 3.11** from the dropdown and click **Deploy**.

---

### Q5: How to Stop the Local Server
* In the terminal running Streamlit, press:
  ```text
  Ctrl + C
### ❓ Q5: Port 8501 is already in use
If an earlier session of Streamlit is still running:
- **macOS**: `lsof -ti:8501 | xargs kill -9`
- **Windows**: `Stop-Process -Id (Get-NetTCPConnection -LocalPort 8501).OwningProcess -Force`
- Or run on an alternative port:
  ```bash
  streamlit run app.py --server.port 8502
  ```

---

## 📁 Repository Links
## 📁 Repository Quick Links
- **GitHub Repository**: [https://github.com/BhuvanExpo/brestcancerai](https://github.com/BhuvanExpo/brestcancerai)
- **Live Streamlit App**: [https://brestcancerai.streamlit.app](https://brestcancerai.streamlit.app/)
