"""
Tests for URL feature extraction and brand mismatch detection.
"""
import pytest
from backend.detection.url_features import extract_url_features
from backend.safety.sanitization import extract_urls

def test_extract_urls():
    text = "Visit https://sbi-verify-secure.xyz or check http://192.168.1.1/login today"
    urls = extract_urls(text)
    assert len(urls) == 2
    assert "https://sbi-verify-secure.xyz" in urls
    assert "http://192.168.1.1/login" in urls

def test_suspicious_url_ip_address():
    res = extract_url_features("http://192.168.1.50/login/bank")
    assert res["is_ip"] is True
    assert res["risk_score"] >= 0.40
    signal_types = [s["type"] for s in res["risk_signals"]]
    assert "IP_HOST" in signal_types

def test_brand_mismatch_detection():
    # Brand 'sbi' used on third-party domain 'sbi-verify-secure.xyz'
    res = extract_url_features("https://sbi-verify-secure.xyz")
    assert len(res["brand_mismatches"]) >= 1
    assert res["brand_mismatches"][0]["brand"] == "SBI"
    assert res["is_suspicious_tld"] is True
    assert res["risk_score"] >= 0.60

def test_legitimate_url_safe():
    res = extract_url_features("https://www.sbi.co.in/portal/web/home")
    assert res["is_ip"] is False
    assert res["is_suspicious_tld"] is False
    assert len(res["brand_mismatches"]) == 0
    assert res["risk_score"] < 0.20
