"""
Message linguistic and social engineering feature extraction for ScamShield AI.
Extracts psychological pressure cues, intent markers, and text statistics.
"""
import re
from typing import Dict, Any, List

def calculate_text_stats(text: str) -> Dict[str, Any]:
    """Calculate statistical and lexical metrics of the message."""
    if not text:
        return {
            "length": 0,
            "word_count": 0,
            "uppercase_ratio": 0.0,
            "exclamation_count": 0,
            "question_count": 0,
            "digit_count": 0,
            "currency_symbol_count": 0
        }
    
    length = len(text)
    words = text.split()
    word_count = len(words)
    uppercase_chars = sum(1 for c in text if c.isupper())
    uppercase_ratio = round(uppercase_chars / max(length, 1), 4)
    exclamation_count = text.count("!")
    question_count = text.count("?")
    digit_count = sum(1 for c in text if c.isdigit())
    currency_symbols = len(re.findall(r"[$€£₹¥]|(?:rs\.?|inr|usd|eur)\b", text, re.IGNORECASE))
    
    return {
        "length": length,
        "word_count": word_count,
        "uppercase_ratio": uppercase_ratio,
        "exclamation_count": exclamation_count,
        "question_count": question_count,
        "digit_count": digit_count,
        "currency_symbol_count": currency_symbols
    }

# Category indicator keyword lists with weights
CATEGORY_INDICATORS = {
    "urgency": [
        "immediately", "urgent", "today", "within 24 hours", "now", "hurry",
        "expires soon", "deadline", "limited time", "act fast", "right away",
        "instant", "quick", "asap", "without delay", "within 2 hours"
    ],
    "threat": [
        "blocked", "suspended", "deactivated", "terminated", "legal action",
        "arrest", "police", "court", "penalty", "fine", "freeze", "locked",
        "restricted", "permanently closed", "unauthorized transaction",
        "security breach", "law enforcement", "fbi", "cbi"
    ],
    "credential_request": [
        "verify kyc", "update kyc", "enter password", "provide password",
        "confirm credentials", "netbanking password", "login credentials",
        "security question", "pan card details", "aadhaar details",
        "ssn", "social security", "pin code", "atm pin", "cvv"
    ],
    "otp_request": [
        "share otp", "enter otp", "provide otp", "send otp", "one time password",
        "verification code", "sms code", "security code", "forward the code",
        "6-digit code", "do not share", "otp will expire"
    ],
    "financial_request": [
        "transfer money", "pay fee", "processing fee", "registration fee",
        "send money", "wire transfer", "gift card", "crypto", "bitcoin",
        "usdt", "deposit required", "refundable deposit", "reschedule fee",
        "customs duty", "clearance charge", "pay ₹", "pay $"
    ],
    "reward_lottery": [
        "congratulations", "you won", "lottery", "cash prize", "lucky winner",
        "jackpot", "claim reward", "free gift", "selected to receive",
        "exclusive bonus", "100% free", "guaranteed returns", "crore", "lakh"
    ],
    "delivery_scam": [
        "parcel", "package", "shipment", "courier", "delivery address",
        "failed delivery", "reschedule delivery", "customs clearance",
        "tracking number", "post office", "express delivery", "undelivered"
    ],
    "job_scam": [
        "work from home", "part time job", "earn daily", "earn ₹", "earn $",
        "no experience required", "daily payout", "telegram task", "youtube like",
        "google review task", "flexible hours", "instant hiring", "hr manager"
    ],
    "secrecy_pressure": [
        "do not tell anyone", "keep this confidential", "secret", "private matter",
        "do not hang up", "stay on the call", "inform nobody", "strictly confidential"
    ]
}

def extract_message_features(text: str) -> Dict[str, Any]:
    """
    Extract linguistic and social engineering score metrics from text.
    """
    text_lower = text.lower()
    stats = calculate_text_stats(text)
    
    category_scores: Dict[str, float] = {}
    matched_phrases: Dict[str, List[str]] = {}
    
    for category, phrases in CATEGORY_INDICATORS.items():
        found = [p for p in phrases if p in text_lower]
        matched_phrases[category] = found
        # Normalized score between 0.0 and 1.0
        score = min(len(found) * 0.35, 1.0)
        category_scores[category] = round(score, 3)
        
    # Composite social engineering intensity
    se_intensity = (
        category_scores["urgency"] * 0.20 +
        category_scores["threat"] * 0.25 +
        category_scores["credential_request"] * 0.25 +
        category_scores["otp_request"] * 0.20 +
        category_scores["secrecy_pressure"] * 0.10
    )
    
    return {
        "text_stats": stats,
        "category_scores": category_scores,
        "matched_phrases": matched_phrases,
        "social_engineering_intensity": round(min(se_intensity, 1.0), 3)
    }
