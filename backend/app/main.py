from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.database.session import engine
from backend.app.models import sensor_data  # Import models to ensure they are registered with Base
from backend.app.database.base import Base
from backend.app.routers import ingestion, dashboard

# 1. Create Database Tables
# This automatically creates the 'sensor_readings' table in SQLite if it doesn't exist.
Base.metadata.create_all(bind=engine)

# 2. Initialize the App
app = FastAPI(
    title="Smart Agriculture API",
    description="Vibe Coding Lab - Phase 3 Backend",
    version="1.0.0"
)

# 3. Configure CORS (Optional but good practice)
# Allows the frontend (or other tools) to communicate with this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the exact frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Include Routers
# We register the endpoints we created in the 'routers' folder.
# The dashboard router serves: GET /recommendations
app.include_router(dashboard.router, tags=["Dashboard"])

# The ingestion router serves: POST /ingest
app.include_router(ingestion.router, tags=["Ingestion"])

@app.get("/")
def health_check():
    """Simple health check to verify the server is running."""
    return {"status": "active", "system": "Smart Agri Vibe Coding Lab"}