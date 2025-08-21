import json
from .embedder import collection

def search(query_text, n_results=5):

    results = collection.query(
        query_texts=[query_text],
        n_results=n_results
    )
    

    formatted_results = []
    
    if results and 'metadatas' in results and len(results['metadatas']) > 0:
        metadatas = results['metadatas'][0]
        documents = results['documents'][0]
        distances = results.get('distances', [[]])[0]
        
        for i in range(len(metadatas)):
            formatted_results.append({
                "title": metadatas[i].get("title", "Untitled"),
                "page_title": metadatas[i].get("pageTitle", "Unknown Page"),
                "content": documents[i],
                "metadata": metadatas[i]
            })
    
    return formatted_results
    




