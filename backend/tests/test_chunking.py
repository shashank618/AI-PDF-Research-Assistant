from app.services.chunking_service import create_chunks

sample_pages = [
    {
        "page_number": 1,
        "text": "Artificial Intelligence is a field of computer science. " * 40
    },
    {
        "page_number": 2,
        "text": "Machine Learning is a subset of Artificial Intelligence. " * 40
    }
]

chunks = create_chunks(sample_pages)

print("Total chunks:", len(chunks))

for chunk in chunks:
    print("\nPage:", chunk["page_number"])
    print("Chunk:", chunk["text"][:100])