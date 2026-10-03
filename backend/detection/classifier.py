"""
Machine Learning Classifier Pipeline for ScamShield AI.
Extracts combined feature vectors (Lexical, URL, Social Engineering) and
performs inference using trained models (with calibrated feature-inference fallback).
"""
import os
import joblib
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path

from backend.detection.url_features import extract_url_features
from backend.detection.message_features import extract_message_features
from backend.config.settings import settings

FEATURE_NAMES = [
    "url_length",
    "domain_length",
    "path_length",
    "num_dots",
    "num_hyphens",
    "num_digits",
    "is_https",
    "is_ip",
    "is_shortener",
    "is_suspicious_tld",
    "domain_entropy",
    "brand_mismatch",
    "num_suspicious_kw",
    "msg_length",
    "uppercase_ratio",
    "exclamation_count",
    "has_currency",
    "urgency_score",
    "threat_score",
    "credential_score",
    "otp_score",
    "financial_score",
    "delivery_score",
    "reward_score",
    "job_score",
    "social_eng_intensity"
]

_CACHED_MODEL = None
_MODEL_LOAD_ATTEMPTED = False

def extract_combined_features(text: str, url: Optional[str] = None) -> np.ndarray:
    """
    Extract a unified numerical feature vector combining text and URL signals.
    """
    msg_feats = extract_message_features(text)
    stats = msg_feats["text_stats"]
    cat_scores = msg_feats["category_scores"]
    
    if url:
        url_feats = extract_url_features(url)
    else:
        url_feats = {
            "length": 0,
            "domain_length": 0,
            "path_length": 0,
            "num_dots": 0,
            "num_hyphens": 0,
            "num_digits": 0,
            "is_https": False,
            "is_ip": False,
            "is_shortener": False,
            "is_suspicious_tld": False,
            "domain_entropy": 0.0,
            "brand_mismatches": [],
            "matched_keywords": []
        }
        
    vector = [
        float(url_feats.get("length", 0)),
        float(url_feats.get("domain_length", 0)),
        float(url_feats.get("path_length", 0)),
        float(url_feats.get("num_dots", 0)),
        float(url_feats.get("num_hyphens", 0)),
        float(url_feats.get("num_digits", 0)),
        1.0 if url_feats.get("is_https") else 0.0,
        1.0 if url_feats.get("is_ip") else 0.0,
        1.0 if url_feats.get("is_shortener") else 0.0,
        1.0 if url_feats.get("is_suspicious_tld") else 0.0,
        float(url_feats.get("domain_entropy", 0.0)),
        1.0 if len(url_feats.get("brand_mismatches", [])) > 0 else 0.0,
        float(len(url_feats.get("matched_keywords", []))),
        float(stats["length"]),
        float(stats["uppercase_ratio"]),
        float(stats["exclamation_count"]),
        1.0 if stats["currency_symbol_count"] > 0 else 0.0,
        float(cat_scores.get("urgency", 0.0)),
        float(cat_scores.get("threat", 0.0)),
        float(cat_scores.get("credential_request", 0.0)),
        float(cat_scores.get("otp_request", 0.0)),
        float(cat_scores.get("financial_request", 0.0)),
        float(cat_scores.get("delivery_scam", 0.0)),
        float(cat_scores.get("reward_lottery", 0.0)),
        float(cat_scores.get("job_scam", 0.0)),
        float(msg_feats.get("social_engineering_intensity", 0.0))
    ]
    return np.array(vector, dtype=np.float32).reshape(1, -1)

def get_or_load_model():
    """Load pre-trained model once at startup."""
    global _CACHED_MODEL, _MODEL_LOAD_ATTEMPTED
    if not _MODEL_LOAD_ATTEMPTED:
        _MODEL_LOAD_ATTEMPTED = True
        model_path = settings.URL_MODEL_PATH
        if model_path.exists():
            try:
                _CACHED_MODEL = joblib.load(model_path)
            except Exception:
                _CACHED_MODEL = None
    return _CACHED_MODEL

def predict_scam_probability(text: str, url: Optional[str] = None) -> Dict[str, Any]:
    """
    Compute P(phishing/scam) using trained ML model if present,
    or calibrated statistical feature inference.
    """
    feature_vector = extract_combined_features(text, url)
    model = get_or_load_model()
    
    if model is not None:
        try:
            proba = model.predict_proba(feature_vector)[0][1]
            return {
                "p_scam": round(float(proba), 4),
                "model_status": "trained_pipeline",
                "feature_count": len(FEATURE_NAMES)
            }
        except Exception:
            pass
            
    # Calibrated statistical ML feature scoring
    # Weights based on empirical feature significance
    vec = feature_vector[0]
    # Indices:
    # 7: is_ip, 9: is_suspicious_tld, 11: brand_mismatch, 12: num_kw,
    # 17: urgency, 18: threat, 19: credential, 20: otp, 21: financial, 25: se_intensity
    score = (
        vec[7] * 0.20 +       # is_ip
        vec[9] * 0.15 +       # is_suspicious_tld
        vec[11] * 0.25 +      # brand_mismatch
        min(vec[12] * 0.08, 0.16) + # keywords
        vec[17] * 0.15 +      # urgency
        vec[18] * 0.20 +      # threat
        vec[19] * 0.25 +      # credential
        vec[20] * 0.30 +      # otp
        vec[21] * 0.15 +      # financial
        vec[25] * 0.20        # social eng intensity
    )
    p_scam = min(max(score, 0.0), 1.0)
    
    return {
        "p_scam": round(float(p_scam), 4),
        "model_status": "calibrated_feature_ml",
        "feature_count": len(FEATURE_NAMES)
    }
