"""
Local High-Performance OCR Engine for ScamShield AI.
Uses RapidOCR (ONNX-accelerated) for offline screenshot text extraction.
"""
import io
import numpy as np
from PIL import Image
from typing import Tuple, List, Dict, Any

_OCR_ENGINE = None

def get_ocr_engine():
    """Lazy initialize RapidOCR engine."""
    global _OCR_ENGINE
    if _OCR_ENGINE is None:
        try:
            from rapidocr_onnxruntime import RapidOCR
            _OCR_ENGINE = RapidOCR()
        except Exception:
            _OCR_ENGINE = False
    return _OCR_ENGINE

def extract_text_from_image(image_bytes: bytes) -> Tuple[str, List[Dict[str, Any]], bool]:
    """
    Extract text and bounding segments from image bytes.
    Returns: (extracted_text, detected_boxes, is_success)
    """
    engine = get_ocr_engine()
    if not engine:
        return "", [], False
        
    try:
        pil_img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        img_array = np.array(pil_img)
        
        results, elapse = engine(img_array)
        if not results:
            return "", [], True
            
        lines = []
        boxes = []
        for item in results:
            box, text, score = item
            lines.append(text)
            boxes.append({
                "text": text,
                "confidence": round(float(score), 3),
                "box": box
            })
            
        full_text = "\n".join(lines)
        return full_text, boxes, True
    except Exception as e:
        return "", [], False
