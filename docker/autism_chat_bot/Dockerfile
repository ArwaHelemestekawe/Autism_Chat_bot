FROM ghcr.io/astral-sh/uv:0.11.23-python3.11-trixie-slim


WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libavif-dev pkg-config \
    libjpeg-dev \
    gcc unzip zip \
    python3-dev \
    libxml2-dev \
    libxslt1-dev \
    libffi-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY src/requirments.txt ./src/requirments.txt
RUN uv pip install -r ./src/requirments.txt --system

COPY src/ ./src/


CMD ["uvicorn", "src.routes.main:app", "--host", "0.0.0.0", "--port", "8000","--workers","4"]