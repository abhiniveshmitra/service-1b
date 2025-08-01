﻿FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y gcc g++ musl-dev libffi-dev && \
    rm -rf /var/lib/apt/lists/* && apt-get clean

# Install PyTorch
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu \
    torch>=2.1.0 torchvision>=0.16.0 torchaudio>=2.1.0

# Install ML packages
RUN pip install --no-cache-dir sentence-transformers>=2.4.0 transformers>=4.33.0 \
    huggingface_hub>=0.20.0 "numpy>=1.24.0,<1.25.0" "scipy>=1.11.0,<1.12.0" \
    "faiss-cpu>=1.7.4,<1.8.0" "requests>=2.31.0,<2.32.0" "pydantic>=2.3.0,<2.4.0"

# Copy everything in one operation (avoids individual COPY issues)
COPY . ./

# Create user and set permissions
RUN groupadd -r appuser && useradd -r -g appuser appuser && \
    mkdir -p logs && chown -R appuser:appuser /app

ENV PYTHONPATH=/app PYTHONUNBUFFERED=1 SERVICE=1B ROUND=round1b

USER appuser
CMD ["python", "-u", "app/main.py"]
