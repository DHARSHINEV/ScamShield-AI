"""
QR Code Detection & Parsing Engine for ScamShield AI.
Uses OpenCV's QRCodeDetector to safely extract QR payloads (URLs, UPI payment links, text)
WITHOUT ever visiting or triggering network requests.
"""
import io
import cv2
import numpy as np
from PIL import Image
from typing import Dict, Any, Optional

def decode_qr_from_bytes(image_bytes: bytes) -> Dict[str, Any]:
    """
    Detect and decode QR codes within an image.
    Returns payload, type of QR (URL, UPI, plain text), and decoded status.
    """
    try:
        pil_img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        img_array = np.array(pil_img)
        # OpenCV uses BGR
        cv_img = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        
        detector = cv2.QRCodeDetector()
        data, points, straight_qrcode = detector.detectAndDecode(cv_img)
        
        if not data:
            # Try multi-detector or grayscale
            gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
            data, points, straight_qrcode = detector.detectAndDecode(gray)
            
        if not data:
            return {
                "detected": False,
                "payload": "",
                "payload_type": "none",
                "message": "No QR code detected in the uploaded image."
            }
            
        payload = data.strip()
        payload_type = "text"
        
        if payload.startswith(("http://", "https://")):
            payload_type = "url"
        elif payload.startswith("upi://pay"):
            payload_type = "upi_payment"
        elif payload.startswith("WIFI:"):
            payload_type = "wifi_config"
        elif payload.startswith("mailto:"):
            payload_type = "email"
            
        return {
            "detected": True,
            "payload": payload,
            "payload_type": payload_type,
            "message": f"Successfully decoded {payload_type} QR code."
        }
    except Exception as e:
        return {
            "detected": False,
            "payload": "",
            "payload_type": "error",
            "message": f"QR decoding error: {str(e)}"
        }
