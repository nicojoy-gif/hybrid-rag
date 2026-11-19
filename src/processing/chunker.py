def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    words = text.split()
    
    while start < len(words):
        chunk = words[start:start + chunk_size]
        chunks.append(" ".join(chunk))
        start += chunk_size - overlap
    return chunks

