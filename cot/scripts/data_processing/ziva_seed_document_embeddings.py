import csv
import os
from ...ai.infrastructure.ziva.rag.retriever import ZiVAVectorRetriever
from dotenv import load_dotenv
input_file = os.path.join(os.path.dirname(__file__),"../../../data/training/ziva_document_embeddings_dataset.csv")
load_dotenv(".env")
# Initialize connection
vector_retriever = ZiVAVectorRetriever(
    connection_str=os.getenv("ZIVA_MONGO_URI")
)

def seed_document_embeddings_data():
    try:
        vector_retriever.create_index()
    except Exception as e:
        print ("CreateIndex Error{}".format(e))
    if not os.path.exists(input_file):
        return print("ziva_document_embeddings_dataset training data doesn't exist")
    with open(input_file, mode="r",  newline='', encoding='utf-8') as f:
        data = csv.DictReader(f)
        metadatakeys = [ "document_id", "document_type", "title","content",  
                        "source_url", "created_date", "updated_date", 
                        "author",  "keywords",
                "category", "locale" ]
        for x in data: 
            metadata = {}
            for key in metadatakeys:
               metadata[key] = x[key]
            vector_retriever.add_document(x['content'], metadata)
      

# Seed the data
seed_document_embeddings_data()