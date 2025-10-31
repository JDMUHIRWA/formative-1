# models.py
from sqlalchemy import Column, Integer, Float
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

    def __repr__(self) -> str:
        return f"<Earthquake id={self.earthquake_id} mag={self.magnitude} loc={self.location_id}>"
