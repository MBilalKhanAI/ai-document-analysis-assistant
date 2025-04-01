"""Document processing module for handling different file types."""
from pathlib import Path
from typing import List, Optional

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    UnstructuredWordDocumentLoader,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter

from ..core.config import settings
from ..utils.helpers import validate_file, get_file_info, logger


class DocumentProcessor:
    """Process and split documents into chunks."""
    
    def __init__(self):
        """Initialize the document processor."""
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", " ", ""],
        )
    
    def load_document(self, file_path: Path) -> List[str]:
        """Load and process a document based on its file type.
        
        Args:
            file_path: Path to the document file
            
        Returns:
            List of document chunks
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If the file type is not supported or file is too large
        """
        if not validate_file(file_path):
            raise ValueError(f"Invalid file: {file_path}")
            
        try:
            # Load document based on file type
            if file_path.suffix.lower() == ".pdf":
                loader = PyPDFLoader(str(file_path))
            elif file_path.suffix.lower() in [".doc", ".docx"]:
                loader = UnstructuredWordDocumentLoader(str(file_path))
            else:  # .txt, .md
                loader = TextLoader(str(file_path))
                
            # Load and split the document
            documents = loader.load()
            chunks = self.text_splitter.split_documents(documents)
            
            # Add file info to metadata
            file_info = get_file_info(file_path)
            for chunk in chunks:
                chunk.metadata.update(file_info)
            
            logger.info(f"Successfully processed document: {file_path}")
            return [chunk.page_content for chunk in chunks]
            
        except Exception as e:
            logger.error(f"Error processing document {file_path}: {str(e)}")
            raise
    
    def process_documents(self, file_paths: List[Path]) -> List[str]:
        """Process multiple documents and combine their chunks.
        
        Args:
            file_paths: List of paths to document files
            
        Returns:
            Combined list of document chunks
            
        Raises:
            ValueError: If any document is invalid
        """
        all_chunks = []
        for file_path in file_paths:
            try:
                chunks = self.load_document(file_path)
                all_chunks.extend(chunks)
            except Exception as e:
                logger.error(f"Failed to process {file_path}: {str(e)}")
                continue
                
        if not all_chunks:
            raise ValueError("No valid documents were processed")
            
        return all_chunks 