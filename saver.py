from db import pdp_data, collection
import pymongo

def save_record(records, idd):
    try:
        pdp_data.insert_one(records)
        print(f"✅ Data inserted: {idd}")
    except pymongo.errors.DuplicateKeyError:
        print(f"⚠️ Duplicate record skipped: {idd}")
    except Exception as e:
        print(f"❌ Insert failed: {e}")
    finally:
        collection.update_one({"url_id": idd}, {"$set": {"status": "page_saved1"}})
