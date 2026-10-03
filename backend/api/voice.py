"""
Voice & Audio Note Analysis API Router for ScamShield AI.
Transcribes speech and routes through multi-layer scam detection.
"""
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
from backend.voice.transcribe import transcribe_audio_bytes
from backend.api.analyze import analyze_text_message, TextAnalysisRequest
from backend.ai.schemas import FullAnalysisResponse
from backend.config.settings import settings

router = APIRouter(prefix="/analyze", tags=["Voice Analysis"])

@router.post("/voice", response_model=FullAnalysisResponse)
async def analyze_voice_note(
    file: UploadFile = File(...),
    manual_transcript: Optional[str] = Form(""),
    language: str = Form("en")
):
    """
    Analyze uploaded voice note (audio file).
    Transcribes audio or uses user-supplied transcript for demonstration reliability.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="Uploaded audio file missing name")
        
    ext = "." + file.filename.split(".")[-1].lower() if "." in file.filename else ""
    if ext not in settings.ALLOWED_AUDIO_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported audio format '{ext}'. Supported formats: {', '.join(settings.ALLOWED_AUDIO_EXTENSIONS)}"
        )
        
    audio_bytes = await file.read()
    if len(audio_bytes) > settings.MAX_FILE_SIZE_BYTES:
        raise HTTPException(status_code=400, detail="Audio file exceeds maximum limit of 10 MB")
        
    transcribed_text, meta = transcribe_audio_bytes(
        audio_bytes=audio_bytes,
        filename=file.filename,
        manual_transcript=manual_transcript or ""
    )
    
    if not transcribed_text:
        raise HTTPException(
            status_code=422,
            detail="Could not transcribe audio. Please verify audio clarity or provide a transcript."
        )
        
    result = await analyze_text_message(TextAnalysisRequest(text=transcribed_text, language=language))
    result.signals.append({
        "type": "VOICE_TRANSCRIPTION",
        "severity": "info",
        "matched_text": transcribed_text[:80] + "...",
        "explanation": f"Speech-to-text generated via {meta.get('transcription_method', 'audio pipeline')}"
    })
    return result
