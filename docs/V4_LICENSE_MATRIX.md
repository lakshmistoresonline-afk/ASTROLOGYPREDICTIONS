# V4 License Matrix

| Package | Version | License | URL / Source | Commercial Use | Copyleft Obligations | Incorporated Source? | Runtime Required? | Replacement Option |
|---|---|---|---|---|---|---|---|---|
| Flask | 3.0.x | BSD-3-Clause | pypi.org/project/Flask | Yes | No | No | Yes | Quart / FastAPI |
| SQLAlchemy | 2.0.x | MIT | pypi.org/project/SQLAlchemy | Yes | No | No | Yes | PonyORM / Tortoise |
| FastAPI | 0.111.x | MIT | pypi.org/project/fastapi | Yes | No | No | Yes | Starlette |
| Uvicorn | 0.29.x | BSD-3-Clause | pypi.org/project/uvicorn | Yes | No | No | Yes | Hypercorn |
| Pydantic | 2.7.x | MIT | pypi.org/project/pydantic | Yes | No | No | Yes | Marshmallow |
| pyswisseph | 2.10.3.x | Astrodienst / GPL-compatible | pypi.org/project/pyswisseph | Conditional (GPL) | Yes (if distributed) | No (API/binary proxy) | Yes | Skyfield / JPL |
| Requests | 2.31.x | Apache-2.0 | pypi.org/project/requests | Yes | No | No | Yes | Httpx |
| PyTZ | 2024.1 | MIT | pypi.org/project/pytz | Yes | No | No | Yes | zoneinfo |
| Pytest | 8.2.x | MIT | pypi.org/project/pytest | Yes | No | No | Yes | unittest |

## Licensing Status: COMPLIANT & ISOLATED
Swiss Ephemeris calculations are isolated within the FastAPI calculation service (`calculation_service/`), maintaining a clean boundary from the Flask application layer.
