"""
  Semantic Search and RAG Query Engine

  This module implements the query/search functionality for the RAG system:
  1. Performs semantic similarity search against the vector database
  2. Retrieves relevant document chunks based on user queries
  3. Uses retrieved context to generate accurate, grounded responses
  4. Implements strict context-only answering to prevent hallucinations

  The search engine ensures responses are always based on the ingested documents,
  maintaining factual accuracy and preventing the model from generating information
  not present in the source material.
"""

import os
from dotenv             import load_dotenv
from langchain_openai   import OpenAIEmbeddings, ChatOpenAI
from langchain_postgres import PGVector
from langchain.prompts  import PromptTemplate

# Initialize environment configuration
load_dotenv()

# Validate required environment variables early to fail fast
# These variables are critical for the search and generation pipeline
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

# RAG Prompt Template - Designed to enforce strict context adherence
PROMPT_TEMPLATE = """
CONTEXT:
{context}

RULES:
- Answer only based on the CONTEXT.
- If the information is not explicitly in the CONTEXT, respond:
  "I don't have the necessary information to answer your question."
- Never invent or use external knowledge.
- Never produce opinions or interpretations beyond what is written.

EXAMPLES OF QUESTIONS OUTSIDE THE CONTEXT:
Question: "What is the capital of France?"
Answer: "I don't have the necessary information to answer your question."

Question: "How many clients do we have in 2024?"
Answer: "I don't have the necessary information to answer your question."

Question: "Do you think this is good or bad?"
Answer: "I don't have the necessary information to answer your question."

USER QUESTION:
{question}

ANSWER THE "USER QUESTION"
"""

def search_prompt(user_question: str = None) -> str:
    """
    Executes semantic search and generates contextual responses using RAG pipeline.
    
    This function orchestrates the complete RAG query process:
    1. Converts user question to embeddings for semantic similarity
    2. Retrieves top-k most relevant document chunks from vector database
    3. Constructs context from retrieved chunks
    4. Generates response using LLM with strict context constraints
    
    Args:
        user_question (str, optional): The user's query to search for.
                                     If None, function can be used for testing.
    
    Returns:
        str: Generated response based strictly on retrieved document context
        
    Raises:
        RuntimeError: If required environment variables are missing
        
    Note:
        - Uses k=10 to retrieve top 10 most similar chunks for comprehensive context
        - Temperature=0 ensures deterministic, factual responses
        - Similarity scores are available but currently not used in response generation
    """

    # Initialize embeddings model - same model used during ingestion for consistency
    # This ensures query embeddings are in the same vector space as stored documents
    embeddings = OpenAIEmbeddings(model=OPENAI_EMBEDDING_MODEL)

    # Connect to PostgreSQL vector store with same configuration as ingestion
    # use_jsonb=True enables efficient metadata filtering if needed in future
    vector_store = PGVector(
        embeddings=embeddings,
        collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
        connection=os.getenv("DATABASE_URL"),
        use_jsonb=True,
    )

    # Perform semantic similarity search with scoring
    # k=10: Retrieves top 10 most relevant chunks to provide comprehensive context
    # Higher k values provide more context but may introduce noise
    similarity_results = vector_store.similarity_search_with_score(user_question, k=10)

    # Aggregate retrieved document chunks into unified context
    context = "\n\n".join([doc.page_content for doc, _ in similarity_results])

    # Create prompt template with strict context adherence rules
    # This template is designed to prevent hallucinations and ensure factual responses
    question_template = PromptTemplate(
        input_variables=["question", "context"],
        template=PROMPT_TEMPLATE
    )

    # Initialize language model with deterministic settings
    # temperature=0: Ensures consistent, factual responses without creativity
    # gpt-5-nano: Lightweight model suitable for context-based Q&A tasks
    language_model = ChatOpenAI(model="gpt-5-nano", temperature=0)

    # Create processing chain: template -> model
    # This pipeline ensures consistent prompt formatting and response generation
    processing_chain = question_template | language_model

    # Generate response by invoking the complete RAG pipeline
    response = processing_chain.invoke({
        "question": user_question, 
        "context": context
    })

    # Debug code for analyzing search results (currently commented out)
    # Useful for understanding retrieval quality and similarity scores
    # for i, (doc, score) in enumerate(similarity_results, start=1):
    #     print("="*50)
    #     print(f"Result {i} (similarity score: {score:.2f}):")
    #     print("="*50)
    #     print("\nContent:\n")
    #     print(doc.page_content.strip())
    #     print("\nMetadata:\n")
    #     for key, value in doc.metadata.items():
    #         print(f"{key}: {value}")

    return response

if __name__ == "__main__":
    search_prompt()