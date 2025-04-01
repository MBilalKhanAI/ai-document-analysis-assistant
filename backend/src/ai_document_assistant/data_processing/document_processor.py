from pathlib import Path
import logging
from typing import List, Optional
from PyPDF2 import PdfReader
from docx import Document
from ..core.config import MAX_FILE_SIZE, SUPPORTED_FILE_TYPES, DATA_DIR

logger = logging.getLogger(__name__)

class DocumentProcessor:
    def __init__(self):
        self.supported_types = SUPPORTED_FILE_TYPES

    def validate_file(self, file_path: Path) -> bool:
        """Validate if a file is supported and within size limits."""
        try:
            if not file_path.exists():
                logger.error(f"File not found: {file_path}")
                return False

            if file_path.stat().st_size > MAX_FILE_SIZE:
                logger.error(f"File too large: {file_path}")
                return False

            file_type = file_path.suffix.lower()
            for mime_type, extensions in self.supported_types.items():
                if file_type in extensions:
                    return True

            logger.error(f"Unsupported file type: {file_path}")
            return False
        except Exception as e:
            logger.error(f"Error validating file {file_path}: {str(e)}")
            return False

    def process_file(self, file_path: Path) -> Optional[str]:
        """Process a file and extract its text content."""
        try:
            if not self.validate_file(file_path):
                return None

            file_type = file_path.suffix.lower()
            if file_type == ".pdf":
                return self._process_pdf(file_path)
            elif file_type in [".doc", ".docx"]:
                return self._process_docx(file_path)
            elif file_type in [".txt", ".md"]:
                return self._process_text(file_path)
            else:
                logger.error(f"Unsupported file type: {file_path}")
                return None
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {str(e)}")
            return None

    def _process_pdf(self, file_path: Path) -> str:
        """Extract text from a PDF file."""
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text

    def _process_docx(self, file_path: Path) -> str:
        """Extract text from a DOCX file."""
        doc = Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text

    def _process_text(self, file_path: Path) -> str:
        """Read text from a text file."""
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    def save_file(self, file_path: Path, content: bytes) -> Optional[Path]:
        """Save an uploaded file to the data directory."""
        try:
            target_path = DATA_DIR / file_path.name
            with open(target_path, "wb") as f:
                f.write(content)
            return target_path
        except Exception as e:
            logger.error(f"Error saving file {file_path}: {str(e)}")
            return None 