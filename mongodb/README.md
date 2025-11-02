#  Global Earthquake & Tsunami Data — MongoDB Implementation

##  Objective
This part of the assignment focuses on **implementing a NoSQL database** using **MongoDB Atlas**.  
The goal is to store, verify, and manage global earthquake and tsunami data in a cloud database.  

The dataset contains **782 records** of earthquakes worldwide between **2001 and 2022**, including information such as magnitude, depth, coordinates, tsunami occurrence, and date.

---

##  Technology Stack
| Tool | Purpose |
|------|---------|
| Python 3 | Scripting and data manipulation |
| pandas | Load and inspect CSV data |
| pymongo | Connect and insert data into MongoDB Atlas |
| python-dotenv | Load environment variables (MongoDB URI) |
| MongoDB Atlas | Cloud NoSQL database |

---

##  Setup Instructions

### 1️ Folder Structure

root_repository/
├─ database/
│   └─ dataset/
│       └─ Global Earthquake Tsunami Data.csv   
├─ mongodb/
│   ├─ .env                                  
│   └─ earthquake_risk_db/
│       ├─ earthquake_risk_db.py    
│       ├─ check_mongo.py           
│       └─ README.md 

### 2 install all dependencies 

pip install pandas pymongo python-dotenv

### 3 configure .env

Create a `.env` file in the **root repository** and insert your own mongodb atlas cluster URL

### 4 run the database

python earthquake_risk_db.py

### 5 output 

✅ Connected to MongoDB
📦 Inserted 782 earthquake records successfully!
🔒 Connection closed

### 6 verify database

python check_mongo.py

### expected output 

Databases in your cluster:
['global_earthquake_db', 'sample_mflix', 'admin', 'local']

Collections in 'global_earthquake_db':
['earthquake_data']

Number of documents in 'earthquake_data': 782
