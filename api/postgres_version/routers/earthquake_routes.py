from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, database

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close() 

# CREATE
@router.post("/earthquakes", response_model=schemas.Earthquake)
def create_eq(earthquake: schemas.EarthquakeCreate, db: Session = Depends(get_db)):
    return crud.create_earthquake(db, earthquake)

# READ ALL
@router.get("/earthquakes", response_model=list[schemas.Earthquake])
def read_eqs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_earthquakes(db, skip, limit)

# READ ONE
@router.get("/earthquakes/{earthquake_id}", response_model=schemas.Earthquake)
def read_eq(earthquake_id: int, db: Session = Depends(get_db)):
    db_eq = crud.get_earthquake(db, earthquake_id)
    if not db_eq:
        raise HTTPException(status_code=404, detail="Earthquake not found")
    return db_eq

# UPDATE
@router.put("/earthquakes/{earthquake_id}", response_model=schemas.Earthquake)
def update_eq(earthquake_id: int, earthquake: schemas.EarthquakeCreate, db: Session = Depends(get_db)):
    updated_eq = crud.update_earthquake(db, earthquake_id, earthquake)
    if not updated_eq:
        raise HTTPException(status_code=404, detail="Earthquake not found")
    return updated_eq

# DELETE
@router.delete("/earthquakes/{earthquake_id}")
def delete_eq(earthquake_id: int, db: Session = Depends(get_db)):
    deleted_eq = crud.delete_earthquake(db, earthquake_id)
    if not deleted_eq:
        raise HTTPException(status_code=404, detail="Earthquake not found")
    return {"message": "Deleted successfully"}
