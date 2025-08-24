# ✨ IKB – Internal Knowledge Base (RAG System)

IKB is a modern **Retrieval-Augmented Generation (RAG)** system designed for answering internal company questions and accessing organizational knowledge efficiently. It provides natural language interactions with your company's documentation, allowing employees to quickly find answers to questions like _"How do I deploy the frontend in our staging environment?"_ or _"What's the process for requesting PTO?"_



## 🚀 Project Overview

- **Purpose**: A chatbot interface for querying internal company knowledge
- **Knowledge Source**: Vector database containing embedded documentation chunks
- **Architecture**:
  - **Frontend**: Modern React UI with Material UI components
  - **Backend**: FastAPI server handling requests and responses
  - **Embeddings**: ChromaDB for vector storage and retrieval
  - **LLM Integration**: Ollama for local inference

## 🔄 Data Flow

1. User enters a question in the modern UI
2. FastAPI backend receives the request
3. ChromaDB performs semantic search to find relevant document chunks
4. Context is retrieved and processed
5. Ollama (with Mistral) generates a structured response
6. Response is displayed in the UI with markdown formatting

## 🛠️ Tech Stack

### Backend

- **Language**: Python 3.x
- **API Framework**: FastAPI
- **Vector Database**: ChromaDB (persistent storage)
- **LLM Integration**: Ollama with Mistral model
- **Embeddings**: Sentence transformers (implicit through ChromaDB)

### Frontend

- **Framework**: React 19 with TypeScript
- **Build Tool**: Vite 7
- **UI Components**: Material UI 7
- **Styling**: SCSS with modern CSS features
- **HTTP Client**: Axios

## ✅ Features

- **Modern UI/UX**: Clean, responsive design with dark/light mode
- **Real-time Chat**: Natural conversation interface
- **Markdown Support**: Rich text formatting in responses
- **Semantic Chunking**: Intelligent document segmentation for improved retrieval accuracy
- **Context Retrieval**: Smart fetching of relevant document chunks
- **Structured Responses**: JSON-formatted answers with confidence levels
- **Automatic Updates**: Embedding updates based on document timestamps

## 🚀 Getting Started

### Prerequisites

- Python 3.x
- Node.js (latest LTS)
- Ollama installed locally with Mistral model

### Backend Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/IKB.git
cd IKB

# Set up Python environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the server
cd ikb_backend
uvicorn server:app --reload --port 3000
```

### Frontend Setup

```bash
# Navigate to frontend directory
cd ikb_frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### Embedding Data

```bash
# Navigate to embedding cron jobs directory
cd embedding-cron-jobs

# Run the ingestion pipeline
python -m injest.pipeline
```

## 🔧 Configuration

The system can be configured to use different LLMs, embeddings, and data sources:

- **LLM**: Edit `llm.py` to change model parameters or switch LLM providers
- **Vector DB**: ChromaDB settings in `db.py`
- **Data Sources**: Configure document sources in `injest/fetcher.py`

## 📂 Project Structure

```
IKB/
├── assets/                         # Screenshots and demo videos
│   ├── Chatting_With_Your_Docs.mp4
│   └── Screenshot*.png
├── chroma_db/                      # Persistent vector database
├── embedding-cron-jobs/            # Document processing pipeline
│   ├── injest/
│   │   ├── __init__.py
│   │   ├── embedder.py             # Document embedding logic
│   │   ├── fetcher.py              # Document source connectors
│   │   ├── pipeline.py             # Main ingestion pipeline
│   │   ├── query.py                # Query testing utilities
│   │   └── transformer.py          # Document chunking logic
│   └── requirements.txt
├── ikb_backend/                    # FastAPI server
│   ├── __init__.py
│   ├── db.py                       # ChromaDB integration
│   ├── llm.py                      # Ollama/LLM integration
│   └── server.py                   # API endpoints
└── ikb_frontend/                   # React frontend
    ├── public/
    ├── src/
    │   ├── App.scss                # SCSS styling
    │   ├── App.tsx                 # Main React component
    │   └── ...
    ├── package.json
    └── ...
```

## 🧪 Key Components

### Semantic Chunking

The system implements intelligent semantic chunking to break down documents into meaningful, context-preserving segments before embedding. This approach:

- Preserves contextual integrity of information
- Increases retrieval accuracy by maintaining semantic coherence
- Optimizes chunk sizes for better vector representation
- Respects document structure (headings, paragraphs, lists)
- Ensures chunks contain complete thoughts rather than arbitrary text splits

### ChromaDB Integration

The system uses ChromaDB for persistent vector storage, allowing for efficient semantic search and automatic updates based on document timestamps.

### Ollama with Mistral

Local LLM inference is handled by Ollama using the Mistral model, providing structured JSON responses with confidence levels and context tracking.

### Material UI Frontend

The modern UI is built with Material UI 7, featuring:

- Dark/light mode toggle
- Responsive chat interface
- Markdown rendering
- Loading indicators
- Custom SCSS styling

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📸 Demo & Screenshots

### Video Demo

A video demonstration of the IKB system is available in the assets folder:

- [Chatting With Your Docs.mp4](./assets/Chatting_With_Your_Docs.mp4)
