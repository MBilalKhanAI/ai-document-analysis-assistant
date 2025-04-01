import logging
from typing import List, Optional
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from ..core.config import OPENAI_API_KEY, CACHE_DIR

logger = logging.getLogger(__name__)

class ChatManager:
    def __init__(self):
        self.llm = ChatOpenAI(
            model_name="gpt-4-turbo-preview",
            temperature=0.7,
            openai_api_key=OPENAI_API_KEY,
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
        )
        self.vector_store = None
        self.chain = None

    def initialize_chain(self, documents: List[str]):
        """Initialize the conversation chain with documents."""
        try:
            # Split documents into chunks
            texts = self.text_splitter.split_documents(documents)
            
            # Create or update vector store
            self.vector_store = Chroma.from_documents(
                documents=texts,
                embedding=self.llm.embeddings,
                persist_directory=str(CACHE_DIR / "chroma"),
            )

            # Create conversation chain
            self.chain = ConversationalRetrievalChain.from_llm(
                llm=self.llm,
                retriever=self.vector_store.as_retriever(),
                memory=self.memory,
                return_source_documents=True,
            )
        except Exception as e:
            logger.error(f"Error initializing chain: {str(e)}")
            raise

    def get_response(self, message: str) -> Optional[str]:
        """Get AI response for a user message."""
        try:
            if not self.chain:
                return "Please upload some documents first."

            result = self.chain({"question": message})
            return result["answer"]
        except Exception as e:
            logger.error(f"Error getting response: {str(e)}")
            return "Sorry, I encountered an error. Please try again."

    def clear_history(self):
        """Clear the conversation history."""
        self.memory.clear()
        if self.vector_store:
            self.vector_store.delete_collection()
            self.vector_store = None
        self.chain = None 