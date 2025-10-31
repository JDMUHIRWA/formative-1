# schemas.py
from pydantic import BaseModel
from typing import Optional

class EarthquakeBase(BaseModel):
    location_id: int
    monitoring_id: Optional[int] = None
    tsunami_id: Optional[int] = None
    magnitude: float
    depth: float
    sig: int
    Year: int
    Month: int

class EarthquakeCreate(EarthquakeBase):
    pass

class EarthquakeUpdate(BaseModel):
    # All fields optional for partial update
    location_id: Optional[int] = None
    monitoring_id: Optional[int] = None
    tsunami_id: Optional[int] = None
    magnitude: Optional[float] = None
    depth: Optional[float] = None
    sig: Optional[int] = None
    Year: Optional[int] = None
    Month: Optional[int] = None

class Earthquake(EarthquakeBase):
    earthquake_id: int

    class Config:
        orm_mode = True
