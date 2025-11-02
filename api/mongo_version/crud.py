from bson import ObjectId
from typing import Optional, List, Dict, Any
from .database import earthquake_collection
from .schemas import EarthquakeMongoCreate, EarthquakeMongoUpdate

# CREATE
def create_earthquake(data: EarthquakeMongoCreate) -> Dict[str, Any]:
    """Create a new earthquake document in MongoDB."""
    # Convert Pydantic model to dict, excluding unset values
    earthquake_dict = data.model_dump(exclude_unset=True)

    # Insert document into collection
    result = earthquake_collection.insert_one(earthquake_dict)

    # Add _id as string for response
    earthquake_dict["_id"] = str(result.inserted_id)
    return earthquake_dict

# READ ALL
def get_earthquakes(skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
    """Get all earthquakes with pagination."""
    results = list(earthquake_collection.find({}).skip(skip).limit(limit))
    # Convert ObjectId to string for JSON
    for r in results:
        r["_id"] = str(r["_id"])
    return results

# READ ONE by _id
def get_earthquake_by_id(eq_id: str) -> Optional[Dict[str, Any]]:
    """Get a single earthquake by MongoDB _id."""
    try:
        obj_id = ObjectId(eq_id)
    except Exception:
        return None

    result = earthquake_collection.find_one({"_id": obj_id})
    if result:
        result["_id"] = str(result["_id"])
    return result

# UPDATE by _id
def update_earthquake(eq_id: str, data: EarthquakeMongoUpdate) -> Optional[Dict[str, Any]]:
    """Update an earthquake document by _id."""
    try:
        obj_id = ObjectId(eq_id)
    except Exception:
        return None

    # Convert Pydantic model to dict, excluding unset values
    update_dict = data.model_dump(exclude_unset=True)

    # Only update if there are fields to update
    if not update_dict:
        return None

    earthquake_collection.update_one({"_id": obj_id}, {"$set": update_dict})
    updated = earthquake_collection.find_one({"_id": obj_id})
    if updated:
        updated["_id"] = str(updated["_id"])
    return updated

# DELETE by _id
def delete_earthquake(eq_id: str) -> Dict[str, Optional[str]]:
    """Delete an earthquake document by _id."""
    try:
        obj_id = ObjectId(eq_id)
    except Exception:
        return {"message": "Invalid ID format", "deleted_id": None}

    result = earthquake_collection.delete_one({"_id": obj_id})

    if result.deleted_count == 0:
        return {"message": "Earthquake not found", "deleted_id": None}

    return {"message": "Earthquake deleted successfully", "deleted_id": eq_id}
