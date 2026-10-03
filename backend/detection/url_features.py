"""
URL Feature Extraction & Analysis Engine for ScamShield AI.
Extracts lexical, structural, statistical, and brand-consistency features
without making live network requests.
"""
import math
import re
from urllib.parse import urlparse, parse_qs
from typing import Dict, Any, List, Tuple

# Suspicious TLDs commonly seen in phishing and spam campaigns
SUSPICIOUS_TLDS = {
    "xyz", "top", "work", "click", "loan", "zip", "gq", "tk", "ml", "cf", "ga",
    "cc", "vip", "buzz", "fit", "live", "country", "stream", "date", "racing",
    "win", "bid", "men", "icu", "rest", "cam", "monster", "cfd", "shop"
}

# Known URL shorteners
SHORTENER_DOMAINS = {
    "bit.ly", "tinyurl.com", "t.co", "is.gd", "buff.ly", "ow.ly", "goo.gl",
    "rebrand.ly", "cutt.ly", "trib.al", "shorturl.at", "tiny.cc", "rb.gy"
}

# High-profile brands frequently targeted by phishing
TARGETED_BRANDS = {
    "sbi": ["sbi.co.in", "onlinesbi.sbi", "onlinesbi.com", "statebankofindia.com"],
    "hdfc": ["hdfcbank.com", "hdfc.com"],
    "icici": ["icicibank.com"],
    "axis": ["axisbank.com"],
    "pnb": ["pnbindia.in"],
    "paytm": ["paytm.com"],
    "phonepe": ["phonepe.com"],
    "gpay": ["pay.google.com", "google.com"],
    "paypal": ["paypal.com"],
    "amazon": ["amazon.com", "amazon.in", "amazon.co.uk"],
    "apple": ["apple.com", "icloud.com"],
    "microsoft": ["microsoft.com", "live.com", "outlook.com", "office.com"],
    "netflix": ["netflix.com"],
    "google": ["google.com", "accounts.google.com"],
    "fedex": ["fedex.com"],
    "dhl": ["dhl.com"],
    "indiapost": ["indiapost.gov.in"],
    "incometax": ["incometax.gov.in"],
    "whatsapp": ["whatsapp.com", "wa.me"],
    "facebook": ["facebook.com", "fb.com"],
    "instagram": ["instagram.com"]
}

SUSPICIOUS_URL_KEYWORDS = [
    "verify", "verification", "secure", "security", "update", "kyc", "login",
    "signin", "sign-in", "banking", "account", "suspend", "confirm", "claim",
    "reward", "wallet", "blocked", "validate", "alert", "auth", "passcode",
    "refund", "unusual", "activate"
]

# IP Address regex (IPv4, basic IPv6, and octal/hex obfuscations)
IPV4_REGEX = re.compile(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
OCT_HEX_IP_REGEX = re.compile(r"^0x[0-9a-fA-F]+|0[0-7]+$")

def calculate_shannon_entropy(data: str) -> float:
    """Calculate the Shannon entropy of a string."""
    if not data:
        return 0.0
    entropy = 0.0
    length = len(data)
    char_counts: Dict[str, int] = {}
    for char in data:
        char_counts[char] = char_counts.get(char, 0) + 1
    for count in char_counts.values():
        p_x = count / length
        if p_x > 0:
            entropy -= p_x * math.log2(p_x)
    return round(entropy, 4)

def extract_domain_parts(netloc: str) -> Tuple[str, str, List[str]]:
    """Extract registered domain, TLD, and subdomains."""
    host = netloc.split(":")[0].lower() # strip port
    parts = host.split(".")
    if len(parts) >= 2:
        # Check two-part ccTLDs like co.in, gov.in, co.uk
        if len(parts) >= 3 and parts[-2] in ["co", "gov", "ac", "org", "net", "edu"] and len(parts[-1]) == 2:
            tld = f"{parts[-2]}.{parts[-1]}"
            root_domain = f"{parts[-3]}.{tld}"
            subdomains = parts[:-3]
        else:
            tld = parts[-1]
            root_domain = f"{parts[-2]}.{tld}"
            subdomains = parts[:-2]
    else:
        tld = ""
        root_domain = host
        subdomains = []
    return root_domain, tld, subdomains

def check_brand_mismatch(url: str, netloc: str, root_domain: str) -> List[Dict[str, str]]:
    """
    Detect if high-profile brand names appear in subdomains or path
    when the root domain does not belong to that brand.
    """
    mismatches = []
    url_lower = url.lower()
    netloc_lower = netloc.lower()
    
    for brand, official_domains in TARGETED_BRANDS.items():
        # Check if brand token appears in URL
        brand_pattern = rf"\b{re.escape(brand)}\b|[-_.]{re.escape(brand)}[-_.]|{re.escape(brand)}-|{re.escape(brand)}\."
        if re.search(brand_pattern, url_lower):
            # Check if root domain is actually legitimate for that brand
            is_legit = any(root_domain == od or root_domain.endswith("." + od) for od in official_domains)
            if not is_legit:
                mismatches.append({
                    "brand": brand.upper(),
                    "official_domain": official_domains[0],
                    "actual_domain": root_domain,
                    "explanation": f"URL mentions brand '{brand.upper()}' but domain '{root_domain}' is NOT an official domain for {brand.upper()}."
                })
    return mismatches

def extract_url_features(url: str) -> Dict[str, Any]:
    """
    Comprehensive feature extraction for a URL.
    Returns numeric feature vector dictionary and descriptive risk flags.
    """
    if not url.startswith(("http://", "https://")):
        url = "http://" + url
        
    parsed = urlparse(url)
    netloc = parsed.netloc or ""
    path = parsed.path or ""
    query = parsed.query or ""
    
    root_domain, tld, subdomains = extract_domain_parts(netloc)
    
    # Check IP address usage
    host_only = netloc.split(":")[0]
    is_ip = bool(IPV4_REGEX.match(host_only) or OCT_HEX_IP_REGEX.match(host_only))
    
    # Punycode check
    is_punycode = "xn--" in netloc.lower()
    
    # Shortener check
    is_shortener = host_only.lower() in SHORTENER_DOMAINS
    
    # TLD check
    is_suspicious_tld = tld.lower() in SUSPICIOUS_TLDS or any(p in SUSPICIOUS_TLDS for p in tld.lower().split("."))
    
    # Count special characters
    num_dots = url.count(".")
    num_hyphens = url.count("-")
    num_at = url.count("@")
    num_question = url.count("?")
    num_equals = url.count("=")
    num_digits = sum(c.isdigit() for c in url)
    num_percent = url.count("%")
    has_encoding = num_percent > 0
    
    # Entropy
    domain_entropy = calculate_shannon_entropy(netloc)
    path_entropy = calculate_shannon_entropy(path)
    
    # Suspicious keywords in URL
    matched_keywords = [kw for kw in SUSPICIOUS_URL_KEYWORDS if kw in url.lower()]
    
    # Brand mismatch
    brand_mismatches = check_brand_mismatch(url, netloc, root_domain)
    
    # Deep nesting
    path_segments = [p for p in path.split("/") if p]
    excessive_nesting = len(subdomains) >= 3 or len(path_segments) >= 5
    
    # Heuristic URL risk score (0.0 to 1.0)
    risk_score = 0.0
    risk_signals = []
    
    if is_ip:
        risk_score += 0.40
        risk_signals.append({
            "type": "IP_HOST",
            "severity": "high",
            "explanation": "Uses an IP address instead of a legitimate domain name"
        })
        
    if is_punycode:
        risk_score += 0.35
        risk_signals.append({
            "type": "PUNYCODE",
            "severity": "high",
            "explanation": "Uses Punycode (IDN homograph), often used to disguise lookalike domains"
        })
        
    if brand_mismatches:
        risk_score += 0.45
        for bm in brand_mismatches:
            risk_signals.append({
                "type": "BRAND_MISMATCH",
                "severity": "high",
                "explanation": bm["explanation"]
            })
            
    if is_suspicious_tld:
        risk_score += 0.25
        risk_signals.append({
            "type": "SUSPICIOUS_TLD",
            "severity": "medium",
            "explanation": f"Top-level domain (.{tld}) has high statistical association with abuse and phishing"
        })
        
    if is_shortener:
        risk_score += 0.20
        risk_signals.append({
            "type": "URL_SHORTENER",
            "severity": "medium",
            "explanation": "URL uses a link shortening service to mask the real destination"
        })
        
    if parsed.scheme == "http" and (matched_keywords or brand_mismatches or is_ip):
        risk_score += 0.15
        risk_signals.append({
            "type": "INSECURE_HTTP",
            "severity": "medium",
            "explanation": "Unencrypted HTTP connection for security/authentication sensitive keywords"
        })
        
    if num_hyphens >= 3:
        risk_score += 0.15
        risk_signals.append({
            "type": "HYPHENATED_DOMAIN",
            "severity": "low",
            "explanation": f"Multiple hyphens ({num_hyphens}) in URL commonly used to spoof brand names"
        })
        
    if len(matched_keywords) >= 2:
        risk_score += 0.20
        risk_signals.append({
            "type": "SUSPICIOUS_KEYWORDS",
            "severity": "medium",
            "explanation": f"Contains security-sensitive lure keywords: {', '.join(matched_keywords[:4])}"
        })
        
    if domain_entropy > 4.2:
        risk_score += 0.15
        risk_signals.append({
            "type": "HIGH_ENTROPY",
            "severity": "low",
            "explanation": f"Domain exhibits high randomness/entropy ({domain_entropy}), typical of DGA or disposable domains"
        })
        
    if num_at > 0:
        risk_score += 0.30
        risk_signals.append({
            "type": "EMBEDDED_AT_SYMBOL",
            "severity": "high",
            "explanation": "URL contains '@' symbol which can redirect credentials or trick browser parsers"
        })
        
    risk_score = min(max(risk_score, 0.0), 1.0)
    
    return {
        "url": url,
        "root_domain": root_domain,
        "tld": tld,
        "subdomains": subdomains,
        "is_https": parsed.scheme == "https",
        "is_ip": is_ip,
        "is_shortener": is_shortener,
        "is_punycode": is_punycode,
        "is_suspicious_tld": is_suspicious_tld,
        "length": len(url),
        "domain_length": len(netloc),
        "path_length": len(path),
        "query_length": len(query),
        "num_subdomains": len(subdomains),
        "num_dots": num_dots,
        "num_hyphens": num_hyphens,
        "num_digits": num_digits,
        "num_params": len(parse_qs(query)),
        "has_encoding": has_encoding,
        "domain_entropy": domain_entropy,
        "path_entropy": path_entropy,
        "matched_keywords": matched_keywords,
        "brand_mismatches": brand_mismatches,
        "excessive_nesting": excessive_nesting,
        "risk_score": round(risk_score, 4),
        "risk_signals": risk_signals
    }
