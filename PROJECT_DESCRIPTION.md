# ScamShield AI — HackNowa Global Hackathon 2026 Submission

**Project Title:** ScamShield AI  
**Tagline:** Detect it. Understand it. Practice it. Prevent it.  
**Track:** Digital Safety & Cybersecurity (Primary) | AI for Everyday Life (Secondary)  
**Live Demo Architecture:** Next.js (App Router, TypeScript, Tailwind CSS) + FastAPI (Python 3.10+, scikit-learn, OpenCV, RapidOCR)

---

## 1. Problem Statement

Cyber fraud in India and emerging economies has shifted from blunt malware to hyper-targeted social engineering. Citizens routinely receive fraudulent communications:
- **Fake Bank KYC SMS**: Threatening same-day account suspension.
- **Micro-Payment Delivery Lures**: Asking ₹25 to reschedule courier addresses, designed to harvest card numbers and OTPs.
- **Task & Job Scams**: Funneling users from WhatsApp to Telegram tasks.
- **Coercive Extortion**: Fabricating "Digital Arrests" and CBI investigations over video calls.

Traditional cybersecurity tools only answer one narrow question: *"Is this domain on a known blacklist?"* But ordinary users face real-world dilemmas:
1. *Is this message actually suspicious?*
2. *Why is it suspicious in plain language?*
3. *What should I do right now to protect my money?*
4. *How can I warn my parents or family members before they get tricked?*
5. *How can I become better at identifying the next scam before it happens?*

---

## 2. The Solution: ScamShield AI

**ScamShield AI** is an intelligent cybersecurity guardian that bridges the gap between technical threat telemetry and everyday human action.

It operates on a continuous 5-step cognitive pipeline:
$$\text{Input} \longrightarrow \text{Analysis} \longrightarrow \text{Risk Score} \longrightarrow \text{TrustLens Evidence} \longrightarrow \text{Action Plan} \longrightarrow \text{Scam Dojo Education}$$

### Key Innovations:
1. **Multimodal Ingestion**: Accepts raw messages, URLs, screenshots (OCR), QR codes (matrix decoding), and voice notes without requiring paid external APIs.
2. **Transparent Multi-Signal Architecture**: Combines deterministic cybersecurity rules, lexical URL feature extractors, and trained machine learning pipelines (`RandomForestClassifier`) rather than acting as a black-box AI wrapper.
3. **TrustLens Evidence Engine**: Deconstructs every threat into clear, numbered evidence cards (`01 — URGENCY`, `02 — IMPERSONATION`, `03 — DOMAIN MISMATCH`) with interactive red-flag text highlighting.
4. **Family Guardian**: 1-click generation of shareable, jargon-free alert cards formatted for WhatsApp and SMS family groups.
5. **Gamified Scam Dojo**: An interactive cybersecurity gym featuring 6 progressive tiers and 12 realistic scenarios that trains users to spot subtle phishing cues before they occur in the real world.
6. **Vernacular Multilingual Support**: Accessible in English, Tamil, Hindi, Telugu, Malayalam, and Kannada with simple, contextual local language summaries.

---

## 3. Technical Architecture

ScamShield AI is divided into specialized decoupled subsystems:

- **Frontend (Next.js 16 App Router, React 19, TypeScript, Tailwind CSS)**:
  - Responsive cybersecurity intelligence UI with dark aesthetics, glassmorphism, and accessible contrast.
  - Interactive SVG circular risk gauge with animated score counters.
  - Red-flag inline highlighting engine with hover tooltip inspectors.
  - Multi-vector risk breakdown meters (Domain, Social Eng, URL, Intent, Credential).
  - Gamified Scam Dojo state tracker (streaks, score points, accuracy, rank progression).
  - LocalStorage sandbox threat audit history.

- **Backend (FastAPI, Python 3.10+, Pydantic v2)**:
  - `backend/safety/sanitization.py`: Input length checks, card/OTP masking, safe URL syntax validation without SSRF vulnerability.
  - `backend/detection/url_features.py`: Extracts 20+ lexical, host, Shannon entropy, and brand mismatch signals.
  - `backend/detection/rules.py`: Transparent heuristic rule engine returning structured evidence dictionaries.
  - `backend/detection/classifier.py`: 26-dimensional combined feature pipeline trained via scikit-learn.
  - `backend/detection/fusion.py`: Configurable multi-vector score fusion normalizing risk between `0.00` and `1.00`.
  - `backend/detection/evidence.py`: TrustLens evidence card builder and protective action plan generator.
  - `backend/vision/ocr.py` & `qr.py`: Local RapidOCR (ONNX) and OpenCV QR decoder.
  - `backend/voice/transcribe.py`: Acoustic analysis with manual transcript fallback.
  - `backend/api/dojo.py`: Curated scenario engine with server-side ground truth verification.

---

## 4. Evaluation & Quantitative Benchmarks

All benchmark values are generated directly from the reproducible evaluation pipeline (`python evaluation/evaluate.py`) on our curated 70-sample ground-truth dataset (`urls.csv` and `messages.csv`):

- **Isolated ML Pipeline (5-Fold Stratified Cross-Validation holdouts)**:
  - Accuracy: **84.29%**
  - Precision: **92.86%**
  - Recall: **74.29%**
  - F1-Score: **0.8254**
  - Latency: **6.62 ms / sample**

- **ScamShield Multi-Signal End-to-End System (5-Fold Stratified Holdout Test Folds)**:
  - Accuracy: **92.86%**
  - Precision: **96.88%**
  - Recall: **88.57%**
  - F1-Score: **0.9254**
  - End-to-End Latency: **0.72 ms / request**
  - *Dataset Note: Evaluated on the included 70-sample prototype dataset (40 URLs, 30 Messages, 50% scam / 50% legitimate) using strict out-of-fold holdout predictions with zero data leakage. This benchmark validates prototype pipeline efficacy, not global production threats.*

---

## 5. Privacy, Ethics & Security

- **Data Minimization**: Content submitted for analysis is processed in transient memory and never written to a permanent server database.
- **Sensitive Credential Scrubbing**: Automatically detects and masks credit card patterns (`[REDACTED_CARD_NUMBER]`) and OTP codes (`[REDACTED_OTP]`).
- **No SSRF / No Blind Navigation**: ScamShield parses URLs lexically and never connects to or executes remote targets.
- **Verified Cybercrime Resources**: Integrates official Indian Ministry of Home Affairs reporting portal (`https://cybercrime.gov.in`) and national helpline `1930`.

---

## 6. Limitations & Future Scope

### Current Limitations:
- Audio note analysis uses local acoustic metadata and speech transcription fallback when external Whisper binaries are not configured.
- Visual phishing detection evaluates layout and OCR text rather than pixel-level DOM screenshots of active websites.

### Future Scope:
- Lightweight browser extension for proactive WhatsApp Web and Gmail link inspection.
- On-device mobile keyboard companion for Android.
- Community threat sharing feed federated through encrypted anonymized hashes.
