from sqlalchemy import Column, Integer, Float, String, TIMESTAMP, Boolean, JSON
from sqlalchemy.sql import func
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
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())


class EarthquakeAuditLog(Base):
    __tablename__ = "earthquake_audit_log"

    log_id = Column(Integer, primary_key=True, index=True)
    table_name = Column(String, nullable=False)
    operation = Column(String, nullable=False)
    record_id = Column(Integer, nullable=True)
    old_values = Column(JSON, nullable=True)
    new_values = Column(JSON, nullable=True)
    changed_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    changed_by = Column(String, nullable=True)
