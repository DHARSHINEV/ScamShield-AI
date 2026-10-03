"""
TrustLens Evidence Engine for ScamShield AI.
Transforms raw rule signals and URL features into clear, explainable,
human-first evidence cards and concrete action plans.
"""
from typing import List, Dict, Any, Optional

# Verified official contact references
OFFICIAL_CYBERCRIME_RESOURCES = {
    "india_portal": "https://cybercrime.gov.in",
    "india_helpline": "1930 (National Cyber Crime Reporting Portal Helpline)",
    "rbi_sachet": "https://sachet.rbi.org.in (RBI portal for unauthorized deposit schemes)",
}

def generate_evidence_cards(raw_evidence: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Format evidence into numbered TrustLens evidence cards.
    Example:
    01 — URGENCY: Creates pressure to act quickly
    02 — IMPERSONATION: Claims to represent a trusted organization
    03 — DOMAIN MISMATCH: Domain does not match official institution
    """
    category_titles = {
        "URGENCY": "URGENCY & PRESSURE",
        "THREAT_COERCION": "INTIMIDATION & THREAT",
        "CREDENTIAL_HARVESTING": "CREDENTIAL REQUEST",
        "OTP_SOLICITATION": "OTP SOLICITATION",
        "FINANCIAL_SOLICITATION": "FINANCIAL DEMAND",
        "IMPERSONATION": "AUTHORITY IMPERSONATION",
        "REWARD_BAIT": "PRIZE / REWARD BAIT",
        "DELIVERY_SCAM": "FAKE DELIVERY COURIER",
        "JOB_SCAM": "UNREALISTIC JOB LURE",
        "DOMAIN_MISMATCH": "DOMAIN SPOOFING / MISMATCH",
        "URL_IP_HOST": "SUSPICIOUS IP ADDRESS HOST",
        "URL_PUNYCODE": "HOMOGRAPH / LOOKALIKE DOMAIN",
        "URL_SUSPICIOUS_TLD": "HIGH-RISK DOMAIN EXTENSION",
        "URL_SHORTENER": "MASKED SHORTENED LINK",
        "URL_INSECURE_HTTP": "UNENCRYPTED CREDENTIAL SUBMISSION",
        "URL_HYPHENATED_DOMAIN": "BRAND-SPOOFING HYPHENS",
        "URL_SUSPICIOUS_KEYWORDS": "DECEPTIVE KEYWORDS IN URL",
        "URL_HIGH_ENTROPY": "RANDOMIZED DISPOSABLE DOMAIN",
        "URL_EMBEDDED_AT_SYMBOL": "CREDENTIAL REDIRECTION TRICK"
    }

    cards = []
    for idx, item in enumerate(raw_evidence[:6], start=1):
        ev_type = item.get("type", "GENERIC_RISK")
        title = category_titles.get(ev_type, ev_type.replace("_", " "))
        cards.append({
            "id": f"{idx:02d}",
            "type": ev_type,
            "title": f"{idx:02d} — {title}",
            "severity": item.get("severity", "medium"),
            "matched_text": item.get("matched_text", ""),
            "explanation": item.get("explanation", "")
        })
    return cards

def generate_red_flags(text: str, raw_evidence: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Extract snippets for red-flag inline highlighting in the UI.
    """
    red_flags = []
    seen_texts = set()
    for ev in raw_evidence:
        matched = ev.get("matched_text", "")
        if matched and matched.lower() in text.lower() and matched.lower() not in seen_texts:
            seen_texts.add(matched.lower())
            red_flags.append({
                "text": matched,
                "reason": ev.get("explanation", "Detected risk pattern"),
                "severity": ev.get("severity", "medium"),
                "type": ev.get("type", "")
            })
    return red_flags

def generate_action_plan(
    classification: str,
    raw_evidence: List[Dict[str, Any]],
    urls: List[str]
) -> List[Dict[str, str]]:
    """
    Generate tailored, protective action steps based on specific detected threats.
    """
    actions = []
    ev_types = {e.get("type") for e in raw_evidence}
    
    if classification == "SAFE":
        actions.append({
            "step": "Standard Vigilance",
            "instruction": "This message does not exhibit obvious scam markers. However, always exercise standard digital caution.",
            "priority": "info"
        })
        actions.append({
            "step": "Verify Sensitive Changes",
            "instruction": "If the sender ever asks for financial transactions or credentials in future communications, verify directly through trusted official numbers.",
            "priority": "low"
        })
        return actions

    # Suspicious or High Risk actions
    if urls or any("URL" in t or "DOMAIN" in t for t in ev_types):
        actions.append({
            "step": "Do NOT Click the Link",
            "instruction": "Avoid opening this link on any browser. Phishing links can capture session tokens or harvest login credentials.",
            "priority": "critical"
        })
        
    if "OTP_SOLICITATION" in ev_types or "CREDENTIAL_HARVESTING" in ev_types:
        actions.append({
            "step": "NEVER Share OTPs or Passwords",
            "instruction": "Banks, courier companies, and government portals will NEVER ask for your password, PIN, or OTP over message, call, or email.",
            "priority": "critical"
        })
        
    if "IMPERSONATION" in ev_types or "DOMAIN_MISMATCH" in ev_types:
        actions.append({
            "step": "Verify via Official Channels",
            "instruction": "Access the institution solely by typing their known legitimate URL in your browser or through their official app. Do not use contact numbers provided inside the message.",
            "priority": "high"
        })
        
    if "FINANCIAL_SOLICITATION" in ev_types or "DELIVERY_SCAM" in ev_types:
        actions.append({
            "step": "Do NOT Send Money or Advance Fees",
            "instruction": "Legitimate delivery services will not require small online fee payments (e.g. ₹25/₹50) to reschedule addresses. This is a tactic to skim card numbers.",
            "priority": "high"
        })
        
    if "THREAT_COERCION" in ev_types:
        actions.append({
            "step": "Do NOT Panic — Recognize Coercion",
            "instruction": "Law enforcement or banks never issue 'Digital Arrests' or demand immediate money transfer on video calls. Disconnect immediately.",
            "priority": "high"
        })
        
    # Standard reporting action
    actions.append({
        "step": "Report the Suspicious Communication",
        "instruction": f"In India, report cybersecurity fraud immediately at {OFFICIAL_CYBERCRIME_RESOURCES['india_portal']} or call the national cybercrime helpline {OFFICIAL_CYBERCRIME_RESOURCES['india_helpline']}.",
        "priority": "medium"
    })
    
    actions.append({
        "step": "Warn Your Contacts / Family",
        "instruction": "Use the 'Protect My Family' card below to alert family members who might be targeted by the same scam wave.",
        "priority": "medium"
    })
    
    return actions
