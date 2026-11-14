from app.services.rag_service import answer_question

document_id = "31e11816-fa65-46f8-af20-937e44fd42c3"

question = "Which framework is used to build Python APIs?"

result = answer_question(
    question=question,
    document_id=document_id
)

print("Question:", question)
print("\nGenerated Answer:")
print(result["answer"])

print("\nSource Pages:")
for source in result["sources"]:
    print("Page:", source["page_number"])