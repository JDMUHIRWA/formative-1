from sqlalchemy.orm import Session
from . import models, schemas

def get_earthquake(db: Session, earthquake_id: int):
    return db.query(models.Earthquake).filter(models.Earthquake.earthquake_id == earthquake_id).first()

def get_earthquakes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Earthquake).offset(skip).limit(limit).all()

def create_earthquake(db: Session, eq: schemas.EarthquakeCreate):
    db_eq = models.Earthquake(**eq.dict())
    db.add(db_eq)
    db.commit()
    db.refresh(db_eq)
    return db_eq

def update_earthquake(db: Session, earthquake_id: int, eq: schemas.EarthquakeCreate):
    db_eq = db.query(models.Earthquake).filter(models.Earthquake.earthquake_id == earthquake_id).first()
    if db_eq:
        for key, value in eq.dict().items():
            setattr(db_eq, key, value)
        db.commit()
        db.refresh(db_eq)
    return db_eq

def delete_earthquake(db: Session, earthquake_id: int):
    db_eq = db.query(models.Earthquake).filter(models.Earthquake.earthquake_id == earthquake_id).first()
    if db_eq:
        db.delete(db_eq)
        db.commit()
    return db_eq
