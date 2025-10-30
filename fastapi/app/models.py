from sqlalchemy import Column, Integer, Float, ForeignKey, String, TIMESTAMP, Boolean # type: ignore
from .database import Base

class Earthquake(Base):
    __tablename__ = "earthquakes"

    earthquake_id = Column(Integer, primary_key=True, index=True)
    location_id = Column(Integer, nullable=False)
    monitoring_id = Column(Integer, nullable=True)
    tsunami_id = Column(Integer, nullable=True)
    magnitude = Column(Float, nullable=False)
    depth = Column(Float, nullable=False)
    sig = Column(Integer, nullable=False)
    Year = Column(Integer, nullable=False)
    Month = Column(Integer, nullable=False)
