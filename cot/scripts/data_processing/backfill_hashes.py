def backfill_hashes():
    for doc in collection.find({"content_hash": {"$exists": False}}):
        hash_val = _generate_document_hash(doc["text"], doc.get("metadata", {}))
        collection.update_one(
            {"_id": doc["_id"]},
            {"$set": {"content_hash": hash_val}}
        )