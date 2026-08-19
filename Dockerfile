FROM python:3.11-slim

LABEL maintainer="Jyotish Dashboard"
LABEL description="Vedic Astrology Kundli Dashboard"

# System deps for pyswisseph + ephem build
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ make wget curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Download Swiss Ephemeris data files (GitHub Mirror — reliable)
RUN mkdir -p /app/ephe && \
    wget -q -O /app/ephe/seas_18.se1 \
        https://github.com/aloistr/swisseph/raw/master/ephe/seas_18.se1 && \
    wget -q -O /app/ephe/semo_18.se1 \
        https://github.com/aloistr/swisseph/raw/master/ephe/semo_18.se1 && \
    wget -q -O /app/ephe/sepl_18.se1 \
        https://github.com/aloistr/swisseph/raw/master/ephe/sepl_18.se1

# Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Application code
COPY . .

# Set ephemeris path for pyswisseph
ENV SE_EPHE_PATH=/app/ephe
ENV FLASK_ENV=production
ENV PORT=8080

EXPOSE 8080

# Use gunicorn in production
# Cloud Run expects the app to listen on the $PORT environment variable
CMD gunicorn --bind 0.0.0.0:$PORT \
     --workers 2 --threads 4 \
     --timeout 120 \
     "run:app"
