from .database import earthquake_collection

def create_earthquake(data):
    earthquake_collection.insert_one(data)
    return data

def get_earthquakes():
    return list(earthquake_collection.find({}, {"_id": 0}))

def get_earthquake_by_id(eq_id: int):
    return earthquake_collection.find_one({"earthquake_id": eq_id}, {"_id": 0})

def update_earthquake(eq_id: int, data):
    earthquake_collection.update_one({"earthquake_id": eq_id}, {"$set": data})
    return earthquake_collection.find_one({"earthquake_id": eq_id}, {"_id": 0})

def delete_earthquake(eq_id: int):
    earthquake_collection.delete_one({"earthquake_id": eq_id})
    return {"message": "Deleted"}
