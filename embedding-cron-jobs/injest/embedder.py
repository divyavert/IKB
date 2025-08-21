
import uuid
import chromadb

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="advantalabs")


def embed_documents(chunk):
    random_id = str(uuid.uuid4()) 
    
    collection.add(
        ids=[random_id],                     
        documents=[chunk["content"]],       
        metadatas=[{
            "title": chunk["title"], 
            "id": random_id,                 
            "content": chunk["content"], 
            "pageTitle": chunk["pageTitle"]
        }]
    )
    
    return collection.get(ids=[random_id])
