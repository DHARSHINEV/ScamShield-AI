"""
Transparent Rule Engine for ScamShield AI.
Detects psychological, semantic, and structural scam indicators.
Every rule returns structured, explainable evidence objects.
"""
import re
from typing import List, Dict, Any, Optional
from backend.detection.url_features import extract_url_features, TARGETED_BRANDS

# High-profile organization names frequently impersonated
IMPERSONATION_TARGETS = [
    ("State Bank of India / SBI", [r"\bsbi\b", r"state bank", r"onlinesbi"]),
    ("HDFC Bank", [r"\bhdfc\b", r"hdfc bank"]),
    ("ICICI Bank", [r"\bicici\b"]),
    ("Axis Bank", [r"\baxis bank\b"]),
    ("Income Tax Department", [r"income tax", r"it department", r"tax refund", r"itr"]),
    ("India Post", [r"india post", r"speed post", r"postal service"]),
    ("Electricity Board / Power Dept", [r"electricity bill", r"power disconnection", r"bijli"]),
    ("WhatsApp Support", [r"whatsapp support", r"whatsapp security", r"whatsapp team"]),
    ("Amazon / Flipkart", [r"\bamazon\b", r"\bflipkart\b"]),
    ("FedEx / DHL / Courier", [r"\bfedex\b", r"\bdhl\b", r"blue dart", r"courier delivery"]),
    ("Netflix / Streaming", [r"\bnetflix\b", r"subscription expired"]),
    ("Police / Law Enforcement", [r"cyber police", r"cbi", r"police department", r"court order", r"digital arrest"]),
    ("Job Recruitment HR", [r"telegram hr", r"recruitment team", r"hiring team"])
]

def find_matched_substring(pattern: str, text: str) -> Optional[str]:
    """Find the actual case-preserved substring that matched."""
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(0)
    return None

def detect_urgency(text: str) -> List[Dict[str, Any]]:
    """Detect artificial urgency and rapid deadlines."""
    evidence = []
    patterns = [
        (r"\b(?:will be|is) blocked today\b", "high", "Creates extreme immediate fear of service loss"),
        (r"\bimmediately\b", "medium", "Pressures the recipient to act before verifying with trusted channels"),
        (r"\bwithin (?:24|12|2|1) hours?\b", "medium", "Imposes artificial countdown deadline to bypass critical thinking"),
        (r"\burgent(?:ly)?\b", "medium", "Classic urgency cue used to bypass analytical skepticism"),
        (r"\bhurry|act fast|limited time|last chance\b", "medium", "Manufactures artificial scarcity to rush decisions"),
        (r"\bexpires (?:today|soon|within)\b", "medium", "Forces hasty reaction under fear of missing out or penalty")
    ]
    for pattern, severity, explanation in patterns:
        matched = find_matched_substring(pattern, text)
        if matched:
            evidence.append({
                "type": "URGENCY",
                "severity": severity,
                "matched_text": matched,
                "explanation": explanation
            })
    return evidence

def detect_threat(text: str) -> List[Dict[str, Any]]:
    """Detect coercive threats, account suspension, or legal intimidation."""
    evidence = []
    patterns = [
        (r"\b(?:account|card|sim|access) (?:will be|has been) (?:blocked|suspended|terminated|deactivated)\b", "high", "Threatens immediate cutoff of essential services to trigger panic"),
        (r"\blegal action|police arrest|court warrant|digital arrest\b", "high", "Severe intimidation invoking law enforcement to terrorize victims"),
        (r"\bpenalty of (?:rs\.?|₹|\$)\s*\d+\b", "high", "Fabricates imminent financial fine or penalty"),
        (r"\bunauthorized transaction detected\b", "medium", "Fake security warning intended to lure user into fraudulent recovery steps"),
        (r"\bpermanently locked\b", "high", "Threatens irreversible loss of account")
    ]
    for pattern, severity, explanation in patterns:
        matched = find_matched_substring(pattern, text)
        if matched:
            evidence.append({
                "type": "THREAT_COERCION",
                "severity": severity,
                "matched_text": matched,
                "explanation": explanation
            })
    return evidence

def detect_credential_request(text: str) -> List[Dict[str, Any]]:
    """Detect solicitation of sensitive passwords, KYC docs, or banking PINs."""
    evidence = []
    patterns = [
        (r"\b(?:verify|update|complete) (?:your )?kyc\b", "high", "Fake KYC prompts are the #1 attack vector for Indian banking fraud"),
        (r"\b(?:enter|provide|confirm) (?:your )?(?:password|netbanking password|pin)\b", "high", "Legitimate institutions never request passwords or PINs over message or link"),
        (r"\bpan card|aadhaar card|ssn\b", "medium", "Solicits government identity numbers used for identity theft"),
        (r"\b(?:atm|debit card|credit card) pin\b", "high", "Direct request for ATM or card PIN, which banks never ask for"),
        (r"\bcvv(?: code)?\b", "high", "Requests 3-digit card security code")
    ]
    for pattern, severity, explanation in patterns:
        matched = find_matched_substring(pattern, text)
        if matched:
            evidence.append({
                "type": "CREDENTIAL_HARVESTING",
                "severity": severity,
                "matched_text": matched,
                "explanation": explanation
            })
    return evidence

def detect_otp_request(text: str) -> List[Dict[str, Any]]:
    """
    Detect attempts to intercept One-Time Passwords.
    Distinguishes genuine requests from legitimate security warnings ('do not share your OTP').
    """
    evidence = []
    
    # Check if the message is actually a security warning advising NOT to share OTP
    is_cautionary_warning = bool(re.search(
        r"\b(?:do not|never|don't|not)\s+(?:share|disclose|give|reveal)\b.*?\b(?:otp|password|pin|code)\b",
        text,
        re.IGNORECASE
    ))
    
    if is_cautionary_warning:
        # Legitimate warning advising against sharing - do not flag as an attack
        return evidence
        
    patterns = [
        (r"\b(?:share|send|enter|forward|give|provide)\s+(?:the|your|me|us|this)?\s*(?:(?:\d+[- ]?digit|secret)\s+)?(?:otp|one[- ]time password|verification code)\b", "high", "OTPs must NEVER be shared. Attackers use this to bypass 2FA and drain accounts"),
        (r"\bforward the (?:sms|code|message)\b", "high", "SMS forwarding enables total account takeover"),
        (r"\benter (?:your )?upi pin to (?:receive|accept|credit)\b", "high", "UPI PIN is only required to send money, never to receive. Classic payment fraud lure"),
        (r"\b(?:send|share) (?:your )?\d+[- ]digit (?:otp|code|pin)\b", "high", "Explicit solicitation of authentication token")
    ]
    for pattern, severity, explanation in patterns:
        matched = find_matched_substring(pattern, text)
        if matched:
            evidence.append({
                "type": "OTP_SOLICITATION",
                "severity": severity,
                "matched_text": matched,
                "explanation": explanation
            })
    return evidence

def detect_financial_request(text: str) -> List[Dict[str, Any]]:
    """Detect unexpected money requests, advance fees, or processing charges."""
    evidence = []
    patterns = [
        (r"\b(?:pay|transfer|send) (?:rs\.?|₹|\$)\s*\d+\b", "high", "Direct demand for unverified monetary transfer"),
        (r"\b(?:processing|registration|customs|delivery|activation) fee\b", "high", "Advance-fee fraud pattern: victim pays small fee to release larger sum or parcel"),
        (r"\bpaytm|phonepe|gpay|google pay|upi pin\b", "medium", "References payment apps; common in UPI request scams where victim is asked to approve payment"),
        (r"\bgift cards?|crypto|bitcoin|usdt\b", "high", "Demands irreversible, untraceable payment instruments")
    ]
    for pattern, severity, explanation in patterns:
        matched = find_matched_substring(pattern, text)
        if matched:
            evidence.append({
                "type": "FINANCIAL_SOLICITATION",
                "severity": severity,
                "matched_text": matched,
                "explanation": explanation
            })
    return evidence

def detect_impersonation(text: str, urls: List[str] = None) -> List[Dict[str, Any]]:
    """
    Detect claims of representing trusted institutions.
    Contextual: Only flags impersonation if accompanied by threats, unverified external links,
    or urgent action requests (not for routine benign debit notifications).
    """
    evidence = []
    
    # Context signals that elevate a brand mention to suspicious impersonation
    has_threat_or_urgency = bool(re.search(
        r"\b(?:alert|blocked|suspended|terminated|deactivated|kyc|verify|arrest|legal action|disconnect|seized|warning)\b",
        text,
        re.IGNORECASE
    ))
    has_external_links = bool(urls and len(urls) > 0)
    # Personal mobile numbers (starting with 6-9 in India or WhatsApp/Telegram handles)
    # Exclude standard official 1800/1860 toll-free numbers
    has_contact_urgency = bool(re.search(
        r"\b(?:call|contact|whatsapp|telegram)\s+(?:officer|executive|manager|us)?\s*(?:at|on)?\s*(?:\+?91[- ]?)?[6-9]\d{9}\b|\b(?:telegram|whatsapp)\s+@[a-zA-Z0-9_]+\b",
        text,
        re.IGNORECASE
    ))
    
    is_suspicious_context = has_threat_or_urgency or has_external_links or has_contact_urgency
    
    if not is_suspicious_context:
        # Benign mention like "SBI: ₹2,500 debited..." without threat or link is NOT impersonation
        return evidence
        
    for org_name, regex_list in IMPERSONATION_TARGETS:
        for r in regex_list:
            matched = find_matched_substring(r, text)
            if matched:
                evidence.append({
                    "type": "IMPERSONATION",
                    "severity": "medium",
                    "matched_text": matched,
                    "explanation": f"Invokes authority of trusted institution '{org_name}' in connection with urgent or unverified actions"
                })
                break
    return evidence

def detect_reward_claim(text: str) -> List[Dict[str, Any]]:
    """Detect fake lotteries, unexpected rewards, and too-good-to-be-true claims."""
    evidence = []
    patterns = [
        (r"\b(?:congratulations|you won|lucky winner|jackpot)\b", "high", "Unsolicited winning notification designed to exploit excitement"),
        (r"\b(?:claim (?:your )?(?:reward|cash prize|gift|bonus|crore|lakh))\b", "high", "Baiting tactic requiring victim to click or pay processing fee"),
        (r"\bguaranteed (?:returns|income|profit)\b", "high", "Ponzi/investment scam hallmark offering unrealistic zero-risk returns")
    ]
    for pattern, severity, explanation in patterns:
        matched = find_matched_substring(pattern, text)
        if matched:
            evidence.append({
                "type": "REWARD_BAIT",
                "severity": severity,
                "matched_text": matched,
                "explanation": explanation
            })
    return evidence

def detect_delivery_scam(text: str) -> List[Dict[str, Any]]:
    """Detect fake courier delivery and parcel rescheduling scams."""
    evidence = []
    patterns = [
        (r"\b(?:parcel|package|shipment) (?:could not be|failed to be) delivered\b", "high", "Common courier lure directing victim to a malicious phishing portal"),
        (r"\bpay (?:rs\.?|₹|\$)?\s*\d+ to (?:reschedule|release|deliver)\b", "high", "Classic phishing lure asking nominal charge to harvest credit/debit card numbers"),
        (r"\bupdate (?:your )?(?:address|delivery details)\b", "medium", "Attempts to capture personal address and contact data")
    ]
    for pattern, severity, explanation in patterns:
        matched = find_matched_substring(pattern, text)
        if matched:
            evidence.append({
                "type": "DELIVERY_SCAM",
                "severity": severity,
                "matched_text": matched,
                "explanation": explanation
            })
    return evidence

def detect_job_scam(text: str) -> List[Dict[str, Any]]:
    """Detect work-from-home, task-based, and fake recruitment scams."""
    evidence = []
    patterns = [
        (r"\b(?:part[- ]time job|work from home)\b", "medium", "Frequent lure targeting job seekers"),
        (r"\bearn (?:rs\.?|₹|\$)\s*\d+[- ]*(?:\d+)? (?:daily|per day|hourly)\b", "high", "Unrealistic daily payout promises for trivial tasks"),
        (r"\b(?:telegram|whatsapp) task|like (?:youtube|videos?)|google review\b", "high", "Well-known 'prepaid task' scam funneling victims into VIP deposit traps")
    ]
    for pattern, severity, explanation in patterns:
        matched = find_matched_substring(pattern, text)
        if matched:
            evidence.append({
                "type": "JOB_SCAM",
                "severity": severity,
                "matched_text": matched,
                "explanation": explanation
            })
    return evidence

def detect_suspicious_url(url_features_dict: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Translate extracted URL risk signals into structured evidence."""
    evidence = []
    for signal in url_features_dict.get("risk_signals", []):
        evidence.append({
            "type": f"URL_{signal['type']}",
            "severity": signal["severity"],
            "matched_text": url_features_dict.get("url", ""),
            "explanation": signal["explanation"]
        })
    return evidence

def detect_domain_mismatch(url_features_dict: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Flag brand impersonation where URL domain conflicts with claimed brand."""
    evidence = []
    for bm in url_features_dict.get("brand_mismatches", []):
        evidence.append({
            "type": "DOMAIN_MISMATCH",
            "severity": "high",
            "matched_text": url_features_dict.get("root_domain", ""),
            "explanation": bm["explanation"]
        })
    return evidence

def run_rule_engine(text: str, urls: List[str] = None) -> Dict[str, Any]:
    """
    Execute all rule checks on the given text and associated URLs.
    Returns composite rule score (0.0 to 1.0) and structured evidence list.
    """
    if urls is None:
        urls = []
        
    all_evidence: List[Dict[str, Any]] = []
    
    # Text-based rules
    all_evidence.extend(detect_urgency(text))
    all_evidence.extend(detect_threat(text))
    all_evidence.extend(detect_credential_request(text))
    all_evidence.extend(detect_otp_request(text))
    all_evidence.extend(detect_financial_request(text))
    all_evidence.extend(detect_impersonation(text, urls))
    all_evidence.extend(detect_reward_claim(text))
    all_evidence.extend(detect_delivery_scam(text))
    all_evidence.extend(detect_job_scam(text))
    
    # URL-based rules
    for u in urls:
        features = extract_url_features(u)
        all_evidence.extend(detect_suspicious_url(features))
        all_evidence.extend(detect_domain_mismatch(features))
        
    # Deduplicate evidence objects by type + matched_text
    seen = set()
    deduped_evidence = []
    for ev in all_evidence:
        key = (ev["type"], ev["matched_text"])
        if key not in seen:
            seen.add(key)
            deduped_evidence.append(ev)
            
    # Calculate deterministic rule score
    severity_weights = {
        "high": 0.30,
        "medium": 0.15,
        "low": 0.08
    }
    raw_score = sum(severity_weights.get(ev.get("severity", "low"), 0.08) for ev in deduped_evidence)
    rule_score = round(min(raw_score, 1.0), 4)
    
    return {
        "rule_score": rule_score,
        "evidence_count": len(deduped_evidence),
        "evidence": deduped_evidence
    }
