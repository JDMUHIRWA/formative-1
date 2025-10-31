from sqlalchemy import Column, Integer, Float, String
from .database import Base

class Earthquake(Base):
    __tablename__ = "earthquakes"

    earthquake_id = Column(Integer, primary_key=True, index=True)
    location_id = Column(Integer)
    monitoring_id = Column(Integer)
    tsunami_id = Column(Integer)
    magnitude = Column(Float)
    depth = Column(Float)
    sig = Column(Integer)
    Year = Column(Integer)
    Month = Column(Integer)
