
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer
from paths import OUTPUT_DIR


def vectorize_chunks(chunks, embed_model):
    """Convert document chunks into embeddings and save them."""

    if not chunks:
        raise ValueError("Cannot create embeddings: chunks is empty.")

    print(f"\n[3/5] Vectorizing with {embed_model}...")

    encoder = SentenceTransformer(embed_model)

    texts = [chunk.page_content for chunk in chunks]

    vectors = encoder.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=True,
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    vector_path = OUTPUT_DIR / "embeddings.npy"
    np.save(vector_path, vectors)

    print(f"- embedding shape: {vectors.shape}")
    print(f"- saved: {vector_path}")

    return encoder, vectors
