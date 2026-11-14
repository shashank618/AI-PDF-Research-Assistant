from app.services.llm_service import generate_answer

question = "Which framework is used to build Python APIs?"

context = """
FastAPI is a Python web framework.
Python is a programming language.
"""

answer = generate_answer(question, context)

print("Question:", question)
print("\nAI Generated Answer:")
print(answer)