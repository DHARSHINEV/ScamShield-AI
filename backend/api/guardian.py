"""
Family Guardian API Router for generating shareable family protection alerts.
"""
from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import List, Optional

router = APIRouter(prefix="/guardian", tags=["Family Guardian"])

class GuardianRequest(BaseModel):
    message_snippet: str = Field(..., max_length=500)
    risk_level: str = "HIGH RISK"
    detected_scam_type: str = "Phishing / Fraud"
    language: str = "en"

class GuardianResponse(BaseModel):
    title: str
    headline: str
    bullet_warnings: List[str]
    shareable_text: str
    official_tip: str
    verified_badge: str

@router.post("", response_model=GuardianResponse)
async def generate_guardian_card(req: GuardianRequest):
    """
    Generate clean, share-ready warning card formatted for WhatsApp, SMS, or Telegram.
    """
    headline = "🚨 SCAM ALERT FOR FAMILY"
    bullet_warnings = [
        "⚠ Do NOT click the link",
        "⚠ Do NOT share OTP or PIN numbers",
        "⚠ Do NOT enter your bank password",
        "⚠ Verify directly through the official app or known website"
    ]
    
    snippet = req.message_snippet[:120] + ("..." if len(req.message_snippet) > 120 else "")
    
    shareable_text = (
        f"🚨 *SCAM ALERT FOR FAMILY*\n"
        f"A suspicious message was recently received and analyzed:\n\n"
        f"💬 _\"{snippet}\"_\n\n"
        f"🛑 *PROTECTION RULES:*\n"
        f"• ❌ Do NOT click any links\n"
        f"• ❌ NEVER share your 6-digit OTP or UPI PIN\n"
        f"• ❌ NEVER pay money to reschedule deliveries or update KYC\n"
        f"• ✅ Always verify directly through the official banking app\n\n"
        f"🛡️ *Checked by ScamShield AI* — Stay alert, stay safe!"
    )
    
    return GuardianResponse(
        title="ScamShield Family Guardian Alert",
        headline=headline,
        bullet_warnings=bullet_warnings,
        shareable_text=shareable_text,
        official_tip="In India, report cyber fraud at cybercrime.gov.in or call 1930.",
        verified_badge="Verified by ScamShield AI Multi-Signal Engine"
    )
