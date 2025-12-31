from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# Base schema with common fields
class SensorDataBase(BaseModel):
    soil_moisture: float = Field(..., description="Soil moisture percentage", ge=0, le=100) # [cite: 36]
    temperature: float = Field(..., description="Ambient temperature in Celsius")          # [cite: 37]
    humidity: float = Field(..., description="Relative humidity percentage", ge=0, le=100) # [cite: 38]

# Schema for creating data (Ingestion)
class SensorDataCreate(SensorDataBase):
    pass

# Schema for reading data (Response)
class SensorDataResponse(SensorDataBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

class RecommendationResponse(BaseModel):
    status: str
    action_required: bool
    irrigation_advice: str
    fertilizer_advice: str
    # Add these fields so the frontend knows what data was used!
    current_moisture: float
    current_temp: float
    current_humidity: float