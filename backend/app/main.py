from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from backend.app.database import engine, Base, get_db
from backend.app.services.ingestion_service import seed_database
from backend.app.api import detections, risk, satellite, permits, trucks, routes

# Initialize database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="KHANAN-NETRA API",
    description="AI-Powered Satellite Mining Intelligence & Surveillance Core Backend",
    version="1.0.0"
)

# Enable CORS for React/Vite local frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows local Vite dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API Routers
app.include_router(detections.router)
app.include_router(risk.router)
app.include_router(satellite.router)
app.include_router(permits.router)
app.include_router(trucks.router)
app.include_router(routes.router)


@app.on_event("startup")
def startup_event():
    """
    Seeding database automatically on startup if tables are empty.
    """
    db = next(get_db())
    seed_database(db)


@app.get("/")
def home():
    return {
        "message": "Welcome to KHANAN-NETRA Core Intelligence Backend",
        "status": "Backend is running",
        "docs_url": "/docs"
    }


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "project": "KHANAN-NETRA",
        "mode": "DEMO DATA"
    }


@app.post("/api/ingest/seed")
def trigger_seed(db: Session = Depends(get_db)):
    """
    Manually re-trigger demo data ingestion.
    """
    seed_database(db)
    return {"message": "Demo data successfully ingested and evaluated."}