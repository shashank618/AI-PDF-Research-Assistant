

import chromadb

from app.services.embedding_service import generate_embedding


# Step 1: Create ChromaDB persistent client
client = chromadb.PersistentClient(
    path="./chroma_db"
)


# Step 2: Create or get collection
collection = client.get_or_create_collection(
    name="pdf_documents"
)


# Step 3: Store PDF chunks in ChromaDB
def store_chunks(chunks, document_id):

    for index, chunk in enumerate(chunks):

        # Generate embedding for each chunk
        embedding = generate_embedding(chunk["text"])

        # Store text, embedding and metadata
        collection.add(
            ids=[f"{document_id}_{index}"],
            documents=[chunk["text"]],
            embeddings=[embedding.tolist()],
            metadatas=[{
                "document_id": document_id,
                "page_number": chunk["page_number"]
            }]
        )


# Step 4: Search relevant chunks
def search_chunks(query, document_id, top_k=3):

    # Validate document ID
    existing_document = collection.get(
        where={"document_id": document_id},
        limit=1
    )

    if not existing_document["ids"]:
        raise ValueError("Document ID not found")

    # Generate query embedding
    query_embedding = generate_embedding(query)

    # Search in ChromaDB
    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k,
        where={"document_id": document_id}
    )

    return results

     # Step 5: Delete all chunks belonging to a document
def delete_document_chunks(document_id):

    collection.delete(
        where={"document_id": document_id}
    )