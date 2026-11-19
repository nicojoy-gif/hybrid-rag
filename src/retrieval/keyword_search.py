
import re
import string


STOP_WORDS = {"what", "is", "the", "a", "how", "does"}


def keyword_search(query, document_chunks):
    query_items = {
        word.strip(string.punctuation).lower()
        for word in query.split()
        if word.strip(string.punctuation).lower() not in STOP_WORDS
        and word.strip(string.punctuation)
    }

    results = []

    for index, chunk in enumerate(document_chunks):
        chunk_words = set(re.findall(r"\b[\w-]+\b", chunk.lower()))

        score = sum(
            1 for word in query_items if word in chunk_words
        )

        if score > 0:
            results.append((index, score))

    results.sort(key=lambda item: item[1], reverse=True)

    return results
