"""
Scam Dojo API Router for interactive gamified cybersecurity training.
"""
import json
from pathlib import Path
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

router = APIRouter(prefix="/dojo", tags=["Scam Dojo"])

SCENARIOS_FILE = Path(__file__).resolve().parent.parent.parent / "samples" / "dojo" / "scenarios.json"

def load_scenarios() -> List[Dict[str, Any]]:
    if not SCENARIOS_FILE.exists():
        return []
    with open(SCENARIOS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

class AnswerRequest(BaseModel):
    challenge_id: str
    user_choice: str = Field(..., description="'SAFE' or 'SUSPICIOUS'")
    current_streak: int = 0
    total_answered: int = 0
    total_correct: int = 0

class AnswerResponse(BaseModel):
    challenge_id: str
    is_correct: bool
    correct_classification: str
    explanation: List[str]
    key_takeaway: str
    updated_streak: int
    updated_score: int
    updated_correct: int
    total_answered: int
    accuracy_percentage: int
    skill_level: str

@router.get("/challenges")
async def get_challenges():
    """
    Get all curated Dojo challenges.
    Hides ground truth verdict from client to preserve interactive challenge integrity.
    """
    scenarios = load_scenarios()
    public_challenges = []
    for s in scenarios:
        public_challenges.append({
            "id": s["id"],
            "level": s["level"],
            "level_title": s["level_title"],
            "difficulty": s["difficulty"],
            "category": s["category"],
            "scenario": s["scenario"],
            "message": s["message"],
            "url": s.get("url", "")
        })
    return {
        "status": "success",
        "total_challenges": len(public_challenges),
        "challenges": public_challenges
    }

@router.post("/answer", response_model=AnswerResponse)
async def submit_answer(req: AnswerRequest):
    """
    Evaluate user's assessment and return verified breakdown and progression.
    """
    scenarios = load_scenarios()
    target = next((s for s in scenarios if s["id"] == req.challenge_id), None)
    if not target:
        raise HTTPException(status_code=404, detail="Challenge ID not found")
        
    actual_is_scam = target["is_scam"]
    user_chose_scam = req.user_choice.strip().upper() == "SUSPICIOUS"
    
    is_correct = (user_chose_scam == actual_is_scam)
    
    new_streak = req.current_streak + 1 if is_correct else 0
    new_correct = req.total_correct + (1 if is_correct else 0)
    new_total = req.total_answered + 1
    accuracy = int(round((new_correct / max(new_total, 1)) * 100))
    
    # Calculate score: 100 base points per correct + 25 * streak bonus
    base_score = 100 if is_correct else 0
    streak_bonus = (new_streak * 25) if is_correct else 0
    earned = base_score + streak_bonus
    
    # Skill level progression
    if new_correct >= 10 and accuracy >= 85:
        skill_level = "Cyber Guardian (Advanced)"
    elif new_correct >= 5:
        skill_level = "Threat Hunter (Intermediate)"
    else:
        skill_level = "Vigilant Rookie (Beginner)"
        
    return AnswerResponse(
        challenge_id=target["id"],
        is_correct=is_correct,
        correct_classification="SUSPICIOUS" if actual_is_scam else "SAFE",
        explanation=target["explanation"],
        key_takeaway=target["key_takeaway"],
        updated_streak=new_streak,
        updated_score=earned,
        updated_correct=new_correct,
        total_answered=new_total,
        accuracy_percentage=accuracy,
        skill_level=skill_level
    )
