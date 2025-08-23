
import uuid
import chromadb

client = chromadb.PersistentClient(path="../chroma_db")
collection = client.get_or_create_collection(name="advantalabs")


def embed_documents(chunk):
    # Check if a document with the same pageId and content exists
    existing_docs = collection.query(
        query_texts=[chunk["content"]],
        n_results=5,
        where={"$and": [
            {"pageTitle": {"$eq": chunk["pageTitle"]}},
            {"title": {"$eq": chunk["title"]}}
        ]}
    )
    
    # Check if we found a match
    should_add_new = True
    if existing_docs and len(existing_docs['ids'][0]) > 0:
        for i, doc_id in enumerate(existing_docs['ids'][0]):
            # Check similarity of content to determine if it's the same document
            metadata = existing_docs['metadatas'][0][i]
            
            # If we found a similar document, check if updated_at is different
            if metadata.get("updated_at") != chunk["updated_at"]:
                # Different updated_at timestamp - update the document
                print(f"Updating document {doc_id} with new content from {chunk['pageTitle']} - {chunk['title']}")
                collection.update(
                    ids=[doc_id],
                    documents=[chunk["content"]],
                    metadatas=[{
                        "title": chunk["title"],
                        "id": doc_id,
                        "content": chunk["content"],
                        "pageTitle": chunk["pageTitle"],
                        "updated_at": chunk["updated_at"]
                    }]
                )
                should_add_new = False
                return collection.get(ids=[doc_id])
            else:
                # Same updated_at - no need to update
                print(f"Document {doc_id} is already up to date - {chunk['pageTitle']} - {chunk['title']}")
                should_add_new = False
                return collection.get(ids=[doc_id])
    
    # If no match found or all matches had different content, add as new document
    if should_add_new:
        random_id = str(uuid.uuid4())
        print(f"Adding new document {random_id} for {chunk['pageTitle']} - {chunk['title']}")
        collection.add(
            ids=[random_id],                     
            documents=[chunk["content"]],       
            metadatas=[{
                "title": chunk["title"], 
                "id": random_id,                 
                "content": chunk["content"], 
                "pageTitle": chunk["pageTitle"],
                "updated_at": chunk["updated_at"]
            }]
        )
        return collection.get(ids=[random_id])
