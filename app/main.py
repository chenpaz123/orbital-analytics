from fastapi import FastAPI
from app.api.endpoints import router as api_router

# הגדרת המטא-דאטה של ה-API (חשוב לתיעוד האוטומטי)
app = FastAPI(
    title="Orbital Analytics API",
    description="Real-time satellite tracking system backed by Skyfield physics engine.",
    version="1.0.0"
)

# חיבור ה-Router הראשי
app.include_router(api_router, prefix="/api/v1", tags=["Satellite"])

@app.get("/health")
async def health_check():
    """
    נקודת קצה לבדיקה שהשרת חי (Liveness Probe).
    משמש את Kubernetes/Docker כדי לדעת אם להפעיל מחדש את הקונטיינר.
    """
    return {"status": "healthy", "service": "orbital-analytics"}