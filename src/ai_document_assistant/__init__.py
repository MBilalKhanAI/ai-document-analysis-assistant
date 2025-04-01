"""AI Document Assistant - An AI-powered document processing and analysis assistant."""

__version__ = "0.1.0"

from .core.config import settings
from .data_processing import DocumentProcessor, VectorStore
from .chat import ChatManager
from .ui import main, start, process_file, setup_agent

__all__ = [
    "settings",
    "DocumentProcessor",
    "VectorStore",
    "ChatManager",
    "main",
    "start",
    "process_file",
    "setup_agent",
] 