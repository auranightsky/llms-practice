from pathlib import Path
import os
from dotenv import load_dotenv

def load_file(filename, readLines=False):
    """Load a file from the project directory or data directory."""

    project_dir = Path(__file__).parent.parent

    # .env file
    if filename == ".env":
        load_dotenv(project_dir / ".env")
        return os.getenv("OPENAI_API_KEY")

    # Files in data/
    input_file = project_dir / "data" / filename

    if not input_file.exists():
        raise FileNotFoundError(f"File not found: {input_file}")

    with open(input_file, "r", encoding="utf-8") as file:
        return file.readlines() if readLines else file.read()