"""
AI Semantic Analyzer for ScamShield AI.
Integrates optional LLM (OpenAI / Gemini) semantic evaluation with
deterministic rule-informed fallback when API keys are not supplied.
"""
import os
import json
import httpx
from typing import List, Dict, Any, Optional

from backend.config.settings import settings
from backend.ai.schemas import SemanticAIResult, RedFlagItem
from backend.ai.prompts import SEMANTIC_ANALYSIS_SYSTEM_PROMPT, build_user_prompt

def deterministic_semantic_fallback(
    text: str,
    urls: List[str],
    rule_signals: List[Dict[str, Any]]
) -> SemanticAIResult:
    """
    High-fidelity deterministic semantic analyzer when no external AI key is present.
    Infers intent, scam type, and summary from detected signals.
    """
    ev_types = {s.get("type", "") for s in rule_signals}
    has_otp = "OTP_SOLICITATION" in ev_types
    has_cred = "CREDENTIAL_HARVESTING" in ev_types
    has_threat = "THREAT_COERCION" in ev_types
    has_urgency = "URGENCY" in ev_types
    has_delivery = "DELIVERY_SCAM" in ev_types
    has_job = "JOB_SCAM" in ev_types
    has_reward = "REWARD_BAIT" in ev_types
    has_mismatch = "DOMAIN_MISMATCH" in ev_types or any("DOMAIN" in t for t in ev_types)
    has_fin = "FINANCIAL_SOLICITATION" in ev_types
    
    # Classify scam type
    if has_delivery:
        scam_type = "delivery_scam"
    elif has_job:
        scam_type = "job_scam"
    elif has_reward:
        scam_type = "lottery_scam"
    elif has_mismatch or has_otp or has_cred or ("sbi" in text.lower() or "bank" in text.lower()):
        scam_type = "phishing"
    elif has_threat:
        scam_type = "extortion_intimidation"
    elif len(rule_signals) == 0:
        scam_type = "legitimate"
    else:
        scam_type = "social_engineering"
        
    # Calculate deterministic semantic risk score
    score = 0.10
    if has_otp:
        score += 0.40
    if has_cred:
        score += 0.35
    if has_mismatch:
        score += 0.30
    if has_threat:
        score += 0.25
    if has_urgency:
        score += 0.20
    if has_delivery or has_job or has_reward or has_fin:
        score += 0.25
        
    score = min(max(score, 0.0), 0.98)
    
    if score >= 0.70:
        classification = "SCAM"
        summary = f"High-confidence {scam_type.replace('_', ' ')} attempt using manufactured urgency and deceptive requests."
    elif score >= 0.35:
        classification = "SUSPICIOUS"
        summary = f"Suspicious communication displaying social-engineering indicators consistent with {scam_type.replace('_', ' ')}."
    else:
        classification = "SAFE"
        summary = "No overt deceptive indicators or social engineering patterns identified."
        
    red_flags = []
    for s in rule_signals[:5]:
        red_flags.append(RedFlagItem(
            text=s.get("matched_text", ""),
            reason=s.get("explanation", "Detected risk pattern"),
            severity=s.get("severity", "medium")
        ))
        
    recommended_actions = [
        "Do not click unverified links or install external APKs.",
        "Verify all urgent claims directly through known official applications.",
        "Never share OTPs, CVV numbers, or login credentials."
    ]
    
    return SemanticAIResult(
        classification=classification,
        risk_score=round(score, 2),
        scam_type=scam_type,
        summary=summary,
        red_flags=red_flags,
        recommended_actions=recommended_actions
    )

async def run_semantic_analysis(
    text: str,
    urls: List[str],
    rule_signals: List[Dict[str, Any]]
) -> tuple[SemanticAIResult, str]:
    """
    Attempt external LLM evaluation if API key is configured.
    Falls back cleanly to deterministic analyzer.
    Returns (SemanticAIResult, provider_name).
    """
    # Check OpenAI
    openai_key = os.getenv("OPENAI_API_KEY") or settings.OPENAI_API_KEY
    if openai_key and len(openai_key) > 10:
        try:
            user_prompt = build_user_prompt(text, urls, rule_signals)
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {openai_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": settings.LLM_MODEL,
                        "messages": [
                            {"role": "system", "content": SEMANTIC_ANALYSIS_SYSTEM_PROMPT},
                            {"role": "user", "content": user_prompt}
                        ],
                        "temperature": 0.1,
                        "response_format": {"type": "json_object"}
                    }
                )
                if resp.status_code == 200:
                    data = resp.json()
                    content = data["choices"][0]["message"]["content"]
                    parsed = json.loads(content)
                    return SemanticAIResult(**parsed), f"openai ({settings.LLM_MODEL})"
        except Exception:
            pass  # Fall back gracefully

    # Check Gemini API
    gemini_key = os.getenv("GEMINI_API_KEY") or settings.GEMINI_API_KEY
    if gemini_key and len(gemini_key) > 10:
        try:
            user_prompt = build_user_prompt(text, urls, rule_signals)
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(
                    url,
                    headers={"Content-Type": "application/json"},
                    json={
                        "contents": [{
                            "parts": [{"text": f"{SEMANTIC_ANALYSIS_SYSTEM_PROMPT}\n\n{user_prompt}"}]
                        }],
                        "generationConfig": {"response_mime_type": "application/json"}
                    }
                )
                if resp.status_code == 200:
                    data = resp.json()
                    content = data["candidates"][0]["content"]["parts"][0]["text"]
                    parsed = json.loads(content)
                    return SemanticAIResult(**parsed), "gemini-1.5-flash"
        except Exception:
            pass

    # Deterministic fallback
    result = deterministic_semantic_fallback(text, urls, rule_signals)
    return result, "deterministic_local_engine"
