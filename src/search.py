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

def search_prompt(question=None):
    pass