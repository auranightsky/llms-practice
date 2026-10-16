
from pathlib import Path
from langchain_mineru import MinerULoader
from src.utils.paths import OUTPUT_DIR, PROJECT_DIR

def parse_manual(manual_path, mode="flash"):
    """Parse a manual using MinerU and save results as Markdown."""

    manual_path = Path(manual_path).resolve()

    if not manual_path.exists():
        raise FileNotFoundError(f"File not found: {manual_path}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Project root: {PROJECT_DIR}")
    print(f"Output folder: {OUTPUT_DIR}")
    print(f"\n[1/5] Parsing with MinerU (mode={mode})...")

    loader = MinerULoader(
        source=str(manual_path),
        mode=mode,
        language="korean",
        split_pages=False,
    )

    docs = loader.load()

    parsed_path = OUTPUT_DIR / "parsed.md"

    with parsed_path.open("w", encoding="utf-8") as file:
        for i, doc in enumerate(docs, start=1):
            page = doc.metadata.get("page", i)
            file.write(f"\n\n<!-- PAGE {page} -->\n\n")
            file.write(doc.page_content)

    print(f"- parsed documents/pages: {len(docs)}")
    print(f"- saved: {parsed_path}")

    return docs
