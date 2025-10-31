from pymongo import MongoClient # type: ignore

client = MongoClient("mongodb://localhost:27017")
db = client["earthquake_db"]
earthquake_collection = db["earthquake"]
