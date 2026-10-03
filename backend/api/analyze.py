"""
Core Analysis API Router for ScamShield AI.
Integrates Rules, URL Heuristics, ML Classifier, AI Semantic Layer,
and TrustLens Evidence Generation.
"""
import time
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

from backend.safety.sanitization import sanitize_text, redact_sensitive_info, extract_urls, is_safe_url_syntax
from backend.detection.rules import run_rule_engine
from backend.detection.url_features import extract_url_features
from backend.detection.message_features import extract_message_features
from backend.detection.classifier import predict_scam_probability
from backend.detection.fusion import fuse_scores, calculate_risk_breakdown
from backend.detection.evidence import generate_evidence_cards, generate_red_flags, generate_action_plan
from backend.detection.multilingual import get_localized_explanations
from backend.ai.analyzer import run_semantic_analysis
from backend.ai.schemas import FullAnalysisResponse, AnalysisMetadata, EvidenceCardItem, RedFlagItem, ActionPlanItem

router = APIRouter(prefix="/analyze", tags=["Analysis"])

class TextAnalysisRequest(BaseModel):
    text: str = Field(..., min_length=2, max_length=10000, description="Message or communication text to evaluate")
    language: str = Field("en", description="Preferred localization language code")

class URLAnalysisRequest(BaseModel):
    url: str = Field(..., min_length=3, max_length=2048, description="URL to evaluate")
    language: str = Field("en", description="Preferred localization language code")

@router.get("/demo-cases")
async def get_demo_cases():
    """
    Returns curated, realistic simulated demo cases for reliable hackathon judging.
    Clearly labeled as simulated examples.
    """
    return [
        {
            "id": "demo-sbi-kyc",
            "title": "Bank KYC Phishing (High Risk)",
            "category": "bank_phishing",
            "text": "🚨 SBI ALERT: Your account will be blocked today. Verify your KYC immediately: https://sbi-verify-secure.xyz",
            "description": "Urgent deadline, KYC lure, and brand spoofing on an untrusted .xyz domain."
        },
        {
            "id": "demo-parcel-payment",
            "title": "Fake Parcel Micro-Payment (High Risk)",
            "category": "delivery_scam",
            "text": "India Post: Your package #IN78219 could not be delivered due to wrong house address. Pay ₹25 redelivery fee to avoid return: http://indiapost-parcel-update.com/track",
            "description": "Exploits routine parcel delivery with ₹25 fee to harvest debit card numbers."
        },
        {
            "id": "demo-job-scam",
            "title": "Work-From-Home Task Scam (High Risk)",
            "category": "job_scam",
            "text": "Congratulations! You are selected for YouTube Video Like & Google Review task. Earn ₹4,500 daily. Payouts every 3 hours. Contact Telegram @HrOfficerTask26 to receive ₹500 joining bonus.",
            "description": "Unrealistic payout for trivial tasks, Telegram funneling, and advance fee patterns."
        },
        {
            "id": "demo-customer-support",
            "title": "Fake WhatsApp Customer Support (Suspicious)",
            "category": "fake_support",
            "text": "Dear customer, your refund is in progress. Kindly install QuickSupport remote application and share your 9-digit code with our executive to approve your refund.",
            "description": "Screen sharing APK request disguised as helpful customer support."
        },
        {
            "id": "demo-legit-bank",
            "title": "Legitimate Bank Transaction (Safe)",
            "category": "legitimate_bank",
            "text": "SBI: ₹2,500.00 debited from A/C ...8902 on 03-Oct-26 at ATM-MG ROAD. Available balance ₹34,210.50. Call 18001234 if not done by you.",
            "description": "Official transaction notification with masked digits, contextual location, and official toll-free dispute number."
        },
        {
            "id": "demo-legit-delivery",
            "title": "Legitimate Courier Out for Delivery (Safe)",
            "category": "legitimate_delivery",
            "text": "BlueDart: Your Amazon order with AWB #849102941 is out for delivery today with courier associate Suresh. Share delivery PIN 4910 ONLY at the time of receiving the physical shipment.",
            "description": "Standard delivery notification with clear instructions to provide PIN only upon receiving the physical package."
        }
    ]

@router.post("/text", response_model=FullAnalysisResponse)
async def analyze_text_message(req: TextAnalysisRequest):
    """
    Complete multi-layered analysis of a text message:
    Sanitization -> URL Extraction -> Rule Engine -> Feature ML -> AI Semantics -> Score Fusion -> TrustLens Evidence
    """
    start_time = time.time()
    
    # 1. Sanitize & Redact
    cleaned_text = sanitize_text(req.text)
    sanitized_text, had_redaction = redact_sensitive_info(cleaned_text)
    
    if not sanitized_text:
        raise HTTPException(status_code=400, detail="Input text cannot be empty or only whitespace")
        
    # 2. Extract URLs
    urls = extract_urls(sanitized_text)
    
    # 3. Rule Engine
    rule_results = run_rule_engine(sanitized_text, urls)
    rule_score = rule_results["rule_score"]
    raw_evidence = rule_results["evidence"]
    
    # 4. URL Feature Engine (if URLs present)
    url_score = None
    primary_url_features = None
    if urls:
        # Use worst URL score
        all_url_feats = [extract_url_features(u) for u in urls]
        all_url_scores = [f["risk_score"] for f in all_url_feats]
        url_score = max(all_url_scores) if all_url_scores else 0.0
        primary_url_features = max(all_url_feats, key=lambda f: f["risk_score"])
        
    # 5. Message Feature Engine
    msg_feats = extract_message_features(sanitized_text)
    
    # 6. ML Classifier Pipeline
    ml_result = predict_scam_probability(sanitized_text, urls[0] if urls else None)
    ml_score = ml_result["p_scam"]
    
    # 7. AI Semantic Analyzer (with deterministic fallback)
    semantic_result, ai_provider = await run_semantic_analysis(sanitized_text, urls, raw_evidence)
    semantic_score = semantic_result.risk_score
    
    # 8. Score Fusion
    fusion = fuse_scores(
        rule_score=rule_score,
        url_score=url_score,
        ml_score=ml_score,
        semantic_score=semantic_score
    )
    final_score = fusion["final_risk_score"]
    classification = fusion["classification"]
    
    # 9. Risk Breakdown
    risk_breakdown = calculate_risk_breakdown(
        rule_evidence=raw_evidence,
        url_features=primary_url_features,
        message_features=msg_feats,
        rule_score=rule_score,
        ml_score=ml_score
    )
    
    # 10. TrustLens Evidence & Red Flags
    evidence_cards = generate_evidence_cards(raw_evidence)
    red_flags = generate_red_flags(sanitized_text, raw_evidence)
    action_plan = generate_action_plan(classification, raw_evidence, urls)
    
    # 11. Multilingual Support
    multilingual = get_localized_explanations(classification)
    
    latency = round((time.time() - start_time) * 1000, 2)
    
    metadata = AnalysisMetadata(
        rules_engine=True,
        ml_classifier=True,
        semantic_ai=ai_provider != "deterministic_local_engine",
        ai_provider=ai_provider,
        latency_ms=latency
    )
    
    return FullAnalysisResponse(
        classification=classification,
        risk_score=final_score,
        percentage=fusion["percentage"],
        scam_type=semantic_result.scam_type,
        summary=semantic_result.summary,
        risk_breakdown=risk_breakdown,
        signals=raw_evidence,
        evidence_cards=[EvidenceCardItem(**c) for c in evidence_cards],
        red_flags=[RedFlagItem(**rf) for rf in red_flags],
        action_plan=[ActionPlanItem(**a) for a in action_plan],
        multilingual=multilingual,
        analysis_metadata=metadata,
        extracted_urls=urls,
        sanitized_input=sanitized_text,
        had_sensitive_redaction=had_redaction
    )

@router.post("/url", response_model=FullAnalysisResponse)
async def analyze_single_url(req: URLAnalysisRequest):
    """
    Dedicated endpoint for deep URL structural and brand analysis.
    """
    cleaned_url = req.url.strip()
    if not is_safe_url_syntax(cleaned_url):
        raise HTTPException(status_code=400, detail="Invalid URL format. Please provide a valid domain or link.")
        
    return await analyze_text_message(TextAnalysisRequest(
        text=f"Direct link inspection: {cleaned_url}",
        language=req.language
    ))
