# Multi-stage Dockerfile for Astrological Intelligence Engine (V3.36)
FROM python:3.11-slim as builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ make libffi-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Final Runtime Image
FROM python:3.11-slim as runner

WORKDIR /app

COPY --from=builder /root/.local /root/.local
COPY . .

ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--threads", "2", "app:create_app()"]
