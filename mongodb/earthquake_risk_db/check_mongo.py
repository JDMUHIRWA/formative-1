from pymongo import MongoClient

# Your Atlas URI
mongo_uri = "mongodb+srv://earthquake_db_user:Mklbt2UaptabgxRF@cluster0.vxnblou.mongodb.net/"

# Connect to MongoDB Atlas
client = MongoClient(mongo_uri)

# List all databases in the cluster
print("Databases in your cluster:")
print(client.list_database_names())

# Access the database you inserted into
db = client["global_earthquake_db"]

# List collections in that database
print("\nCollections in 'global_earthquake_db':")
print(db.list_collection_names())

# Optional: count documents in your collection
collection = db["earthquake_data"]
print(f"\nNumber of documents in 'earthquake_data': {collection.count_documents({})}")

client.close()
