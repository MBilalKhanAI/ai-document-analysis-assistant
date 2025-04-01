import uvicorn
from ai_document_assistant.main import app

if __name__ == "__main__":
    uvicorn.run(
        "ai_document_assistant.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    ) 