import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from ../.env
load_dotenv(os.path.join("..", ".env"))

#  Get MongoDB URI from environment
mongo_uri = os.getenv("MONGO_URI")  

#  Connect to MongoDB
client = MongoClient(mongo_uri)
print(" Connected to MongoDB")

# Create database and collection
db = client["global_earthquake_db"]
collection = db["global_earthquake_db"]

# 5 Load CSV dataset from its full path
csv_path = r"../database/dataset/Global Earthquake Tsunami Data.csv"

df = pd.read_csv(csv_path)

#  Insert all records into MongoDB
collection.insert_many(df.to_dict(orient="records"))
print(f" Inserted {len(df)} earthquake records successfully!")

#  Close connection
client.close()
print(" Connection closed")
