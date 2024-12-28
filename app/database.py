import pymongo
from app.config import Config

class Database:
    def __init__(self):
        self.client = pymongo.MongoClient(Config.MONGODB_URI)
        self.db = self.client[Config.DATABASE_NAME]
        self.collection = self.db[Config.COLLECTION_NAME]
    
    def insert_trends(self, trends_data):
        return self.collection.insert_one(trends_data)
    
    def get_latest_trends(self):
        return self.collection.find_one(
            sort=[('datetime', pymongo.DESCENDING)]
        )
    
    def close(self):
        self.client.close()