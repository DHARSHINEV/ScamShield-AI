"""
Tests for Scam Dojo interactive scenario and scoring logic.
"""
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_load_dojo_challenges():
    response = client.get("/api/dojo/challenges")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["total_challenges"] >= 10
    first = data["challenges"][0]
    assert "scenario" in first
    assert "message" in first
    assert "is_scam" not in first  # Ground truth hidden from public challenge payload

def test_dojo_answer_correct():
    payload = {
        "challenge_id": "dojo-01",
        "user_choice": "SUSPICIOUS",
        "current_streak": 2,
        "total_answered": 4,
        "total_correct": 3
    }
    response = client.post("/api/dojo/answer", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["is_correct"] is True
    assert data["updated_streak"] == 3
    assert data["updated_correct"] == 4
    assert len(data["explanation"]) > 0

def test_dojo_answer_incorrect():
    payload = {
        "challenge_id": "dojo-01",
        "user_choice": "SAFE",
        "current_streak": 5,
        "total_answered": 10,
        "total_correct": 9
    }
    response = client.post("/api/dojo/answer", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["is_correct"] is False
    assert data["updated_streak"] == 0
    assert data["updated_correct"] == 9
