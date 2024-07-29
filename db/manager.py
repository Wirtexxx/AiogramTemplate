from pymongo.mongo_client import MongoClient
from conf import DB_URI


client = MongoClient(DB_URI)
customer_db = client["customer"]
users_collection = customer_db["users"]
order_collection = customer_db["orders"]

print("Db status is", customer_db.command('ping'))
