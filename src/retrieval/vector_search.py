
import math


def cosine_similarity(vector_a, vector_b):

    if len(vector_a) != len(vector_b):
        raise ValueError("Vectors must have the same dimensions.")

    dot_product = sum(
        x * y for x, y in zip(vector_a, vector_b)
    )

    magnitude_a = math.sqrt(sum(x * x for x in vector_a))
    magnitude_b = math.sqrt(sum(y * y for y in vector_b))

    if magnitude_a == 0 or magnitude_b == 0:
        raise ValueError("Cannot calculate similarity for a zero vector.")

    return dot_product / (magnitude_a * magnitude_b)


def vector_search(query_embedding, document_embeddings, top_k=3):

    scores = []

    for index, embedding in enumerate(document_embeddings):
        score = cosine_similarity(query_embedding, embedding)
        scores.append((index, score))

    ranked_scores = sorted(
        scores,
        key=lambda item: item[1],
        reverse=True
    )

    return ranked_scores[:top_k]
