"""
Pydantic Schemas for AI Semantic Analyzer & API Response Payloads.
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class RedFlagItem(BaseModel):
    text: str = Field(..., description="Suspicious substring")
    reason: str = Field(..., description="Explanation of why this is suspicious")
    severity: str = Field("medium", description="Severity: low, medium, high")

class ActionPlanItem(BaseModel):
    step: str
    instruction: str
    priority: str = "medium"

class EvidenceCardItem(BaseModel):
    id: str
    type: str
    title: str
    severity: str
    matched_text: str
    explanation: str

class SemanticAIResult(BaseModel):
    classification: str = Field(..., description="SCAM, SUSPICIOUS, or SAFE")
    risk_score: float = Field(..., ge=0.0, le=1.0, description="Semantic risk score 0.0 to 1.0")
    scam_type: str = Field(..., description="Category, e.g., phishing, lottery, job_scam, bank_fraud, legitimate")
    summary: str = Field(..., description="Brief explainable summary")
    red_flags: List[RedFlagItem] = Field(default_factory=list)
    recommended_actions: List[str] = Field(default_factory=list)

class AnalysisMetadata(BaseModel):
    rules_engine: bool = True
    ml_classifier: bool = True
    semantic_ai: bool = False
    ai_provider: str = "deterministic_local_engine"
    latency_ms: float = 0.0

class FullAnalysisResponse(BaseModel):
    classification: str # "SAFE" | "SUSPICIOUS" | "HIGH RISK"
    risk_score: float
    percentage: int
    scam_type: str
    summary: str
    risk_breakdown: Dict[str, float]
    signals: List[Dict[str, Any]]
    evidence_cards: List[EvidenceCardItem]
    red_flags: List[RedFlagItem]
    action_plan: List[ActionPlanItem]
    multilingual: Dict[str, Dict[str, str]] = Field(default_factory=dict)
    analysis_metadata: AnalysisMetadata
    extracted_urls: List[str] = Field(default_factory=list)
    sanitized_input: str = ""
    had_sensitive_redaction: bool = False
