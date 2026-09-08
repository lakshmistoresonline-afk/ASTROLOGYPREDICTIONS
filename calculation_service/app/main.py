from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .core.engine import calculate_natal_chart, calculate_dasha, calculate_transits_for_range, calculate_sky_events
from typing import Optional, Dict, Any, List

app = FastAPI(title="Jyotish OS Calculation Service")

class BirthData(BaseModel):
    year: int
    month: int
    day: int
    hour: float
    lat: float
    lon: float
    ayanamsa: Optional[str] = "LAHIRI"

class TransitRangeRequest(BaseModel):
    start_date: str
    end_date: str
    lat: float
    lon: float

class SkyEventRequest(BaseModel):
    jd_ut: float
    lat: float
    lon: float

@app.get("/health")
def health():
    return {"status": "ok", "engine": "Swiss Ephemeris"}

@app.post("/v1/natal-chart")
def get_natal_chart(data: BirthData):
    try:
        return calculate_natal_chart(data.year, data.month, data.day, data.hour, data.lat, data.lon, data.ayanamsa)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/v1/transits/range")
def get_transit_range(req: TransitRangeRequest):
    try:
        return calculate_transits_for_range(req.start_date, req.end_date, req.lat, req.lon)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/v1/sky-events")
def get_sky_events(req: SkyEventRequest):
    try:
        return calculate_sky_events(req.jd_ut, req.lat, req.lon)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
