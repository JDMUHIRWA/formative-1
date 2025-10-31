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
    return crud.get_earthquakes()

# READ ONE
@router.get("/earthquakes/{eq_id}")
def read_eq(eq_id: int):
    eq = crud.get_earthquake_by_id(eq_id)
    if not eq:
        raise HTTPException(status_code=404, detail="Not found")
    return eq

# UPDATE
@router.put("/earthquakes/{eq_id}")
def update_eq(eq_id: int, data: dict):
    updated_eq = crud.update_earthquake(eq_id, data)
    if not updated_eq:
        raise HTTPException(status_code=404, detail="Not found")
    return updated_eq

# DELETE
@router.delete("/earthquakes/{eq_id}")
def delete_eq(eq_id: int):
    result = crud.delete_earthquake(eq_id)
    if not result:
        raise HTTPException(status_code=404, detail="Not found")
    return result
