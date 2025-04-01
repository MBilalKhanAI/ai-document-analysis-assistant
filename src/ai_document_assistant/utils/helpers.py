"""Utility functions for the AI Document Assistant."""
import logging
from pathlib import Path
from typing import List, Optional

from ..core.config import settings

# Configure logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def validate_file(file_path: Path) -> bool:
    """Validate if a file meets the requirements.
    
    Args:
        file_path: Path to the file to validate
        
    Returns:
        bool: True if file is valid, False otherwise
    """
    if not file_path.exists():
        logger.error(f"File not found: {file_path}")
        return False
        
    if file_path.stat().st_size > settings.MAX_FILE_SIZE:
        logger.error(f"File too large: {file_path}")
        return False
        
    if file_path.suffix.lower() not in settings.SUPPORTED_FILE_TYPES:
        logger.error(f"Unsupported file type: {file_path.suffix}")
        return False
        
    return True


def get_file_info(file_path: Path) -> dict:
    """Get information about a file.
    
    Args:
        file_path: Path to the file
        
    Returns:
        dict: File information including size, type, and name
    """
    return {
        "name": file_path.name,
        "type": file_path.suffix.lower(),
        "size": file_path.stat().st_size,
        "created": file_path.stat().st_ctime,
        "modified": file_path.stat().st_mtime,
    }


def ensure_directories() -> None:
    """Ensure all required directories exist."""
    settings.DATA_DIR.mkdir(exist_ok=True)
    settings.CACHE_DIR.mkdir(exist_ok=True)
    (settings.CACHE_DIR / "chroma").mkdir(exist_ok=True) 