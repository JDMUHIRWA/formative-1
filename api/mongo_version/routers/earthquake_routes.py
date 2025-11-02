from fastapi import APIRouter, HTTPException, Query
from typing import List
from .. import crud
from ..schemas import (
    EarthquakeMongoCreate,
    EarthquakeMongoUpdate,
    EarthquakeMongoResponse,
    DeleteResponse
)

router = APIRouter()

# CREATE
@router.post("/earthquakes", response_model=dict, status_code=201)
def create_eq(earthquake: EarthquakeMongoCreate):
    """
    Create a new earthquake record in MongoDB.
    
    - **magnitude**: Earthquake magnitude (0-10)
    - **depth**: Depth in kilometers (must be positive)
    - **sig**: Significance value
    - **Year**: Year of earthquake
    - **Month**: Month (1-12)
    - Plus optional fields like latitude, longitude, tsunami, etc.
    """
    return crud.create_earthquake(earthquake)

# READ ALL
@router.get("/earthquakes", response_model=List[dict])
def read_eqs(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return")
):
    """
    Retrieve all earthquake records with pagination.
    
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum records to return (default: 100, max: 1000)
    """
    earthquakes = crud.get_earthquakes(skip=skip, limit=limit)
    if not earthquakes:
        return []
    return earthquakes

# READ ONE by _id
@router.get("/earthquakes/{eq_id}", response_model=dict)
def read_eq(eq_id: str):
    """
    Retrieve a single earthquake record by its MongoDB _id.
    
    - **eq_id**: MongoDB document ID (24-character hex string)
    """
    eq = crud.get_earthquake_by_id(eq_id)
    if not eq:
        raise HTTPException(
            status_code=404,
            detail=f"Earthquake with ID '{eq_id}' not found"
        )
    return eq

# UPDATE by _id
@router.put("/earthquakes/{eq_id}", response_model=dict)
def update_eq(eq_id: str, earthquake: EarthquakeMongoUpdate):
    """
    Update an existing earthquake record.
    
    - **eq_id**: MongoDB document ID
    - All fields are optional - only provided fields will be updated
    """
    updated_eq = crud.update_earthquake(eq_id, earthquake)
    if not updated_eq:
        raise HTTPException(
            status_code=404,
            detail=f"Earthquake with ID '{eq_id}' not found or no fields to update"
        )
    return updated_eq

# DELETE by _id
@router.delete("/earthquakes/{eq_id}", response_model=DeleteResponse)
def delete_eq(eq_id: str):
    """
    Delete an earthquake record by its MongoDB _id.
    
    - **eq_id**: MongoDB document ID
    """
    result = crud.delete_earthquake(eq_id)
    
    if result.get("deleted_id") is None:
        raise HTTPException(
            status_code=404 if "not found" in result.get("message", "").lower() else 400,
            detail=result.get("message", "Failed to delete earthquake")
        )
    
    return result
