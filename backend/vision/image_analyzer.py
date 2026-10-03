"""
Unified Screenshot & Image Analysis Pipeline for ScamShield AI.
Combines RapidOCR text extraction, QR code decoding, and visual threat cues.
"""
from typing import Dict, Any, List
from backend.vision.ocr import extract_text_from_image
from backend.vision.qr import decode_qr_from_bytes
from backend.safety.sanitization import extract_urls

def analyze_image_content(image_bytes: bytes) -> Dict[str, Any]:
    """
    Run complete multi-modal visual inspection:
    1. Check for QR code
    2. Run OCR to extract text
    3. Extract URLs found in text
    4. Detect visual phishing layout indicators (login forms, payment prompts, bank logos)
    """
    # 1. QR Code Check
    qr_result = decode_qr_from_bytes(image_bytes)
    
    # 2. OCR Text Extraction
    ocr_text, text_boxes, ocr_success = extract_text_from_image(image_bytes)
    
    # 3. Extract URLs from OCR text + QR
    urls = extract_urls(ocr_text)
    if qr_result.get("detected") and qr_result.get("payload_type") == "url":
        urls.append(qr_result["payload"])
    urls = list(dict.fromkeys(urls))
    
    # 4. Visual phishing layout cues
    visual_signals = []
    text_lower = ocr_text.lower()
    
    if any(k in text_lower for k in ["login", "sign in", "password", "username"]):
        visual_signals.append({
            "type": "LOGIN_FORM_PRESENT",
            "severity": "medium",
            "explanation": "Image contains a login / credential submission prompt"
        })
        
    if any(k in text_lower for k in ["kyc", "pan card", "aadhaar", "update kyc"]):
        visual_signals.append({
            "type": "KYC_VERIFICATION_PROMPT",
            "severity": "high",
            "explanation": "Visual layout mimics bank KYC update dialog"
        })
        
    if any(k in text_lower for k in ["pay ", "payment", "upi", "gpay", "phonepe", "paytm", "scan to pay"]):
        visual_signals.append({
            "type": "PAYMENT_REQUEST_INTERFACE",
            "severity": "medium",
            "explanation": "Visual interface solicits immediate financial transaction"
        })
        
    if qr_result.get("detected") and qr_result.get("payload_type") == "upi_payment":
        visual_signals.append({
            "type": "EMBEDDED_UPI_QR",
            "severity": "high",
            "explanation": "Image contains a direct UPI payment QR code commonly used in marketplace / OLX scams"
        })

    return {
        "ocr_success": ocr_success,
        "extracted_text": ocr_text,
        "text_boxes_count": len(text_boxes),
        "qr_result": qr_result,
        "extracted_urls": urls,
        "visual_signals": visual_signals
    }
