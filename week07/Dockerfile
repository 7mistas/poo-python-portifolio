FROM python:3.11-slim AS base

LABEL maintainer="mista.ayo7@gmail.com"
LABEL description="ChatAWS = API de mensagens com autenticação JWT"
LABEL version="1.0.0"

WORKDIR /app

ENV PYHTHODONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

RUN mkdir -p /app/data &&\
    mkdir -p /app/logs

RUN useradd -m -u 1000 chatuser && \
    chown -R chatuser:chatuser /app

USER chatuser

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/health')"

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "app:app"]

