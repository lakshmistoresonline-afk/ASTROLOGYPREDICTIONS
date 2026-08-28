FROM python:3.11-slim-bookworm

# Install build dependencies for pyswisseph
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ make wget curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Download essential ephemeris data
RUN mkdir -p /app/ephe && \
    wget -q -O /app/ephe/seas_18.se1 https://github.com/aloistr/swisseph/raw/master/ephe/seas_18.se1 && \
    wget -q -O /app/ephe/semo_18.se1 https://github.com/aloistr/swisseph/raw/master/ephe/semo_18.se1 && \
    wget -q -O /app/ephe/sepl_18.se1 https://github.com/aloistr/swisseph/raw/master/ephe/sepl_18.se1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

ENV SE_EPHE_PATH=/app/ephe
ENV PORT=8000

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
