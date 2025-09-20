"""
    Interactive Chat Interface for PDF-based RAG System

    This module provides a command-line chat interface that allows users to:
    1. Ask questions about ingested PDF documents
    2. Receive contextual answers based on semantic search
    3. Maintain a conversational flow with proper error handling
    4. Exit gracefully with multiple quit commands

    The interface acts as a bridge between user input and the RAG pipeline,
    providing a user-friendly way to interact with the document knowledge base.
"""

from search import search_prompt

def main() -> None:
    """
    Orchestrates the interactive chat session for PDF document Q&A.
    
    This function manages the complete user interaction lifecycle:
    1. Displays welcome message and usage instructions
    2. Continuously processes user questions through the RAG pipeline
    3. Handles various exit conditions and error scenarios
    4. Provides feedback during processing for better UX
    
    The chat loop continues until the user explicitly exits or interrupts
    the session, ensuring a robust and user-friendly experience.
    
    Raises:
        KeyboardInterrupt: Handled gracefully to allow clean exit
        Exception: All other exceptions are caught and displayed to user
        
    Note:
        Empty input is treated as an exit command for convenience.
        The system provides clear feedback during processing to manage
        user expectations, especially for complex queries that may take time.
    """
    
    # Display welcome message and usage instructions
    # Clear instructions help users understand how to interact with the system
    print("PDF Q&A Chat System")
    print("Type 'quit', 'exit', or 'q' to end the session")
    print("-" * 50)
    
    # Main interaction loop - continues until explicit exit
    while True:
        try:
            # Capture user input with prompt and clean whitespace
            # .strip() removes leading/trailing whitespace for better command matching
            user_question = input("\nAsk your question: ").strip()
            
            # Handle multiple exit conditions for user convenience
            # Empty string allows quick exit by just pressing Enter
            if user_question.lower() in ('quit', 'exit', 'q', ''):
                print("Ending chat session. Goodbye!")
                break
            
            # Provide processing feedback to manage user expectations
            # RAG pipeline can take several seconds, especially for complex queries
            print("\nProcessing...")
            
            # Execute the complete RAG pipeline: search + generation
            # This involves embedding generation, vector search, and LLM inference
            response = search_prompt(user_question)
            
            # Display the generated response with clear formatting
            # .content extracts the text from the LangChain response object
            print(f"\nANSWER: {response.content}")
            print("-" * 50)
            
        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully without showing error traceback
            # Double newline provides clean separation from the interrupted input
            print("\n\nEnding chat session. Goodbye!")
            break
            
        except Exception as e:
            # Catch and display all other errors without crashing the session
            # This ensures the chat continues even if individual queries fail
            print(f"\nError: {str(e)}")
            print("Please try again or type 'quit' to exit.")

if __name__ == "__main__":
    main()