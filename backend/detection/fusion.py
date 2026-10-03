"""
Multi-Signal Score Fusion Engine for ScamShield AI.
Combines Rule Engine, URL Structural Features, ML Probabilities,
and optional LLM Semantic Analysis into an explainable, calibrated risk score.
"""
from typing import Dict, Any, List, Optional
from backend.config.settings import settings

def calculate_risk_breakdown(
    rule_evidence: List[Dict[str, Any]],
    url_features: Optional[Dict[str, Any]],
    message_features: Optional[Dict[str, Any]],
    rule_score: float,
    ml_score: float
) -> Dict[str, float]:
    """
    Calculate normalized domain-specific risk factor breakdown (0.0 to 1.0).
    Categories:
    - Domain
    - Social Engineering
    - URL Pattern
    - Message Intent
    - Credential Request
    """
    # 1. Domain Risk
    domain_score = 0.0
    if url_features:
        if url_features.get("is_ip"):
            domain_score += 0.45
        if url_features.get("brand_mismatches"):
            domain_score += 0.50
        if url_features.get("is_suspicious_tld"):
            domain_score += 0.35
        if url_features.get("is_punycode"):
            domain_score += 0.40
        if url_features.get("domain_entropy", 0) > 4.0:
            domain_score += 0.20
    domain_score = min(max(domain_score, 0.0), 1.0)
    
    # 2. Social Engineering
    se_score = 0.0
    if message_features:
        se_score = message_features.get("social_engineering_intensity", 0.0)
    se_score = min(max(se_score, 0.0), 1.0)
    
    # 3. URL Pattern
    url_pattern_score = 0.0
    if url_features:
        url_pattern_score = url_features.get("risk_score", 0.0)
    url_pattern_score = min(max(url_pattern_score, 0.0), 1.0)
    
    # 4. Message Intent
    msg_intent_score = 0.0
    if message_features:
        cat_scores = message_features.get("category_scores", {})
        intent_signals = [
            cat_scores.get("urgency", 0),
            cat_scores.get("threat", 0),
            cat_scores.get("delivery_scam", 0),
            cat_scores.get("reward_lottery", 0),
            cat_scores.get("job_scam", 0),
        ]
        msg_intent_score = max(intent_signals) if intent_signals else 0.0
    msg_intent_score = min(max(msg_intent_score, 0.0), 1.0)
    
    # 5. Credential Request
    cred_score = 0.0
    ev_types = {e.get("type") for e in rule_evidence}
    if "CREDENTIAL_HARVESTING" in ev_types:
        cred_score += 0.70
    if "OTP_SOLICITATION" in ev_types:
        cred_score += 0.85
    if "FINANCIAL_SOLICITATION" in ev_types:
        cred_score += 0.50
    cred_score = min(max(cred_score, 0.0), 1.0)
    
    return {
        "domain": round(domain_score, 2),
        "social_engineering": round(se_score, 2),
        "url_pattern": round(url_pattern_score, 2),
        "message_intent": round(msg_intent_score, 2),
        "credential_request": round(cred_score, 2)
    }

def fuse_scores(
    rule_score: float,
    url_score: Optional[float],
    ml_score: float,
    semantic_score: Optional[float] = None
) -> Dict[str, Any]:
    """
    Fuse multiple distinct detection vectors into a unified risk estimate.
    Weights are normalized dynamically based on active signals.
    """
    # Active weights
    has_url = url_score is not None
    has_semantic = semantic_score is not None
    
    # Baseline weights
    w_rule = settings.WEIGHT_RULES
    w_url = settings.WEIGHT_URL if has_url else 0.0
    w_ml = settings.WEIGHT_ML
    w_sem = 0.20 if has_semantic else 0.0
    
    total_weight = w_rule + w_url + w_ml + w_sem
    if total_weight == 0:
        total_weight = 1.0
        
    norm_w_rule = w_rule / total_weight
    norm_w_url = w_url / total_weight
    norm_w_ml = w_ml / total_weight
    norm_w_sem = w_sem / total_weight
    
    final_score = (
        rule_score * norm_w_rule +
        (url_score or 0.0) * norm_w_url +
        ml_score * norm_w_ml +
        ((semantic_score or 0.0) * norm_w_sem if has_semantic else 0.0)
    )
    
    # Strict floor if high-confidence malicious rule matched (e.g. OTP request or severe brand mismatch)
    final_score = min(max(final_score, 0.0), 1.0)
    
    # Classification based on thresholds
    if final_score < settings.SAFE_THRESHOLD:
        classification = "SAFE"
    elif final_score < settings.SUSPICIOUS_THRESHOLD:
        classification = "SUSPICIOUS"
    else:
        classification = "HIGH RISK"
        
    return {
        "final_risk_score": round(final_score, 4),
        "percentage": int(round(final_score * 100)),
        "classification": classification,
        "contributions": {
            "rules": round(rule_score * norm_w_rule, 4),
            "url": round((url_score or 0.0) * norm_w_url, 4),
            "ml": round(ml_score * norm_w_ml, 4),
            "semantic_ai": round((semantic_score or 0.0) * norm_w_sem, 4) if has_semantic else 0.0
        },
        "weights_used": {
            "rules": round(norm_w_rule, 3),
            "url": round(norm_w_url, 3),
            "ml": round(norm_w_ml, 3),
            "semantic_ai": round(norm_w_sem, 3)
        }
    }
