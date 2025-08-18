# 🧠 IKB – Internal Knowledge Base (RAG Demo)

IKB is a **Retrieval-Augmented Generation (RAG)** system designed for answering internal company FAQs.  
It simulates how employees in a company could query policies, workflows, or engineering guides (e.g., *“How do I deploy the frontend in our staging environment?”*), with answers retrieved from internal documentation (mock Confluence pages).

---

## 🚀 Project Overview
- **Goal**: Build a chatbot that answers internal FAQs using company docs.  
- **Knowledge Base**: Mock Confluence-like documents (policies, workflows, engineering guidelines).  
- **Pipeline Design**:  
  - **Ingestion** → Fetch & embed docs into a vector DB.  
  - **Query** → Retrieve relevant chunks + generate an answer using an LLM.  

---

## ⚙️ Tech Stack
- **Language**: Python  
- **Embeddings**: [Sentence Transformers](https://www.sbert.net/) (`all-MiniLM-L6-v2`)  
- **Vector DB**: [FAISS](https://github.com/facebookresearch/faiss) (local, lightweight)  
- **LLM**: [Ollama](https://ollama.ai/) (Mistral or Llama3 recommended)  
- **Docs Source**: Mock Confluence data (can be swapped with real Confluence API)  
