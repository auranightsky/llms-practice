
from pathlib import Path

# Find the project root by locating its expected folders.
current = Path(__file__).resolve()

PROJECT_DIR = next(
    (
        parent
        for parent in current.parents
        if (parent / "src").is_dir()
        and (parent / "data").is_dir()
        and (parent / "experiments").is_dir()
    ),
    None,
)

if PROJECT_DIR is None:
    raise FileNotFoundError(
        "Could not find the project root containing src/, data/, and experiment/."
    )

OUTPUT_DIR = PROJECT_DIR / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("Project root:", PROJECT_DIR)
print("Output folder:", OUTPUT_DIR)
