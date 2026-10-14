import pytest
from pathlib import Path
from unittest.mock import Mock, patch

# Change this import if utils.py is in a different location
from src import utils


@pytest.fixture
def project_dir(tmp_path, monkeypatch):
    """Create a temporary project directory."""
    project = tmp_path
    data_dir = project / "data"
    src_dir = project / "src"

    data_dir.mkdir()
    src_dir.mkdir()

    # Make load_file() use the temporary project directory
    monkeypatch.setattr(
        utils,
        "__file__",
        str(src_dir / "utils.py")
    )

    return project


def test_load_text_file(project_dir):
    """Test reading a text file."""
    file_path = project_dir / "data" / "notes.txt"
    file_path.write_text("Hello, world!", encoding="utf-8")

    result = utils.load_file("notes.txt")

    assert result == "Hello, world!"


def test_load_text_file_as_lines(project_dir):
    """Test reading a text file line by line."""
    file_path = project_dir / "data" / "notes.txt"
    file_path.write_text("First line\nSecond line\n", encoding="utf-8")

    result = utils.load_file("notes.txt", readLines=True)

    assert result == ["First line\n", "Second line\n"]


def test_load_pdf_file(project_dir):
    """Test PDF parsing with a mocked MinerU loader."""
    file_path = project_dir / "data" / "manual.pdf"
    file_path.write_bytes(b"%PDF-mock")

    mock_doc = Mock()
    mock_doc.page_content = "Extracted PDF text"
    mock_doc.metadata = {"page": 1}

    with patch.object(
        utils,
        "MinerULoader"
    ) as mock_loader:
        mock_loader.return_value.load.return_value = [mock_doc]

        result = utils.load_file("manual.pdf")

        mock_loader.assert_called_once_with(
            source=str(file_path),
            mode="flash",
            language="korean",
            split_pages=False,
        )

        assert len(result) == 1
        assert result[0].page_content == "Extracted PDF text"


def test_missing_file_raises_error(project_dir):
    """Test that a missing file raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        utils.load_file("missing.txt")


def test_load_env_file(project_dir, monkeypatch):
    """Test loading the API key from .env."""
    env_file = project_dir / ".env"
    env_file.write_text(
        "OPENAI_API_KEY=test-key",
        encoding="utf-8"
    )

    with patch.object(utils, "load_dotenv") as mock_load_dotenv:
        monkeypatch.setenv("OPENAI_API_KEY", "test-key")

        result = utils.load_file(".env")

        mock_load_dotenv.assert_called_once_with(env_file)
        assert result == "test-key"