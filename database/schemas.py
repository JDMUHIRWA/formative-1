from pydantic import BaseModel

class EarthquakeBase(BaseModel):
    location_id: int
    monitoring_id: int
    tsunami_id: int
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
