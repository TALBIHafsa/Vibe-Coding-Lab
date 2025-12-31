from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from backend.app.database.session import get_db
from backend.app.models.sensor_data import SensorData
from backend.app.services.engine import generate_recommendation
from backend.app.schemas.sensor import RecommendationResponse, SensorDataCreate

router = APIRouter()

@router.get("/recommendations", response_model=RecommendationResponse)
def get_latest_recommendation(db: Session = Depends(get_db)):
    """
    Analyzes the latest sensor reading to provide actionable advice.
    """
    # Fetch latest reading [cite: 48]
    latest = db.query(SensorData).order_by(desc(SensorData.timestamp)).first()
    
    if not latest:
        raise HTTPException(status_code=404, detail="No sensor data available to analyze")

    # Map model to schema for service processing
    data_snapshot = SensorDataCreate(
        soil_moisture=latest.soil_moisture,
        temperature=latest.temperature,
        humidity=latest.humidity
    )

    # Generate recommendation using the logic engine [cite: 39]
    return generate_recommendation(data_snapshot)