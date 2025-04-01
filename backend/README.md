# AI Document Assistant Backend

This is the backend service for the AI Document Assistant, providing document processing and AI-powered chat functionality.

## Features

- Document upload and processing (PDF, DOCX, TXT, MD)
- AI-powered document analysis and chat
- Vector store for efficient document retrieval
- RESTful API endpoints

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Running the Application

1. Start the FastAPI server:
```bash
python run.py
```

2. The API will be available at `http://localhost:8000`

3. Access the API documentation at:
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

## API Endpoints

- `POST /api/upload`: Upload and process a document
- `POST /api/chat`: Send a message to the AI assistant
- `POST /api/clear`: Clear the chat history
- `GET /api/health`: Health check endpoint

## Project Structure

```
backend/
├── src/
│   └── ai_document_assistant/
│       ├── core/
│       │   ├── __init__.py
│       │   └── config.py
│       ├── data_processing/
│       │   ├── __init__.py
│       │   └── document_processor.py
│       ├── llm/
│       │   ├── __init__.py
│       │   └── chat_manager.py
│       ├── __init__.py
│       └── main.py
├── requirements.txt
├── run.py
└── README.md
```

## Development

The backend is built with:
- FastAPI for the web framework
- LangChain for AI document processing
- ChromaDB for vector storage
- OpenAI's GPT-4 for chat functionality

## License

This project is licensed under the MIT License - see the LICENSE file for details. 