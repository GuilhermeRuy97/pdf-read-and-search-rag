# Project Goals

**Ingest**: Read a PDF file and save its information to a PostgreSQL database with the pgVector extension. <br>
**Search**: Allow the user to ask questions via the command line (CLI) and receive answers based solely on the PDF content.

## Stack

**Language**: Python <br>
**Framework**: LangChain <br>
**Database**: PostgreSQL + pgVector <br>
**Database execution**: Docker & Docker Compose <br>

## Solution

- _placeholder_

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
