
from app.services.vector_store import search_chunks
from app.services.llm_service import generate_answer


def answer_question(question, document_id):

    # Step 1: Retrieve relevant chunks
    results = search_chunks(
        query=question,
        document_id=document_id,
        top_k=3
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    if not documents:
        return {
            "answer": "No relevant information found in this document.",
            "sources": []
        }

    # Step 2: Prepare context for the LLM
    context_parts = []

    for text, metadata in zip(documents, metadatas):
        context_parts.append(
            f"Page {metadata['page_number']}: {text}"
        )

    context = "\n\n".join(context_parts)

    # Step 3: Generate the answer
    answer = generate_answer(question, context)

    # Step 4: Remove duplicate source pages
    unique_sources = []
    seen_pages = set()

    for metadata in metadatas:
        page_number = metadata["page_number"]

        if page_number not in seen_pages:
            unique_sources.append(metadata)
            seen_pages.add(page_number)

    # Step 5: Return answer and unique sources
    return {
        "answer": answer,
        "sources": unique_sources
    }
