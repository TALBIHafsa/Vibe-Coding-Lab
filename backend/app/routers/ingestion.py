from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.database.session import get_db # Assuming get_db dependency exists
from backend.app.schemas.sensor import SensorDataCreate, SensorDataResponse
from backend.app.models.sensor_data import SensorData

router = APIRouter()

@router.post("/ingest", response_model=SensorDataResponse, status_code=201)
def ingest_sensor_data(reading: SensorDataCreate, db: Session = Depends(get_db)):
    """
    Ingest data from IoT sensors (Soil, Temp, Humidity).
    """
    new_reading = SensorData(
        soil_moisture=reading.soil_moisture,
        temperature=reading.temperature,
        humidity=reading.humidity
    )
    db.add(new_reading)
    db.commit()
    db.refresh(new_reading)
    return new_reading