from fastapi import FastAPI
from app.api.endpoints import router as api_router
from fastapi.middleware.cors import CORSMiddleware

# הגדרת המטא-דאטה של ה-API (חשוב לתיעוד האוטומטי)
app = FastAPI(
    title="Orbital Analytics API",
    description="Real-time satellite tracking system backed by Skyfield physics engine.",
    version="1.0.0",
)


origins = [
    "http://localhost:3000",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
