"""
Comprehensive API integration tests for ScamShield AI.
"""
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "subsystems" in data
    assert data["subsystems"]["rule_engine"] == "operational"

def test_demo_cases_endpoint():
    response = client.get("/api/analyze/demo-cases")
    assert response.status_code == 200
    cases = response.json()
    assert len(cases) >= 5

def test_analyze_scam_text():
    payload = {
        "text": "🚨 SBI ALERT: Your account will be blocked today. Verify your KYC immediately: https://sbi-verify-secure.xyz",
        "language": "en"
    }
    response = client.post("/api/analyze/text", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["classification"] in ["HIGH RISK", "SUSPICIOUS"]
    assert data["risk_score"] >= 0.70
    assert len(data["evidence_cards"]) >= 2
    assert len(data["red_flags"]) >= 1
    assert len(data["action_plan"]) >= 2
    assert "risk_breakdown" in data
    assert "ta" in data["multilingual"]

def test_analyze_safe_text():
    payload = {
        "text": "SBI: ₹2,500.00 debited from A/C ...8902 on 03-Oct-26 at ATM-MG ROAD. Available balance ₹34,210.50. Call 18001234 if not done by you.",
        "language": "en"
    }
    response = client.post("/api/analyze/text", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["classification"] == "SAFE"
    assert data["risk_score"] < 0.35

def test_analyze_empty_text_error():
    payload = {"text": "   "}
    response = client.post("/api/analyze/text", json=payload)
    assert response.status_code in [400, 422]

def test_guardian_endpoint():
    payload = {
        "message_snippet": "Your account is suspended. Verify KYC immediately.",
        "risk_level": "HIGH RISK",
        "detected_scam_type": "phishing"
    }
    response = client.post("/api/guardian", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "SCAM ALERT FOR FAMILY" in data["headline"]
    assert len(data["bullet_warnings"]) >= 3
    assert len(data["shareable_text"]) > 20
