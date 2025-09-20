# Project Goals

**Ingest**: Read a PDF file and save its information to a PostgreSQL database with the pgVector extension. <br>
**Search**: Allow the user to ask questions via the command line (CLI) and receive answers based solely on the PDF content.

## Stack

**Language**: Python <br>
**Framework**: LangChain <br>
**Database**: PostgreSQL + pgVector <br>
**Database execution**: Docker & Docker Compose <br>

## Solution

This project implements a **Retrieval-Augmented Generation (RAG)** system that enables users to ask questions about PDF documents and receive accurate, contextual answers. The solution consists of three main components:

### 1. Document Ingestion Pipeline (`ingest.py`)
- **PDF Processing**: Loads and parses PDF documents using PyPDFLoader
- **Text Chunking**: Splits documents into overlapping chunks (1000 chars with 150 char overlap) to preserve context
- **Embedding Generation**: Creates vector representations using OpenAI's embedding model (`text-embedding-3-small`)
- **Vector Storage**: Stores embeddings in PostgreSQL with pgVector extension for efficient similarity search
- **Metadata Enrichment**: Cleans and optimizes document metadata for better query performance

### 2. Semantic Search Engine (`search.py`)
- **Query Processing**: Converts user questions into embeddings using the same model as ingestion
- **Similarity Search**: Retrieves top-10 most relevant document chunks using vector similarity
- **Context Assembly**: Aggregates retrieved chunks into unified context for the language model
- **Response Generation**: Uses GPT-5-nano with temperature=0 for deterministic, factual responses
- **Hallucination Prevention**: Implements strict prompt engineering to ensure answers are based only on document content

### 3. Interactive Chat Interface (`chat.py`)
- **User Experience**: Provides a command-line interface for natural conversation with the document
- **Error Handling**: Robust exception handling ensures continuous operation even when individual queries fail
- **Multiple Exit Options**: Supports various quit commands (`quit`, `exit`, `q`, or empty input) for user convenience
- **Processing Feedback**: Shows "Processing..." message to manage user expectations during query execution

### Key Features
- **Context Preservation**: Overlapping chunks ensure no information is lost at boundaries
- **Factual Accuracy**: Strict context-only responses prevent AI hallucinations
- **Scalable Architecture**: PostgreSQL + pgVector handles large document collections efficiently
- **Deterministic Responses**: Zero temperature ensures consistent answers for the same questions
- **Graceful Error Handling**: System continues operating even when individual components encounter issues

### Workflow
1. **Ingestion**: PDF → Chunks → Embeddings → Vector Database
2. **Query**: User Question → Query Embedding → Similarity Search → Context Retrieval
3. **Generation**: Context + Question → LLM → Grounded Response
4. **Interaction**: Continuous chat loop with proper error handling and user feedback

## Project Structure

├── docker-compose.yml <br>
├── requirements.txt      &nbsp;&nbsp;&nbsp;# Dependencies <br>
├── .env.example          &nbsp;&nbsp;&nbsp;# Environment variables template <br>
├── src/ <br>
│   ├── ingest.py         &nbsp;&nbsp;&nbsp;# Script - Ingest PDF <br>
│   ├── search.py         &nbsp;&nbsp;&nbsp;# Script - Search <br>
│   ├── chat.py           &nbsp;&nbsp;&nbsp;# CLI for user iteraction <br>
├── document.pdf          &nbsp;&nbsp;&nbsp;# PDF to be used <br>
└── README.md

## Execution Steps

1. Clone the repository
2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up credentials:

   a. Create `.env` file based on `.env.example`:
   ```bash
   GOOGLE_API_KEY = "change_me"
   GOOGLE_EMBEDDING_MODEL = 'models/embedding-001'
   OPENAI_API_KEY = "change_me"
   OPENAI_EMBEDDING_MODEL = 'text-embedding-3-small'
   DATABASE_URL = "change_me"
   PG_VECTOR_COLLECTION_NAME = "change_me"
   PDF_PATH = "change_me"
   ```

5. Push Database
`docker compose up -d`

6. Execute PDF Ingestion
`python src/ingest.py`

7. Run Chat
`python src/chat.py`

## Author

- [GuilhermeRuy97](https://github.com/GuilhermeRuy97) - September 2025
