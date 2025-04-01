# AI Document Assistant

A powerful AI-powered document processing and analysis assistant that helps you understand and interact with your documents using OpenAI's advanced language models.

## Features

- 📄 Process and analyze various document formats (PDF, DOC, DOCX, TXT, MD)
- 🤖 Interactive chat interface for document Q&A
- 🔍 Advanced document search and retrieval
- 💡 Smart document summarization
- 🔄 Real-time document processing
- 📊 Document insights and analytics

## Project Structure

```
ai-document-assistant/
├── frontend/                 # Next.js frontend application
│   ├── src/
│   │   ├── app/             # Next.js app directory
│   │   ├── components/      # React components
│   │   ├── types/          # TypeScript type definitions
│   │   └── api.config.ts    # API configuration
│   └── package.json
├── backend/                  # FastAPI backend application
│   ├── src/
│   │   └── ai_document_assistant/
│   │       ├── core/        # Core functionality
│   │       ├── data_processing/  # Document processing
│   │       └── llm/         # Language model integration
│   └── requirements.txt
└── README.md
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/MBilalKhanAI/ai-document-analysis-assistant.git
cd ai-document-analysis-assistant
```

2. Set up the backend:
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your OpenAI API key
```

3. Set up the frontend:
```bash
cd frontend
npm install
cp .env.example .env.local
# Edit .env.local with your configuration
```

## Usage

1. Start the backend server:
```bash
cd backend
uvicorn src.ai_document_assistant.main:app --reload
```

2. Start the frontend development server:
```bash
cd frontend
npm run dev
```

3. Open your browser and navigate to http://localhost:3000

## Development

### Frontend
- Run tests: `npm test`
- Lint code: `npm run lint`
- Type checking: `npm run type-check`

### Backend
- Run tests: `pytest`
- Format code: `black .`
- Type checking: `mypy .`
- Lint code: `ruff .`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for providing the language models
- LangChain for the document processing framework
- Next.js and FastAPI for the web framework
