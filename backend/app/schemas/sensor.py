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

# Schema for Recommendations
class RecommendationResponse(BaseModel):
    status: str
    action_required: bool
    irrigation_advice: str  # [cite: 40]
    fertilizer_advice: str  # [cite: 41]