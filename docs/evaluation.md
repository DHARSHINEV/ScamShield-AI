# ScamShield AI — Quantitative Evaluation & Benchmark Report

> **Scientific Notice & Integrity Statement:**  
> All benchmark values reported in this document are generated directly from the included reproducible evaluation pipeline (`python evaluation/evaluate.py`) on our 70-sample ground-truth prototype dataset. **Evaluation uses strict 5-Fold Stratified Cross-Validation with out-of-fold predictions to guarantee ZERO data leakage.** No fabricated or in-sample metrics are presented.

---

## 1. Prototype Benchmark Scope & Limitations

### Prototype Limitations
- **Dataset Size:** 70 curated samples (40 URLs, 30 Messages).
- **Data Source:** Manually curated representative samples mirroring real-world scam lures active in India and Asia-Pacific (KYC threats, ₹25 delivery micro-fees, YouTube task jobs, digital arrest extortion) alongside verified legitimate notifications.
- **Absence of Wild-Web Scale:** This benchmark is explicitly intended to validate that the multi-signal pipeline, rule engine, and ML feature representations work correctly together. It **does NOT claim production-world threat detection at internet scale**, which would require continuous telemetry and live threat feeds.
- **Zero Data Leakage:** In this evaluation pass, the multi-signal system is evaluated strictly using **out-of-fold cross-validation predictions**. No sample was ever included in the model training split when being evaluated by the system.

---

## 2. Dataset Composition

The ground-truth benchmark dataset comprises **70 curated samples** with a strict 50:50 balanced class distribution:

| Sub-Dataset | Total | Malicious (Scam / Phishing) | Benign (Legitimate) | Category Coverage |
| :--- | :--- | :--- | :--- | :--- |
| **URLs** (`urls.csv`) | **40** | 20 (50%) | 20 (50%) | IP hosts, brand spoofing, suspicious TLDs, punycode, vs. official banking & e-commerce portals |
| **Messages** (`messages.csv`) | **30** | 15 (50%) | 15 (50%) | KYC deactivation, courier reschedule fees, job scams, digital arrest, vs. genuine bank debit alerts & OTPs |
| **Total Benchmark** | **70** | **35 (50%)** | **35 (50%)** | Balanced 50% scam / 50% legitimate |

---

## 3. Measured Out-of-Fold Benchmark Results

### 1. Isolated Machine Learning Classifier (5-Fold Out-of-Fold CV)
Evaluates the 26-dimensional feature vector fitted on a `RandomForestClassifier` on holdout folds:

| Metric | Measured Value | Operational Interpretation |
| :--- | :--- | :--- |
| **Accuracy** | **84.29%** (0.8429) | Correct predictions on unseen holdout test folds |
| **Precision** | **92.86%** (0.9286) | High precision prevents false accusations |
| **Recall** | **74.29%** (0.7429) | Catches three out of four attacks purely on statistical features |
| **F1-Score** | **0.8254** | Balanced harmonic score |
| **Inference Latency** | **6.62 ms / sample** | Fast model evaluation |

---

### 2. URL Detector Subsystem (40 Out-of-Fold Samples)
Evaluates lexical URL feature analysis, Shannon entropy, and brand mismatch verification on holdout folds:

| Metric | Measured Value |
| :--- | :--- |
| **Accuracy** | **100.00%** (1.0000) |
| **Precision** | **100.00%** (1.0000) |
| **Recall** | **100.00%** (1.0000) |
| **F1-Score** | **1.0000** |

---

### 3. Message Detector Subsystem (30 Out-of-Fold Samples)
Evaluates linguistic cues, urgency markers, and social-engineering indicators on holdout folds:

| Metric | Measured Value |
| :--- | :--- |
| **Accuracy** | **83.33%** (0.8333) |
| **Precision** | **91.67%** (0.9167) |
| **Recall** | **73.33%** (0.7333) |
| **F1-Score** | **0.8148** |

---

### 4. Combined ScamShield Multi-Signal System (70 Out-of-Fold Samples)
Synthesizes the Rule Engine, URL Structural Analyzer, and Out-of-Fold ML Probabilities through the Multi-Signal Fusion Engine:

| Metric | Measured Value | Operational Impact |
| :--- | :--- | :--- |
| **System Accuracy** | **92.86%** (0.9286) | Solid end-to-end detection across holdout test splits |
| **System Precision** | **96.88%** (0.9688) | Low false alarm rate; legitimate transactions remain safe |
| **System Recall** | **88.57%** (0.8857) | Successfully intercepts 31 of 35 diverse attack types |
| **System F1-Score** | **0.9254** | Robust multi-modal balance |
| **End-to-End Latency** | **0.72 ms / request** | Instantaneous interactive response |

---

## 4. Confusion Matrix (Combined System Out-of-Fold)

Visualized in `evaluation/results/confusion_matrix.png`:

```
                           Predicted: Legitimate (0)   Predicted: Scam (1)
Actual Ground Truth:
Legitimate (0)                     34 (TN)                     1 (FP)
Scam / Phishing (1)                 4 (FN)                    31 (TP)
```

- **True Negatives (TN): 34** — 34 of 35 legitimate banking transactions, delivery confirmations, and OTP notices were correctly classified as SAFE.
- **False Positives (FP): 1** — Only 1 benign alert triggered a borderline suspicious flag.
- **False Negatives (FN): 4** — 4 subtle text lures fell below the high-risk threshold when evaluated out-of-fold without prior exposure.
- **True Positives (TP): 31** — 31 attacks were intercepted.

---

## 5. How to Reproduce Benchmarks

Run the evaluation script from the project root:

```bash
python evaluation/evaluate.py
```

Outputs:
- JSON report: `evaluation/results/metrics.json`
- Matrix plot: `evaluation/results/confusion_matrix.png`
- Production model: `models/scam_url_model.joblib`
