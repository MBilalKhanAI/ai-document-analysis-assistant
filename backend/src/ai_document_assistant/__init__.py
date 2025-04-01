"""AI Document Assistant - An AI-powered document processing and analysis assistant."""

__version__ = "0.1.0"

from .core.config import settings
from .data_processing.document_processor import DocumentProcessor
from .llm.chat_manager import ChatManager

__all__ = ["settings", "DocumentProcessor", "ChatManager"] 