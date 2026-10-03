"""
Input sanitization and safety checks for ScamShield AI.
Ensures no code execution, prevents SSRF by never blindly visiting links,
and redacts sensitive credentials if inadvertently submitted.
"""
import re
from urllib.parse import urlparse
from typing import List, Tuple

# Patterns for sensitive credentials to redact for privacy
SENSITIVE_PATTERNS = [
    (re.compile(r"\b(?:\d[ -]*?){13,16}\b"), "[REDACTED_CARD_NUMBER]"),
    (re.compile(r"\b(?:otp|code|pin)[:\s=]+(\d{4,8})\b", re.IGNORECASE), "otp: [REDACTED_OTP]"),
    (re.compile(r"\b(?:password|passwd|pwd)[:\s=]+([^\s,;]+)", re.IGNORECASE), "password: [REDACTED_SECRET]"),
    (re.compile(r"\b(?:cvv|cvc)[:\s=]+(\d{3,4})\b", re.IGNORECASE), "cvv: [REDACTED_CVV]"),
]

URL_REGEX = re.compile(
    r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))",
    re.IGNORECASE
)

def sanitize_text(text: str, max_length: int = 10000) -> str:
    """Sanitize raw text input and enforce length limit."""
    if not text:
        return ""
    # Strip null bytes and non-printable control chars except standard newlines/tabs
    cleaned = "".join(c for c in text if c == '\n' or c == '\r' or c == '\t' or ord(c) >= 32)
    return cleaned[:max_length].strip()

def redact_sensitive_info(text: str) -> Tuple[str, bool]:
    """
    Redact credit cards, OTPs, and passwords from logs/processing.
    Returns (redacted_text, was_redacted).
    """
    redacted = text
    found = False
    for pattern, replacement in SENSITIVE_PATTERNS:
        new_text, count = re.subn(pattern, replacement, redacted)
        if count > 0:
            found = True
            redacted = new_text
    return redacted, found

def extract_urls(text: str) -> List[str]:
    """
    Safely extract all URLs from text.
    Ensures URLs start with a scheme for consistent parsing.
    """
    matches = URL_REGEX.findall(text)
    urls = []
    for match in matches:
        raw_url = match[0] if isinstance(match, tuple) else match
        raw_url = raw_url.strip(".,;:)'\"")
        if not raw_url.startswith(("http://", "https://")):
            # Check if looks like a domain
            if "." in raw_url:
                raw_url = "http://" + raw_url
            else:
                continue
        urls.append(raw_url)
    return list(dict.fromkeys(urls))  # deduplicate preserving order

def is_safe_url_syntax(url_str: str) -> bool:
    """Check if URL string is syntactically valid without requesting network."""
    try:
        parsed = urlparse(url_str)
        return bool(parsed.scheme and (parsed.netloc or parsed.path))
    except Exception:
        return False
