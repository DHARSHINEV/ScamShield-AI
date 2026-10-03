"""
Tests for Rule Engine detection capabilities.
"""
import pytest
from backend.detection.rules import (
    detect_urgency,
    detect_threat,
    detect_credential_request,
    detect_otp_request,
    detect_financial_request,
    run_rule_engine
)

def test_detect_urgency_positive():
    text = "Your account will be blocked today. Act immediately or within 24 hours."
    evidence = detect_urgency(text)
    assert len(evidence) >= 2
    types = [e["type"] for e in evidence]
    assert "URGENCY" in types

def test_detect_urgency_negative():
    text = "The bank branch will be open on regular working days from 10 AM to 4 PM."
    evidence = detect_urgency(text)
    assert len(evidence) == 0

def test_detect_threat():
    text = "Your account has been suspended due to an unauthorized transaction. Avoid digital arrest."
    evidence = detect_threat(text)
    assert len(evidence) >= 1
    assert any(e["severity"] == "high" for e in evidence)

def test_detect_credential_request():
    text = "Please verify your KYC and enter your netbanking password to continue."
    evidence = detect_credential_request(text)
    assert len(evidence) >= 1
    types = [e["type"] for e in evidence]
    assert "CREDENTIAL_HARVESTING" in types

def test_detect_otp_request():
    text = "Share the 6-digit OTP code sent to your phone to confirm your transaction."
    evidence = detect_otp_request(text)
    assert len(evidence) >= 1
    assert any("OTP" in e["type"] for e in evidence)

def test_detect_financial_request():
    text = "Pay processing fee of ₹1,500 via crypto or gift card."
    evidence = detect_financial_request(text)
    assert len(evidence) >= 1

def test_run_rule_engine_composite():
    text = "🚨 SBI ALERT: Your account will be blocked today. Verify your KYC immediately: https://sbi-verify-secure.xyz"
    res = run_rule_engine(text, ["https://sbi-verify-secure.xyz"])
    assert res["rule_score"] >= 0.70
    assert res["evidence_count"] >= 3
