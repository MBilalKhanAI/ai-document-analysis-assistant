from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import uuid
from pathlib import Path
import os
import logging

from .core.config import API_TITLE, API_DESCRIPTION, API_VERSION
from .core.search import DocumentSearch
from .data_processing.processor import DocumentProcessor
from .llm.chat import ChatManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
storage_dir = Path("storage")
storage_dir.mkdir(exist_ok=True)
document_search = DocumentSearch(storage_dir)
document_processor = DocumentProcessor()
chat_manager = ChatManager()

class ChatRequest(BaseModel):
    message: str

class SearchResponse(BaseModel):
    results: List[Dict[str, Any]]

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Handle file upload and processing."""
    try:
        # Save the uploaded file
        file_id = str(uuid.uuid4())
        file_path = storage_dir / f"{file_id}_{file.filename}"
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Process the document
        processed_content = document_processor.process_file(file_path)

        # Index the document for search
        document_search.index_document(
            file_id,
            processed_content,
            {
                "filename": file.filename,
                "file_path": str(file_path),
                "file_size": len(content),
            }
        )

        return {"message": f"File {file.filename} uploaded and processed successfully", "filename": file.filename}
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat(request: ChatRequest):
    """Handle chat messages."""
    try:
        response = chat_manager.get_response(request.message)
        return {"response": response}
    except Exception as e:
        logger.error(f"Error in chat: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/search")
async def search_documents(query: str, limit: int = 5):
    """Search for documents."""
    try:
        results = document_search.search(query, limit)
        return SearchResponse(results=results)
    except Exception as e:
        logger.error(f"Error searching documents: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/clear")
async def clear_chat():
    """Clear chat history."""
    try:
        chat_manager.clear_history()
        return {"message": "Chat history cleared successfully"}
    except Exception as e:
        logger.error(f"Error clearing chat: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 