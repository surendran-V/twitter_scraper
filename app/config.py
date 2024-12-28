import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TWITTER_USERNAME = os.getenv('TWITTER_USERNAME')
    TWITTER_PASSWORD = os.getenv('TWITTER_PASSWORD')
    PROXYMESH_USERNAME = os.getenv('PROXYMESH_USERNAME')
    PROXYMESH_PASSWORD = os.getenv('PROXYMESH_PASSWORD')
    PROXYMESH_HOST = os.getenv('PROXYMESH_HOST')
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
    DATABASE_NAME = os.getenv('DATABASE_NAME', 'trending_topics')
    COLLECTION_NAME = os.getenv('COLLECTION_NAME', 'trends')