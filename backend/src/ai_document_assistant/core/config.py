from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
API_VERSION = "0.1.0"
API_TITLE = "AI Document Assistant API"
API_DESCRIPTION = "API for processing and analyzing documents using AI"

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

# File Processing Configuration
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", "10485760"))  # 10MB default
SUPPORTED_FILE_TYPES = {
    "application/pdf": [".pdf"],
    "application/msword": [".doc"],
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [".docx"],
    "text/plain": [".txt"],
    "text/markdown": [".md"],
}

# Directory Configuration
BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data"
CACHE_DIR = BASE_DIR / "cache"

# Create necessary directories
DATA_DIR.mkdir(exist_ok=True)
CACHE_DIR.mkdir(exist_ok=True)
(CACHE_DIR / "chroma").mkdir(exist_ok=True)

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO") 