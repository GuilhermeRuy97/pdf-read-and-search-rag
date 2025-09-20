"""
    PDF Document Ingestion Pipeline for RAG System

    This module handles the complete pipeline for ingesting PDF documents into a vector database:
    1. Loads and parses PDF files
    2. Splits documents into semantic chunks
    3. Generates embeddings using OpenAI
    4. Stores vectors in PostgreSQL with pgvector extension

    The ingested documents can then be used for semantic search and retrieval-augmented generation.
"""

import os
from dotenv                               import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters             import RecursiveCharacterTextSplitter
from pathlib                              import Path
from langchain_openai                     import OpenAIEmbeddings
from langchain_postgres                   import PGVector
from langchain_core.documents             import Document

# Initialize environment configuration
load_dotenv()

# Validate required environment variables early to fail fast
# These variables are critical for the entire pipeline to function
REQUIRED_ENV_VARS = (
    "OPENAI_API_KEY", 
    "OPENAI_EMBEDDING_MODEL", 
    "DATABASE_URL", 
    "PG_VECTOR_COLLECTION_NAME"
)

for env_var in REQUIRED_ENV_VARS:
    if not os.getenv(env_var):
        raise RuntimeError(f"Environment variable {env_var} is not set")

# Configuration constants - centralized for easy modification
PDF_PATH = os.getenv("PDF_PATH")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL")

def ingest_pdf() -> bool:
    """
    Orchestrates the complete PDF ingestion pipeline for RAG system.
    
    This function performs the following operations:
    1. Loads PDF document from configured path
    2. Splits document into overlapping chunks for better context preservation
    3. Enriches chunks by cleaning metadata
    4. Generates embeddings using OpenAI's embedding model
    5. Stores vectors in PostgreSQL with pgvector for semantic search
    
    Returns:
        bool: True if ingestion completed successfully
        
    Raises:
        SystemExit: If no chunks are generated from the PDF (empty or corrupted file)
        RuntimeError: If required environment variables are missing
        
    Note:
        The function uses overlapping chunks (150 chars) to ensure context isn't lost
        at chunk boundaries, which is crucial for maintaining semantic coherence.
    """
    
    # Load PDF document - PyPDFLoader handles various PDF formats and encodings
    loader = PyPDFLoader(PDF_PATH)
    docs = loader.load()

    # Split documents into manageable chunks for embedding generation
    # chunk_size=1000: Optimal balance between context and embedding model limits
    # chunk_overlap=150: Preserves context across chunk boundaries
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=150
    )
    chunks = splitter.split_documents(docs)

    # Early exit if PDF processing failed or document is empty
    if not chunks:
        raise SystemExit(0)

    # Clean and enrich document metadata by removing empty/null values
    # This prevents storage of unnecessary metadata and improves query performance
    enriched_chunks = [
        Document(
            page_content=chunk.page_content,
            metadata={
                key: value 
                for key, value in chunk.metadata.items() 
                if value not in ("", None)
            }
        )
        for chunk in chunks
    ]

    # Generate unique identifiers for each chunk to enable updates/deletions
    chunk_ids = [f"doc-enriched-{i}" for i in range(len(enriched_chunks))]

    # Initialize OpenAI embeddings with configured model
    # This creates vector representations of text for semantic similarity search
    embeddings = OpenAIEmbeddings(model=OPENAI_EMBEDDING_MODEL)

    # Configure PostgreSQL vector store with pgvector extension
    # use_jsonb=True: Enables efficient metadata querying and filtering
    vector_store = PGVector(
        embeddings=embeddings,
        collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
        connection=os.getenv("DATABASE_URL"),
        use_jsonb=True,
    )

    # Batch insert documents with their embeddings into the vector database
    # This operation generates embeddings and stores them with metadata
    vector_store.add_documents(documents=enriched_chunks, ids=chunk_ids)

    return True


if __name__ == "__main__":
    ingest_pdf()