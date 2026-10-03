"""
Evaluation Metrics calculation utilities for ScamShield AI.
"""
from typing import Dict, Any, List
import numpy as np

def compute_classification_metrics(y_true: List[int], y_pred: List[int], latency_list: List[float] = None) -> Dict[str, Any]:
    """Compute precision, recall, f1, accuracy, and confusion matrix from raw arrays."""
    y_t = np.array(y_true)
    y_p = np.array(y_pred)
    
    tp = int(np.sum((y_t == 1) & (y_p == 1)))
    fp = int(np.sum((y_t == 0) & (y_p == 1)))
    tn = int(np.sum((y_t == 0) & (y_p == 0)))
    fn = int(np.sum((y_t == 1) & (y_p == 0)))
    
    total = len(y_t)
    accuracy = (tp + tn) / max(total, 1)
    precision = tp / max(tp + fp, 1)
    recall = tp / max(tp + fn, 1)
    f1 = (2 * precision * recall) / max(precision + recall, 1e-9)
    
    avg_latency = float(np.mean(latency_list)) if latency_list else 0.0
    
    return {
        "accuracy": round(float(accuracy), 4),
        "precision": round(float(precision), 4),
        "recall": round(float(recall), 4),
        "f1_score": round(float(f1), 4),
        "confusion_matrix": {
            "true_positive": tp,
            "false_positive": fp,
            "true_negative": tn,
            "false_negative": fn
        },
        "total_samples": total,
        "average_latency_ms": round(avg_latency, 2)
    }
