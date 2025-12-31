from sqlalchemy import Column, Integer, Float, DateTime
from datetime import datetime
from backend.app.database.base import Base # Assuming Base is defined in database/base.py

class SensorData(Base):
    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    soil_moisture = Column(Float, nullable=False)
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)