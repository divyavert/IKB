import chromadb
import os

# Use an absolute path for the persistent database
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../chroma_db'))

# Ensure the directory exists
os.makedirs(DB_PATH, exist_ok=True)

client = chromadb.PersistentClient(path=DB_PATH)
collection = client.get_or_create_collection(name="advantalabs")


def semantic_search(query_text, n_results=6):
    """
    Performs semantic search on embedded documents using vector similarity.
    
    Args:
        query_text (str): The query text to search for
        n_results (int): Number of results to return (default: 5)
        
    Returns:
        list: List of formatted search results with metadata
    """
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
    




