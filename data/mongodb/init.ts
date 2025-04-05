db.createCollection("document_embeddings");
db.runCommand({
  "createIndexes": "document_embeddings",
  "indexes": [{
    "name": "vector_index",
    "key": {"embedding": "cosmosSearch"},
    "cosmosSearchOptions": {"kind": "vector-ivf", "dimensions": 384}
  }]
});
db.document_embeddings.createIndex(
    {"content_hash": 1}, 
    {unique: true, name: "content_hash_idx"}
)