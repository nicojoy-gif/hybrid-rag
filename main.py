
from pathlib import Path

from src.ingestion.loader import load_and_chunk_document
from src.embeddings.embedder import generate_embeddings, generate_embedding
from src.retrieval.hybrid_search import hybrid_search
from src.generation.answer import generate_answer


DATA_DIR = Path("data/raw")
ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}


def load_knowledge_base():
    all_chunks = []
    chunk_metadata = []

    for file_path in DATA_DIR.iterdir():

        if not file_path.is_file():
            continue

        if file_path.suffix.lower() not in ALLOWED_EXTENSIONS:
            continue

        document_chunks = load_and_chunk_document(file_path)

        for index, chunk in enumerate(document_chunks):
            all_chunks.append(chunk)

            chunk_metadata.append({
                "document": file_path.name,
                "chunk_index": index
            })

    document_embeddings = (
        generate_embeddings(all_chunks) if all_chunks else []
    )

    return all_chunks, document_embeddings, chunk_metadata


def refresh_knowledge_base():
    global document_chunks, document_embeddings, chunk_metadata

    document_chunks, document_embeddings, chunk_metadata = (
        load_knowledge_base()
    )

    print(f"Knowledge base refreshed: {len(document_chunks)} chunks loaded.")


document_chunks = []
document_embeddings = []
chunk_metadata = []

refresh_knowledge_base()


def run_rag_pipeline(query):

    if not document_chunks:
        return {
            "answer": "The knowledge base is empty. Please upload documents first.",
            "sources": []
        }

    query_embedding = generate_embedding(query)

    hybrid_result = hybrid_search(
        query,
        document_chunks,
        query_embedding,
        document_embeddings
    )

    if not hybrid_result:
        return {
            "answer": "I couldn't find relevant information in the knowledge base to answer your question.",
            "sources": []
        }

    retrieved_chunks = [chunk[1] for chunk in hybrid_result]

    sources = [
        chunk_metadata[chunk[0]]
        for chunk in hybrid_result
    ]

    answer = generate_answer(query, retrieved_chunks)

    return {
        "answer": answer,
        "sources": sources
    }
