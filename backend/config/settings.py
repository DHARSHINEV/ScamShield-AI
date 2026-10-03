"""
ScamShield AI Configuration and Settings
"""
from pathlib import Path
from pydantic_settings import BaseSettings
from typing import Dict

BASE_DIR = Path(__file__).resolve().parent.parent.parent
BACKEND_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    PROJECT_NAME: str = "ScamShield AI"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "production"
    DEBUG: bool = False
    
    # API Settings
    API_PREFIX: str = "/api"
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000", "*"]
    
    # Thresholds for classification
    SAFE_THRESHOLD: float = 0.35      # 0.00 - 0.34 => SAFE
    SUSPICIOUS_THRESHOLD: float = 0.70 # 0.35 - 0.69 => SUSPICIOUS, >= 0.70 => HIGH RISK / SCAM
    
    # Fusion Weights (Configurable)
    # Default weighting when LLM is absent vs present
    WEIGHT_RULES: float = 0.35
    WEIGHT_URL: float = 0.30
    WEIGHT_ML: float = 0.35
    WEIGHT_SEMANTIC_AI: float = 0.0  # Boosted dynamically if external LLM key is active
    
    # Model storage paths
    MODELS_DIR: Path = BASE_DIR / "models"
    URL_MODEL_PATH: Path = BASE_DIR / "models" / "scam_url_model.joblib"
    MESSAGE_MODEL_PATH: Path = BASE_DIR / "models" / "scam_message_model.joblib"
    
    # AI / LLM Integration (Optional)
    OPENAI_API_KEY: str = ""
    GEMINI_API_KEY: str = ""
    LLM_PROVIDER: str = "local" # "openai", "gemini", or "local"
    LLM_MODEL: str = "gpt-4o-mini"
    
    # File limits
    MAX_FILE_SIZE_BYTES: int = 10 * 1024 * 1024  # 10 MB
    ALLOWED_IMAGE_EXTENSIONS: set[str] = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}
    ALLOWED_AUDIO_EXTENSIONS: set[str] = {".mp3", ".wav", ".m4a", ".ogg", ".webm"}

    model_config = {"env_file": ".env", "extra": "ignore"}

settings = Settings()
