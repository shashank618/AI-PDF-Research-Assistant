from uuid import uuid4
from app.services.vector_store import store_chunks, collection

document_id = str(uuid4())

sample_chunks = [
    {
        "text": "Python is a programming language.",
        "page_number": 1
    },
    {
        "text": "FastAPI is a Python web framework.",
        "page_number": 2
    }
]

store_chunks(sample_chunks, document_id)

results = collection.get(
    where={"document_id": document_id},
    include=["documents", "metadatas"]
)

print("Stored chunks:", len(results["ids"]))
print("Documents:", results["documents"])
print("Metadata:", results["metadatas"])



from app.services.vector_store import search_chunks

query = "Which framework is used to build Python APIs?"

search_results = search_chunks(query, document_id)

print("\nSearch Results:")
print(search_results["documents"])
print(search_results["metadatas"])