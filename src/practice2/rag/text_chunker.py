
import json
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.utils.paths import OUTPUT_DIR


def chunk_documents(docs, chunk_size=1000, chunk_overlap=150):
    """Split documents into chunks and save them as JSONL."""

    print("\n[2/5] Chunking...")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", "。", ". ", " ", ""],
    )

    chunks = splitter.split_documents(docs)

    chunks_path = OUTPUT_DIR / "chunks.jsonl"
    chunks_path.parent.mkdir(parents=True, exist_ok=True)

    with chunks_path.open("w", encoding="utf-8") as file:
        for i, chunk in enumerate(chunks):
            chunk.metadata["chunk_id"] = i

            row = {
                "chunk_id": i,
                "page": chunk.metadata.get("page"),
                "text": chunk.page_content,
            }

            file.write(
                json.dumps(row, ensure_ascii=False) + "\n"
            )

    print(f"- chunks: {len(chunks)}")
    print(f"- saved: {chunks_path}")

    return chunks
