# ScamShield AI - Production Backend Container
# Multi-stage/Slim Python 3.11 image with OpenCV & ONNX Runtime support
FROM python:3.11-slim

# Prevent Python from buffering stdout/stderr and writing pyc files
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=10000 \
    HOST=0.0.0.0 \
    ENVIRONMENT=production

WORKDIR /app

# Install minimal OS dependencies for OpenCV, RapidOCR, and compilation
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    libgomp1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY backend/ ./backend/
COPY models/ ./models/
COPY samples/ ./samples/

# Expose container ports (Render default 10000 and legacy 8000)
EXPOSE 10000 8000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://127.0.0.1:${PORT:-10000}/api/health || exit 1

# Launch uvicorn listening on 0.0.0.0:$PORT with fallback to 10000
CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-10000}"]
