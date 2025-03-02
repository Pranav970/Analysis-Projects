from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("MONGO_DB_NAME")

def connect_mongodb():
    """
    Connects to MongoDB and returns the database object.
    """
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        print("Connected to MongoDB successfully!")
        return db
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None

if __name__ == '__main__':
    db = connect_mongodb()
    if db:
        print(f"Connected to database: {db.name}")
