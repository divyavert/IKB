

from injest.embedder import embed_documents
from injest.fetcher import fetch_confluence_pages
from injest.transformer import transform_fetched_pages
from dotenv import load_dotenv

load_dotenv()


fetched_pages = fetch_confluence_pages()
transformed_chunks = transform_fetched_pages(fetched_pages)


count = 0
for chunk in transformed_chunks:
    embeddings = embed_documents(chunk)
    count += 1


