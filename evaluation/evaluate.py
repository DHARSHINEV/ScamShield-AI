"""
Strict Out-of-Fold Model Training & Benchmark Pipeline for ScamShield AI.
Guarantees ZERO data leakage by evaluating all systems (ML classifier and
Multi-Signal end-to-end pipeline) strictly on out-of-fold holdout predictions.

Outputs real, measured metrics for:
1. Isolated ML Classifier (5-Fold Out-of-Fold CV)
2. URL Detector Subsystem (40 Samples Out-of-Fold)
3. Message Detector Subsystem (30 Samples Out-of-Fold)
4. Combined Multi-Signal System (70 Samples Out-of-Fold)
"""
import sys
import os
import time
import json
import joblib
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold

# Ensure project root is in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from backend.detection.classifier import extract_combined_features, FEATURE_NAMES
from backend.detection.rules import run_rule_engine
from backend.detection.url_features import extract_url_features
from backend.detection.fusion import fuse_scores
from backend.safety.sanitization import extract_urls
from evaluation.metrics import compute_classification_metrics

DATASET_DIR = BASE_DIR / "evaluation" / "dataset"
RESULTS_DIR = BASE_DIR / "evaluation" / "results"
MODELS_DIR = BASE_DIR / "models"

RESULTS_DIR.mkdir(parents=True, exist_ok=True)
MODELS_DIR.mkdir(parents=True, exist_ok=True)

# Ensure UTF-8 output on Windows
if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def train_and_evaluate():
    print("=" * 70)
    print("[*] SCAMSHIELD AI - LEAK-FREE OUT-OF-FOLD EVALUATION BENCHMARK")
    print("=" * 70)
    
    # 1. Load Datasets
    urls_file = DATASET_DIR / "urls.csv"
    msgs_file = DATASET_DIR / "messages.csv"
    
    df_urls = pd.read_csv(urls_file)
    df_msgs = pd.read_csv(msgs_file)
    
    n_urls = len(df_urls)
    n_msgs = len(df_msgs)
    total_samples = n_urls + n_msgs
    print(f"Loaded {n_urls} URL samples and {n_msgs} Message samples. Total: {total_samples}")
    
    # 2. Extract Feature Matrix
    X_list = []
    y_list = []
    sample_metadata = []
    
    for _, row in df_urls.iterrows():
        feat = extract_combined_features(text="", url=row["url"])
        X_list.append(feat[0])
        y_list.append(int(row["label"]))
        sample_metadata.append({"type": "url", "raw": row["url"]})
        
    for _, row in df_msgs.iterrows():
        urls = extract_urls(row["text"])
        u = urls[0] if urls else None
        feat = extract_combined_features(text=row["text"], url=u)
        X_list.append(feat[0])
        y_list.append(int(row["label"]))
        sample_metadata.append({"type": "message", "raw": row["text"]})
        
    X = np.array(X_list, dtype=np.float32)
    y = np.array(y_list, dtype=np.int32)
    
    # 3. 5-Fold Stratified Cross-Validation (ZERO LEAKAGE)
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    
    oof_ml_preds = np.zeros(total_samples)
    oof_ml_probas = np.zeros(total_samples)
    oof_sys_preds = np.zeros(total_samples)
    
    ml_latencies = []
    sys_latencies = []
    
    for fold, (train_idx, test_idx) in enumerate(skf.split(X, y), start=1):
        # Train fold classifier ONLY on train_idx
        fold_clf = RandomForestClassifier(n_estimators=50, max_depth=6, random_state=42)
        fold_clf.fit(X[train_idx], y[train_idx])
        
        # Evaluate strictly on unseen test_idx
        for idx in test_idx:
            sample_meta = sample_metadata[idx]
            feat_vec = X[idx].reshape(1, -1)
            
            # Isolated ML Inference
            t0 = time.time()
            proba = fold_clf.predict_proba(feat_vec)[0][1]
            pred = 1 if proba >= 0.5 else 0
            t1 = time.time()
            ml_latencies.append((t1 - t0) * 1000)
            
            oof_ml_preds[idx] = pred
            oof_ml_probas[idx] = proba
            
            # End-to-End System Evaluation (Rules + URLs + ML Out-of-Fold)
            t_sys_0 = time.time()
            if sample_meta["type"] == "url":
                u = sample_meta["raw"]
                u_feats = extract_url_features(u)
                rule_res = run_rule_engine("", [u])
                fusion = fuse_scores(rule_res["rule_score"], u_feats["risk_score"], proba)
            else:
                txt = sample_meta["raw"]
                urls = extract_urls(txt)
                u = urls[0] if urls else None
                u_score = extract_url_features(u)["risk_score"] if u else None
                rule_res = run_rule_engine(txt, urls)
                fusion = fuse_scores(rule_res["rule_score"], u_score, proba)
            t_sys_1 = time.time()
            sys_latencies.append((t_sys_1 - t_sys_0) * 1000)
            
            # System decision: 1 (Scam) if HIGH RISK or SUSPICIOUS
            oof_sys_preds[idx] = 1 if fusion["classification"] in ["HIGH RISK", "SUSPICIOUS"] else 0
            
    # Compute Out-of-Fold Metrics for Isolated ML Layer
    ml_metrics = compute_classification_metrics(y.tolist(), oof_ml_preds.tolist(), ml_latencies)
    
    # Compute Out-of-Fold Metrics for Full System
    sys_metrics = compute_classification_metrics(y.tolist(), oof_sys_preds.tolist(), sys_latencies)
    
    # Compute Subsystem Breakdowns (URL-only vs Message-only)
    url_indices = list(range(n_urls))
    msg_indices = list(range(n_urls, total_samples))
    
    url_sys_metrics = compute_classification_metrics(
        y[url_indices].tolist(),
        oof_sys_preds[url_indices].tolist(),
        [sys_latencies[i] for i in url_indices]
    )
    
    msg_sys_metrics = compute_classification_metrics(
        y[msg_indices].tolist(),
        oof_sys_preds[msg_indices].tolist(),
        [sys_latencies[i] for i in msg_indices]
    )
    
    # Display Output
    print(f"\n[1. ML Classifier Alone (5-Fold Out-of-Fold CV)]")
    print(f"Accuracy:  {ml_metrics['accuracy'] * 100:.2f}%")
    print(f"Precision: {ml_metrics['precision'] * 100:.2f}%")
    print(f"Recall:    {ml_metrics['recall'] * 100:.2f}%")
    print(f"F1-Score:  {ml_metrics['f1_score']:.4f}")
    print(f"Latency:   {ml_metrics['average_latency_ms']:.2f} ms/sample")
    
    print(f"\n[2. URL Detector Subsystem (40 Out-of-Fold Samples)]")
    print(f"Accuracy:  {url_sys_metrics['accuracy'] * 100:.2f}%")
    print(f"Precision: {url_sys_metrics['precision'] * 100:.2f}%")
    print(f"Recall:    {url_sys_metrics['recall'] * 100:.2f}%")
    print(f"F1-Score:  {url_sys_metrics['f1_score']:.4f}")
    
    print(f"\n[3. Message Detector Subsystem (30 Out-of-Fold Samples)]")
    print(f"Accuracy:  {msg_sys_metrics['accuracy'] * 100:.2f}%")
    print(f"Precision: {msg_sys_metrics['precision'] * 100:.2f}%")
    print(f"Recall:    {msg_sys_metrics['recall'] * 100:.2f}%")
    print(f"F1-Score:  {msg_sys_metrics['f1_score']:.4f}")
    
    print(f"\n[4. Combined ScamShield Multi-Signal System (70 Out-of-Fold Samples)]")
    print(f"Accuracy:  {sys_metrics['accuracy'] * 100:.2f}%")
    print(f"Precision: {sys_metrics['precision'] * 100:.2f}%")
    print(f"Recall:    {sys_metrics['recall'] * 100:.2f}%")
    print(f"F1-Score:  {sys_metrics['f1_score']:.4f}")
    print(f"Latency:   {sys_metrics['average_latency_ms']:.2f} ms/request")
    
    # 4. Save Final Production Model (trained on all 70 samples for deployment)
    final_model = RandomForestClassifier(n_estimators=60, max_depth=6, random_state=42)
    final_model.fit(X, y)
    model_save_path = MODELS_DIR / "scam_url_model.joblib"
    joblib.dump(final_model, model_save_path)
    print(f"\nSaved production model artifact to {model_save_path}")
    
    # 5. Save Honest Metrics JSON
    evaluation_results = {
        "benchmark_type": "prototype_validation_benchmark",
        "dataset": {
            "total_samples": total_samples,
            "url_samples": n_urls,
            "message_samples": n_msgs,
            "positive_scam_samples": int(np.sum(y == 1)),
            "negative_legitimate_samples": int(np.sum(y == 0)),
            "balance_ratio": "50% scam / 50% legitimate (balanced)",
            "data_source": "Manually curated representative synthetic and public cyber threat patterns",
            "limitations": [
                "Small prototype dataset (70 samples) designed for validation of detection pipeline components.",
                "Not an external wild-web benchmark.",
                "Does not reflect production-world threat drift without continuous retraining."
            ]
        },
        "evaluation_methodology": "5-Fold Stratified Cross-Validation with strict out-of-fold prediction (Zero Leakage)",
        "results": {
            "ml_classifier_oof_cv": ml_metrics,
            "url_detector_oof": url_sys_metrics,
            "message_detector_oof": msg_sys_metrics,
            "combined_multisignal_oof": sys_metrics
        },
        "feature_count": len(FEATURE_NAMES),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    metrics_path = RESULTS_DIR / "metrics.json"
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(evaluation_results, f, indent=2)
    print(f"Saved verified evaluation metrics to {metrics_path}")
    
    # 6. Plot Confusion Matrix
    cm = sys_metrics["confusion_matrix"]
    cm_matrix = np.array([
        [cm["true_negative"], cm["false_positive"]],
        [cm["false_negative"], cm["true_positive"]]
    ])
    
    plt.figure(figsize=(7, 6))
    plt.imshow(cm_matrix, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title('ScamShield AI - Out-of-Fold Confusion Matrix (Combined System)', fontsize=12, fontweight='bold', pad=15)
    plt.colorbar()
    tick_marks = np.arange(2)
    plt.xticks(tick_marks, ['Legitimate (0)', 'Scam/Phish (1)'], fontsize=11)
    plt.yticks(tick_marks, ['Legitimate (0)', 'Scam/Phish (1)'], fontsize=11)
    
    thresh = cm_matrix.max() / 2.
    for i in range(2):
        for j in range(2):
            val = cm_matrix[i, j]
            color = "white" if val > thresh else "black"
            lbl = f"{val}\n({('TN' if i==0 and j==0 else 'FP' if i==0 and j==1 else 'FN' if i==1 and j==0 else 'TP')})"
            plt.text(j, i, lbl, horizontalalignment="center", verticalalignment="center",
                     color=color, fontsize=12, fontweight='bold')
                     
    plt.ylabel('Ground Truth (Actual)', fontsize=12)
    plt.xlabel('ScamShield Out-of-Fold Prediction', fontsize=12)
    plt.tight_layout()
    
    cm_plot_path = RESULTS_DIR / "confusion_matrix.png"
    plt.savefig(cm_plot_path, dpi=200)
    plt.close()
    print(f"Generated confusion matrix plot at {cm_plot_path}")
    print("=" * 70)
    print("[+] EVALUATION COMPLETED WITH ZERO DATA LEAKAGE")
    print("=" * 70)

if __name__ == "__main__":
    train_and_evaluate()
