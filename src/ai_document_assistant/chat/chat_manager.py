"""Chat manager module for handling conversations with the AI."""
from typing import List, Optional

from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate
from langchain.schema import Document

from ..core.config import settings
from ..data_processing.vector_store import VectorStore
from ..utils.helpers import logger


class ChatManager:
    """Manages chat interactions with the AI."""
    
    def __init__(self, vector_store: VectorStore):
        """Initialize the chat manager.
        
        Args:
            vector_store: Vector store for document retrieval
        """
        self.vector_store = vector_store
        self.llm = ChatOpenAI(
            model_name=settings.MODEL_NAME,
            temperature=settings.TEMPERATURE,
            max_tokens=settings.MAX_TOKENS,
        )
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            max_history_length=settings.MAX_HISTORY_LENGTH,
        )
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a helpful AI assistant that answers questions about documents.
            Use the following context to answer the user's question. If you cannot find the answer in the context,
            say so. Always cite your sources using the document metadata.
            
            Context: {context}
            
            Chat History: {chat_history}
            
            Question: {question}
            
            Answer: """),
        ])
    
    def get_relevant_documents(self, query: str) -> List[Document]:
        """Get relevant documents for the query.
        
        Args:
            query: User's question
            
        Returns:
            List of relevant documents
        """
        return self.vector_store.similarity_search(query)
    
    def format_context(self, documents: List[Document]) -> str:
        """Format documents into context string.
        
        Args:
            documents: List of documents
            
        Returns:
            Formatted context string
        """
        context = []
        for doc in documents:
            content = doc.page_content
            source = doc.metadata.get("source", "Unknown")
            context.append(f"From {source}:\n{content}")
        return "\n\n".join(context)
    
    def get_response(self, question: str) -> str:
        """Get AI response to user question.
        
        Args:
            question: User's question
            
        Returns:
            AI's response
        """
        try:
            # Get relevant documents
            documents = self.get_relevant_documents(question)
            context = self.format_context(documents)
            
            # Generate response
            chain = self.prompt | self.llm
            response = chain.invoke({
                "context": context,
                "chat_history": self.memory.chat_memory.messages,
                "question": question,
            })
            
            # Update memory
            self.memory.chat_memory.add_user_message(question)
            self.memory.chat_memory.add_ai_message(response.content)
            
            return response.content
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise
    
    def clear_history(self) -> None:
        """Clear chat history."""
        self.memory.clear()
        logger.info("Cleared chat history") 