# Knowbase – Internal Knowledge Assistant

Knowbase is an AI-powered internal knowledge assistant that allows employees to ask questions about company documents and receive answers based on the information stored in a central knowledge base.

It uses Retrieval-Augmented Generation (RAG) with hybrid search to retrieve relevant information from uploaded documents before generating responses.

## Features

- **Document ingestion:** Upload PDF, DOCX, and TXT files.
- **Text processing:** Extract, clean, and split documents into smaller chunks.
- **Embedding generation:** Generate document embeddings using Ollama and Nomic Embed Text.
- **Vector search:** Retrieve relevant information using cosine similarity.
- **Keyword search:** Find relevant document chunks through keyword matching.
- **Hybrid search:** Combine keyword and vector search using Reciprocal Rank Fusion (RRF).
- **AI-generated answers:** Generate responses using a local Ollama language model.
- **Source references:** Return document names and chunk references used to generate answers.
- **Document management:** Upload, list, and open documents through the API.
- **Frontend integration:** Connect the backend to a Next.js dashboard.

## Tech Stack

### Backend
- Python
- FastAPI
- Ollama
- Nomic Embed Text
- Pydantic
- PyPDF
- python-docx

### Frontend
- Next.js
- React
- TypeScript
- Tailwind CSS

## Project Structure

```text
hybrid-rag/
│
├── api.py
├── main.py
├── requirements.txt
├── README.md
│
├── data/
│   └── raw/
│       └── uploaded documents
│
└── src/
    ├── ingestion/
    │   └── loader.py
    │
    ├── processing/
    │   ├── cleaner.py
    │   └── chunker.py
    │
    ├── embeddings/
    │   └── embedder.py
    │
    ├── retrieval/
    │   ├── vector_search.py
    │   ├── keyword_search.py
    │   └── hybrid_search.py
    │
    └── generation/
        └── answer.py
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/nicojoy-gif/hybrid-rag
cd hybrid-rag
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Ollama

Download and install Ollama from:

https://ollama.com/

Pull the required models:

```bash
ollama pull llama3.2:1b
ollama pull nomic-embed-text
```

Ensure Ollama is running before starting the backend.

## Running the Backend

From the `hybrid-rag` directory, run:

```bash
uvicorn api:app --reload
```

The API will be available at:

`http://127.0.0.1:8000`

Interactive API documentation:

`http://127.0.0.1:8000/docs`

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Check API status |
| POST | `/ask` | Ask a question |
| POST | `/documents/upload` | Upload and index a document |
| GET | `/documents` | Retrieve uploaded documents |
| GET | `/documents/{filename}/view` | Open a document |

### Asking a Question

Example request:

```json
{
  "question": "What should an employee do when requesting time off?"
}
```

Example response:

```json
{
  "question": "What should an employee do when requesting time off?",
  "answer": "The employee should notify their manager before their scheduled absence.",
  "sources": [
    {
      "document": "Employee-Handbook-Template.pdf",
      "chunk_index": 5
    }
  ]
}
```

## How Hybrid Search Works

Knowbase uses two retrieval techniques:

**1. Keyword Search**

Finds document chunks containing words that match the user's question.

**2. Vector Search**

Converts the question into an embedding and compares it with document embeddings using cosine similarity.

**3. Reciprocal Rank Fusion (RRF)**

Combines the rankings from keyword search and vector search to produce a unified ranking of relevant document chunks.

**4. Answer Generation**

The retrieved chunks are passed to the language model, which generates an answer using the available context.

## Frontend Setup

The frontend is maintained separately in a Next.js project.

Create a `.env.local` file in the frontend project:

```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

Install dependencies and start the development server:

```bash
npm install
npm run dev
```

The frontend will be available at:

`http://localhost:3000`

## Limitations

- The knowledge base is currently stored and indexed in memory.
- Documents are reprocessed when the backend starts.
- The current implementation uses a local language model.
- Retrieval quality depends on document quality, chunking, and embedding performance.
- The current implementation is designed as a local development MVP.

## Future Improvements

- Persistent vector database storage.
- Improved document relevance filtering.
- Better retrieval evaluation and answer quality testing.
- Support for additional document formats.
- Authentication and role-based access control.
- Production deployment and monitoring.

## Author

Built as a practical AI Engineering project exploring Retrieval-Augmented Generation, hybrid retrieval, embeddings, and local language models.