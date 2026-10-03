# ScamShield AI

> **Detect it. Understand it. Practice it. Prevent it.**

[![HackNowa Global Hackathon 2026](https://img.shields.io/badge/HackNowa-Hackathon%202026-blue?style=for-the-badge)](https://hacknowa.devpost.com/)
[![Track: Digital Safety & Cybersecurity](https://img.shields.io/badge/Track-Digital%20Safety%20%26%20Cybersecurity-red?style=for-the-badge)](#)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg?style=for-the-badge&logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688.svg?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![Next.js 16](https://img.shields.io/badge/Next.js-16%20App%20Router-black?style=for-the-badge&logo=next.js)](https://nextjs.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

An AI-powered cybersecurity assistant that helps ordinary users detect scams, understand **why** something is suspicious, know **what to do** next, warn their family members, and **practice** spotting scams before they strike.

---

## 📌 Problem & Motivation

Cyber fraud has evolved into rapid, psychologically coercive social engineering:
- **Banking KYC Fraud**: Urgent threats claiming accounts will be blocked today.
- **Micro-Payment Lures**: Small ₹25 courier redelivery fees designed to harvest card details and OTPs.
- **Digital Arrest Extortion**: Impersonation of police, CBI, or customs over video calls.
- **Task & Job Scams**: Work-from-home lures paying thousands for liking videos.

Ordinary users do not need complex threat intelligence feeds. They need clear answers to three essential questions:
1. **Is this suspicious?**
2. **Why did you flag this?**
3. **What concrete steps should I take right now?**

---

## 🛡️ The ScamShield Experience

```
INPUT (Message, Link, Screenshot, QR, Voice)
  ↓
ANALYSIS (Rules + Lexical Heuristics + ML Feature Vector + AI Semantics)
  ↓
CALIBRATED RISK SCORE (Safe / Suspicious / High Risk)
  ↓
TRUSTLENS EVIDENCE (01 Urgency, 02 Impersonation, 03 Domain Mismatch...)
  ↓
ACTION PLAN (Protective Checklist + Official Cybercrime Portal 1930)
  ↓
FAMILY GUARDIAN & SCAM DOJO (Shareable Alerts & Gamified Practice)
```

---

## 🚀 Key Features

- **Multimodal Detection**:
  - 💬 **Message / SMS**: Detects coercive threats, artificial urgency, and OTP solicitation.
  - 🔗 **URL Inspection**: Deep lexical analysis, Shannon entropy, Punycode detection, and brand mismatch verification.
  - 🖼️ **Screenshot OCR**: Local, high-speed text extraction via RapidOCR (ONNX).
  - 📱 **QR Code Decoder**: OpenCV matrix decoding without automatically navigating to suspicious destinations.
  - 🎙️ **Voice / Transcript**: Acoustic metadata extraction with transcript-assisted voice analysis fallback.
- **AI & Rule Architecture**:
  - **Deterministic Rule Engine**: Transparent heuristics returning structured, explainable evidence.
  - **Machine Learning Layer**: scikit-learn `RandomForestClassifier` trained on a 26-dimensional combined feature vector.
  - **Semantic AI**: Optional LLM semantic analysis with deterministic local fallback when no external API key is configured.
- **TrustLens Evidence Engine**: Numbered evidence cards highlighting exact trigger words in user text.
- **Family Guardian**: 1-click generation of shareable warning cards formatted for WhatsApp and SMS family groups.
- **🥋 Scam Dojo**: Signature gamified training gym featuring 6 levels, 12 scenarios, streaks, and cybersecurity rank progression.
- **Vernacular Localization**: Simple, jargon-free explanations in **English, தமிழ் (Tamil), हिन्दी (Hindi), తెలుగు (Telugu), മലയാളം (Malayalam), and ಕನ್ನಡ (Kannada)**.
- **Privacy & Safety First**: Input length limits, automatic credit card & OTP redaction, and no remote database retention.

---

## 📊 Prototype Evaluation & Benchmark Results

> **Scientific Integrity Notice:**  
> On the included 70-sample prototype evaluation dataset, the multi-signal pipeline achieved **92.86% out-of-fold cross-validation accuracy**. All benchmark metrics reported below are generated directly from the included reproducible evaluation pipeline (`python evaluation/evaluate.py`). **The evaluation uses strict 5-Fold Stratified Cross-Validation with out-of-fold holdout predictions to guarantee ZERO data leakage.**

### Prototype Dataset Details & Limitations
- **Total Samples:** 70 samples (40 URLs, 30 Messages).
- **Class Balance:** Perfectly balanced 50% scam (35) / 50% legitimate (35).
- **Data Source:** Manually curated representative samples mirroring active threat patterns in India and Asia-Pacific.
- **Scope:** Intended to validate prototype pipeline components; does not claim internet-scale wild-web detection without continuous retraining.

| Subsystem Evaluated | Accuracy | Precision | Recall | F1-Score | Measured Latency |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **ML Classifier Alone (5-Fold CV)** | 84.29% | 92.86% | 74.29% | 0.8254 | 6.62 ms / sample |
| **URL Subsystem (40 Out-of-Fold Samples)** | 100.00% | 100.00% | 100.00% | 1.0000 | < 1 ms |
| **Message Subsystem (30 Out-of-Fold Samples)** | 83.33% | 91.67% | 73.33% | 0.8148 | < 1 ms |
| **Combined Multi-Signal System (70 Samples Out-of-Fold)** | **92.86%** | **96.88%** | **88.57%** | **0.9254** | **0.72 ms / request** |

Run the benchmark locally:
```bash
python evaluation/evaluate.py
```

---

## 🛠️ Technology Stack

- **Frontend**: Next.js 16 (App Router), React 19, TypeScript, Tailwind CSS, Lucide React, Canvas Confetti.
- **Backend**: Python 3.10+, FastAPI, Pydantic v2, Uvicorn, Httpx.
- **Machine Learning**: scikit-learn (`RandomForestClassifier`), XGBoost, joblib, NumPy, Pandas.
- **Computer Vision**: OpenCV (`cv2.QRCodeDetector`), RapidOCR (ONNX Runtime), Pillow.
- **Testing**: Pytest (100% automated test suite).

---

## ⚡ Quickstart & Running Locally

### 1. Prerequisites
- Node.js 18+ and npm
- Python 3.10+ (Tested on Python 3.14 on Windows)

### 2. Backend Setup
From the project root:

```bash
# Optional: create and activate virtual environment
python -m venv venv
# Windows:
.\venv\Scripts\Activate.ps1
# Mac/Linux:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run backend tests
python -m pytest tests -v

# Run reproducible evaluation benchmark
python evaluation/evaluate.py

# Start FastAPI backend server (Runs on http://127.0.0.1:8000)
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

Backend API Swagger Documentation is accessible at `http://127.0.0.1:8000/docs`.  
Health check: `http://127.0.0.1:8000/api/health`.

### 3. Frontend Setup
In a new terminal:

```bash
cd frontend

# Install frontend dependencies
npm install

# Start development server (Runs on http://localhost:3000)
npm run dev

# Or build production bundle
npm run build
npm run start
```

Open `http://localhost:3000` in your web browser.

---

## 🚢 Public Deployment & Containerization

ScamShield AI is pre-configured and verified for instant 1-click cloud deployment:

- **Docker Container**: Build and run the self-contained backend image:
  ```bash
  docker build -t scamshield-backend .
  docker run -p 8000:8000 -e PORT=8000 scamshield-backend
  ```
- **Render (Full-Stack Blueprint)**: Use `render.yaml` to spin up both the FastAPI backend and Next.js frontend services.
- **Vercel (Frontend)**: Deploy the Next.js frontend with `frontend/vercel.json` and set `NEXT_PUBLIC_API_URL` to your production backend URL.

---

## 📑 Hardening & Hackathon Documentation

- [📋 Final Audit Report](docs/final-audit.md) — Comprehensive feature-by-feature verification matrix.
- [🧪 Scientific Evaluation](docs/evaluation.md) — Leak-free 5-fold cross-validation methodology and metrics.
- [📝 Official Submission Material](docs/submission.md) — Executive summary, 100/250/500-word descriptions, and innovation impact.
- [✅ Final Verification Report](docs/final-verification.md) — Build, backend, frontend, and security verification results.
- [🎬 Hackathon Demo Script](docs/demo-script.md) — 2.5-minute structured presentation script.

## ⚙️ Environment Variables

Copy `.env.example` to `.env` to customize settings:

```ini
PROJECT_NAME="ScamShield AI"
ENVIRONMENT="production"
DEBUG=false
API_PREFIX="/api"

# Optional AI LLM Provider ("openai", "gemini", or "local")
# If left empty, the application runs entirely on local deterministic rules and scikit-learn models.
LLM_PROVIDER="local"
OPENAI_API_KEY=""
GEMINI_API_KEY=""
LLM_MODEL="gpt-4o-mini"

# Classification Thresholds
SAFE_THRESHOLD=0.35
SUSPICIOUS_THRESHOLD=0.70
```

---

## 🌐 API Endpoints Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/health` | Comprehensive system health check & active subsystem statuses |
| `GET` | `/api/analyze/demo-cases` | Curated simulated judging demo cases |
| `POST` | `/api/analyze/text` | Full multi-signal analysis of message text |
| `POST` | `/api/analyze/url` | Deep structural and brand-spoof analysis of URLs |
| `POST` | `/api/analyze/image` | RapidOCR text extraction and scam inspection from screenshots |
| `POST` | `/api/analyze/qr` | Safe QR code matrix decoding and payload risk evaluation |
| `POST` | `/api/analyze/voice` | Audio voice note analysis with acoustic transcript engine |
| `POST` | `/api/guardian` | Generates shareable family alert warning card |
| `GET` | `/api/dojo/challenges` | Curated multi-level Scam Dojo challenges |
| `POST` | `/api/dojo/answer` | Evaluates answer, calculates streak, score, and rank |

---

## 🔒 Privacy & Safety Declarations

- **Data Minimization**: ScamShield processes messages in transient memory and retains no user communications on a server database.
- **Sensitive Credential Redaction**: Automatically scrubs detected credit card numbers and OTPs before evaluation.
- **No SSRF / No Blind Navigation**: ScamShield parses URLs lexically and never connects to or executes remote targets.
- **Verified Cybercrime Resources**: Integrates official Indian Ministry of Home Affairs reporting portal ([cybercrime.gov.in](https://cybercrime.gov.in)) and national helpline **1930**.

---

## 🏆 Hackathon Context

- **Event**: HackNowa Global Hackathon 2026
- **Primary Track**: Digital Safety & Cybersecurity
- **Secondary Fit**: AI for Everyday Life
- **Positioning**: Traditional tools ask *"Is this domain malicious?"* ScamShield AI asks *"Is this suspicious? Why? What should you do? How do you warn your family? And how do you train to spot the next scam?"*

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
