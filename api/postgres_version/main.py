from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud
from database import database, models, schemas

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create
@app.post("/earthquakes/", response_model=schemas.Earthquake)
def create_earthquake(eq: schemas.EarthquakeCreate, db: Session = Depends(get_db)):
    return crud.create_earthquake(db=db, eq=eq)

# Read all
@app.get("/earthquakes/", response_model=list[schemas.Earthquake])
def read_earthquakes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_earthquakes(db=db, skip=skip, limit=limit)

# Latest
@app.get("/earthquakes/latest", response_model=schemas.Earthquake)
def read_latest_earthquake(db: Session = Depends(get_db)):
    db_eq = crud.get_latest_earthquake(db=db)
    if db_eq is None:
        raise HTTPException(status_code=404, detail="No earthquakes found")
    return db_eq

# Read single
@app.get("/earthquakes/{earthquake_id}", response_model=schemas.Earthquake)
def read_earthquake(earthquake_id: int, db: Session = Depends(get_db)):
    db_eq = crud.get_earthquake(db=db, earthquake_id=earthquake_id)
    if db_eq is None:
        raise HTTPException(status_code=404, detail="Earthquake not found")
    return db_eq



# Update
@app.put("/earthquakes/{earthquake_id}", response_model=schemas.Earthquake)
def update_earthquake(earthquake_id: int, eq: schemas.EarthquakeCreate, db: Session = Depends(get_db)):
    db_eq = crud.update_earthquake(db=db, earthquake_id=earthquake_id, eq=eq)
    if db_eq is None:
        raise HTTPException(status_code=404, detail="Earthquake not found")
    return db_eq

# Delete
@app.delete("/earthquakes/{earthquake_id}", response_model=schemas.Earthquake)
def delete_earthquake(earthquake_id: int, db: Session = Depends(get_db)):
    db_eq = crud.delete_earthquake(db=db, earthquake_id=earthquake_id)
    if db_eq is None:
        raise HTTPException(status_code=404, detail="Earthquake not found")
    return db_eq
