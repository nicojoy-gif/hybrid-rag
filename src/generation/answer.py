
import ollama

MODEL_NAME = "llama3.2:1b"

def generate_answer(query, context):

    if not context:
        return "I couldn't find relevant information in the knowledge base to answer your question."

    prompt = f"""
You are an internal company knowledge assistant.

STRICT RULES:
1. Answer using only facts explicitly stated in the context.
2. Consider all provided context before answering.
3. Give a direct answer when relevant information exists.
4. If the answer is unavailable, clearly say so.
5. Do not invent facts, explanations, dates, or instructions.
6. Do not mix information belonging to different error codes.
7. Identify the most relevant error code when the question concerns an error.
8. Only include causes and fixes belonging to that error code.
9. Do not introduce unrelated information.
10. Keep answers concise and factual.

CONTEXT:
{chr(10).join(context)}

QUESTION:
{query}

ANSWER:
"""

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"].strip()