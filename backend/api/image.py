"""
Vision & Image Analysis API Router for ScamShield AI.
Handles Screenshot OCR text extraction, visual layout inspection, and QR Code parsing.
"""
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
from backend.vision.image_analyzer import analyze_image_content
from backend.vision.qr import decode_qr_from_bytes
from backend.api.analyze import analyze_text_message, TextAnalysisRequest
from backend.ai.schemas import FullAnalysisResponse
from backend.config.settings import settings

router = APIRouter(prefix="/analyze", tags=["Image & QR Analysis"])

@router.post("/image", response_model=FullAnalysisResponse)
async def analyze_screenshot(
    file: UploadFile = File(...),
    language: str = Form("en"),
    manual_context: Optional[str] = Form("")
):
    """
    Upload a screenshot for RapidOCR text extraction, visual layout analysis, and scam detection.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="Uploaded file missing name")
        
    ext = "." + file.filename.split(".")[-1].lower() if "." in file.filename else ""
    if ext not in settings.ALLOWED_IMAGE_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported image format '{ext}'. Supported formats: {', '.join(settings.ALLOWED_IMAGE_EXTENSIONS)}"
        )
        
    image_bytes = await file.read()
    if len(image_bytes) > settings.MAX_FILE_SIZE_BYTES:
        raise HTTPException(status_code=400, detail="Image file exceeds maximum limit of 10 MB")
        
    img_analysis = analyze_image_content(image_bytes)
    extracted_text = img_analysis["extracted_text"].strip()
    
    # If manual context provided, merge
    if manual_context and manual_context.strip():
        combined_text = f"{extracted_text}\n\n[User Context]: {manual_context.strip()}".strip()
    else:
        combined_text = extracted_text
        
    if not combined_text:
        # Check if QR was found
        qr = img_analysis.get("qr_result", {})
        if qr.get("detected"):
            combined_text = f"Decoded QR code content: {qr.get('payload')}"
        else:
            raise HTTPException(
                status_code=422,
                detail="ScamShield couldn't extract any readable text or QR codes from this image. Please try a clearer screenshot or paste the message directly."
            )
            
    # Run full detection pipeline
    result = await analyze_text_message(TextAnalysisRequest(text=combined_text, language=language))
    
    # Append visual signals to result signals
    for vs in img_analysis.get("visual_signals", []):
        result.signals.append(vs)
        
    return result

@router.post("/qr", response_model=FullAnalysisResponse)
async def analyze_qr_code(
    file: UploadFile = File(...),
    language: str = Form("en")
):
    """
    Detect and decode QR code from image, then analyze its target URL or payload.
    Never automatically navigates to or opens suspicious URLs.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="Uploaded file missing name")
        
    image_bytes = await file.read()
    if len(image_bytes) > settings.MAX_FILE_SIZE_BYTES:
        raise HTTPException(status_code=400, detail="Image file exceeds maximum limit of 10 MB")
        
    qr_data = decode_qr_from_bytes(image_bytes)
    if not qr_data.get("detected"):
        raise HTTPException(
            status_code=422,
            detail="No QR code found in this image. Please ensure the QR code is centered, well-lit, and unblurred."
        )
        
    payload = qr_data.get("payload", "").strip()
    payload_type = qr_data.get("payload_type", "text")
    
    eval_text = f"Decoded QR destination ({payload_type}): {payload}"
    result = await analyze_text_message(TextAnalysisRequest(text=eval_text, language=language))
    
    result.signals.append({
        "type": "DECODED_QR_CODE",
        "severity": "info",
        "matched_text": payload,
        "explanation": f"Decoded destination: '{payload}'. Evaluated without following or navigating to the link."
    })
    return result
