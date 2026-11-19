
from src.retrieval.keyword_search import keyword_search
from src.retrieval.vector_search import vector_search

def reciprocal_rank_fusion(keyword_result, vector_result, k=60):
    result = {}

    for rank, (index, _) in enumerate(keyword_result, start=1):
        rrf_score = 1 / (k + rank)
        result[index] = result.get(index, 0) + rrf_score

    for rank, (index, _) in enumerate(vector_result, start=1):
        rrf_score = 1 / (k + rank)
        result[index] = result.get(index, 0) + rrf_score

    ranked_results = sorted(
        result.items(),
        key=lambda item: item[1],
        reverse=True
    )

    return ranked_results

def hybrid_search(
    query,
    document_chunks,
    query_embedding,
    document_embeddings,
    top_k=3
):
    keyword_result = keyword_search(query, document_chunks)

    vector_result = vector_search(
        query_embedding,
        document_embeddings,
        top_k=top_k
    )

    hybrid_ranking = reciprocal_rank_fusion(
        keyword_result,
        vector_result
    )

    hybrid_results = []

    for index, score in hybrid_ranking:
        matched_chunk = document_chunks[index]
        hybrid_results.append((index, matched_chunk))

    return hybrid_results[:top_k]