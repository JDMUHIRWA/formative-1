from bson import ObjectId
from .database import earthquake_collection

# CREATE
def create_earthquake(data: dict):
    # Insert document into collection
    result = earthquake_collection.insert_one(data)
    # Add _id as string for response
    data["_id"] = str(result.inserted_id)
    return data

# READ ALL
def get_earthquakes():
    results = list(earthquake_collection.find({}))
    # Convert ObjectId to string for JSON
    for r in results:
        r["_id"] = str(r["_id"])
    return results

# READ ONE by _id
def get_earthquake_by_id(eq_id: str):
    try:
        obj_id = ObjectId(eq_id)
    except:
        return None
    result = earthquake_collection.find_one({"_id": obj_id})
    if result:
        result["_id"] = str(result["_id"])
    return result

# UPDATE by _id
def update_earthquake(eq_id: str, data: dict):
    try:
        obj_id = ObjectId(eq_id)
    except:
        return None
    earthquake_collection.update_one({"_id": obj_id}, {"$set": data})
    updated = earthquake_collection.find_one({"_id": obj_id})
    if updated:
        updated["_id"] = str(updated["_id"])
    return updated

# DELETE by _id
def delete_earthquake(eq_id: str):
    try:
        obj_id = ObjectId(eq_id)
    except:
        return {"message": "Invalid ID"}
    earthquake_collection.delete_one({"_id": obj_id})
    return {"message": "Deleted"}
