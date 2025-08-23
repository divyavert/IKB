
from injest.embedder import embed_documents
from injest.fetcher import fetch_confluence_pages
from injest.transformer import transform_fetched_pages
from dotenv import load_dotenv
import time

load_dotenv()

print("Starting document embedding pipeline...")
start_time = time.time()

print("Fetching pages from Confluence...")
fetched_pages = fetch_confluence_pages()
print(f"Fetched {len(fetched_pages)} pages from Confluence.")

print("Transforming pages into chunks...")
transformed_chunks = transform_fetched_pages(fetched_pages)
print(f"Created {len(transformed_chunks)} chunks for embedding.")

print("Starting embedding process...")
new_count = 0
updated_count = 0
unchanged_count = 0

for i, chunk in enumerate(transformed_chunks):
    print(f"Processing chunk {i+1}/{len(transformed_chunks)}: {chunk['title']}")
    
    # Track state before embedding
    initial_doc_state = {"new": True}
    
    # Process embedding and get result
    embeddings = embed_documents(chunk)

    
    
    # Count based on console output (a bit hacky but works)
    if "Adding new document" in str(embeddings):
        new_count += 1
    elif "Updating document" in str(embeddings):
        updated_count += 1
    else:
        unchanged_count += 1

elapsed_time = time.time() - start_time
print(f"\nEmbedding pipeline completed in {elapsed_time:.2f} seconds.")
print(f"Summary: {new_count} new documents, {updated_count} updated documents, {unchanged_count} unchanged documents.")
print(f"Total chunks processed: {len(transformed_chunks)}")


