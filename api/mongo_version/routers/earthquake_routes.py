from fastapi import APIRouter, HTTPException
from .. import crud

router = APIRouter()

# CREATE
@router.post("/earthquakes")
def create_eq(data: dict):
    return crud.create_earthquake(data)

# READ ALL
@router.get("/earthquakes")
def read_eqs():
    earthquakes = crud.get_earthquakes()
    if not earthquakes:
        return {"message": "No records found"}
    return earthquakes

# READ ONE by _id
@router.get("/earthquakes/{eq_id}")
def read_eq(eq_id: str):
    eq = crud.get_earthquake_by_id(eq_id)
    if not eq:
        raise HTTPException(status_code=404, detail="Earthquake not found")
    return eq

# UPDATE by _id
@router.put("/earthquakes/{eq_id}")
def update_eq(eq_id: str, data: dict):
    updated_eq = crud.update_earthquake(eq_id, data)
    if not updated_eq:
        raise HTTPException(status_code=404, detail="Earthquake not found")
    return updated_eq

# DELETE by _id
@router.delete("/earthquakes/{eq_id}")
def delete_eq(eq_id: str):
    return crud.delete_earthquake(eq_id)
