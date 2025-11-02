from pydantic import BaseModel
from typing import Optional

class EarthquakeBase(BaseModel):
    location_id: int
    monitoring_id: Optional[int]
    tsunami_id: Optional[int]
    magnitude: float
    depth: float
    sig: int
    Year: int
    Month: int

class EarthquakeCreate(EarthquakeBase):
    pass

class Earthquake(EarthquakeBase):
    earthquake_id: int

    class Config:
        orm_mode = True
