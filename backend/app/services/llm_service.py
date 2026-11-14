import ollama


def generate_answer(question, context):

    response = ollama.chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "system",
                "content": """
You are a PDF research assistant.

Follow these rules strictly:
1. Answer only using information explicitly available in the provided context.
2. Do not assume, guess, or add information from your general knowledge.
3. If information is not available in the context, say:
   'This information is not available in the uploaded document.'
4. Keep answers clear, accurate, and relevant to the question.
5. Do not invent technical skills, experience, or qualifications.
"""
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion:\n{question}"
            }
        ]
    )

    return response["message"]["content"]