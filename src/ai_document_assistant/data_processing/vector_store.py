"""Vector store module for document embeddings and retrieval."""
from pathlib import Path
from typing import List, Optional

from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document

from ..core.config import settings
from ..utils.helpers import ensure_directories, logger


class VectorStore:
    """Vector store for document embeddings and retrieval."""
    
    def __init__(self):
        """Initialize the vector store."""
        ensure_directories()
        self.embeddings = OpenAIEmbeddings()
        self.persist_directory = settings.CACHE_DIR / "chroma"
        self.vector_store = Chroma(
            persist_directory=str(self.persist_directory),
            embedding_function=self.embeddings,
        )
    
    def add_documents(self, documents: List[Document]) -> None:
        """Add documents to the vector store.
        
        Args:
            documents: List of documents to add
        """
        try:
            self.vector_store.add_documents(documents)
            self.vector_store.persist()
            logger.info(f"Added {len(documents)} documents to vector store")
        except Exception as e:
            logger.error(f"Error adding documents to vector store: {str(e)}")
            raise
    
    def similarity_search(
        self, query: str, k: int = 4, filter: Optional[dict] = None
    ) -> List[Document]:
        """Search for similar documents.
        
        Args:
            query: Search query
            k: Number of results to return
            filter: Optional filter criteria
            
        Returns:
            List of similar documents
        """
        try:
            results = self.vector_store.similarity_search(
                query=query,
                k=k,
                filter=filter,
            )
            return results
        except Exception as e:
            logger.error(f"Error searching vector store: {str(e)}")
            raise
    
    def delete_documents(self, ids: List[str]) -> None:
        """Delete documents from the vector store.
        
        Args:
            ids: List of document IDs to delete
        """
        try:
            self.vector_store.delete(ids=ids)
            self.vector_store.persist()
            logger.info(f"Deleted {len(ids)} documents from vector store")
        except Exception as e:
            logger.error(f"Error deleting documents from vector store: {str(e)}")
            raise
    
    def clear(self) -> None:
        """Clear all documents from the vector store."""
        try:
            self.vector_store.delete_collection()
            self.vector_store = Chroma(
                persist_directory=str(self.persist_directory),
                embedding_function=self.embeddings,
            )
            logger.info("Cleared vector store")
        except Exception as e:
            logger.error(f"Error clearing vector store: {str(e)}")
            raise 