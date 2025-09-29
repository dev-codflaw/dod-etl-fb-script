import pymongo
from config import MONGO_URI, DB_NAME, INPUT_COLLECTION, OUTPUT_COLLECTION

client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]

collection = db[INPUT_COLLECTION]
pdp_data   = db[OUTPUT_COLLECTION]

# unique index
pdp_data.create_index("hash_id", unique=True)
