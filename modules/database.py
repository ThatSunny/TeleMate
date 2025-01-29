import urllib.parse
from pymongo import MongoClient
import configparser

# Load configuration
config = configparser.ConfigParser()
config.read('config.ini')

USERNAME = urllib.parse.quote_plus(config.get('default', 'username'))
PASSWORD = urllib.parse.quote_plus(config.get('default', 'password'))
DB_NAME = config.get('default', 'db_name')

# Correctly formatted MongoDB URI
MONGO_URL = f"mongodb+srv://{USERNAME}:{PASSWORD}@tgbot.bihau.mongodb.net/{DB_NAME}?retryWrites=true&w=majority"

# Connect to MongoDB
mongo_client = MongoClient(MONGO_URL)
db = mongo_client[DB_NAME]

# Collections
users_collection = db["users"]
chats_collection = db["chats"]
files_collection = db["files"]