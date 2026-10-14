import numpy as np

def retrieve(
    query: str,
    encoder,
    chunk_vectors,
    chunks,
    top_k: int = 4,
):
    """Retrieve the most relevant chunks for a user query."""

    print("\n[4/5] Retrieving relevant chunks...")

    if not query.strip():
        raise ValueError("Query cannot be empty.")

    if len(chunks) != len(chunk_vectors):
        raise ValueError(
            "The number of chunks must match the number of vectors."
        )

    if len(chunks) == 0:
        return []

    # Convert the user query into an embedding vector.
    query_vector = encoder.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True,
    )[0]

    # Calculate cosine similarity scores.
    scores = chunk_vectors @ query_vector

    # Select the top-k chunks.
    top_k = max(1, min(top_k, len(chunks)))
    top_indices = np.argsort(scores)[::-1][:top_k]

    results = [
        (chunks[i], float(scores[i]))
        for i in top_indices
    ]

    # Display retrieved results.
    for rank, (chunk, score) in enumerate(results, start=1):
        page = chunk.metadata.get("page", "?")
        preview = chunk.page_content.replace("\n", " ")[:140]

        print(
            f"#{rank} score={score:.3f}, "
            f"page={page}: {preview}..."
        )

    return results
