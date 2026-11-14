# AI-Powered PDF Research Assistant

An AI-powered application that allows users to upload PDF documents, ask questions, and receive context-aware answers using Retrieval-Augmented Generation (RAG).

## Overview

The AI-Powered PDF Research Assistant simplifies the process of understanding and researching lengthy PDF documents. It extracts text, divides it into smaller chunks, generates embeddings, and stores them in a vector database.

When a user asks a question, the application retrieves relevant information from the uploaded document and uses a Large Language Model (LLM) to generate an answer based on the retrieved context.

## Key Features

- **PDF Upload:** Upload PDF documents through a FastAPI endpoint.
- **PDF Text Extraction:** Extract text and page numbers using PyMuPDF.
- **Text Chunking:** Split extracted content into manageable chunks using LangChain.
- **Embeddings Generation:** Generate semantic embeddings using Hugging Face Sentence Transformers.
- **Vector Storage:** Store document chunks and embeddings in ChromaDB.
- **Semantic Search:** Retrieve relevant chunks based on user questions.
- **AI-Powered Answers:** Generate context-aware responses using Ollama and Llama 3.2.
- **Source References:** Return page numbers used to generate answers.
- **Input Validation:** Validate uploaded PDFs and user questions.
- **Error Handling:** Handle invalid documents and storage failures.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| FastAPI | REST API development |
| LangChain | Text splitting |
| PyMuPDF | PDF text extraction |
| Hugging Face | Embedding generation |
| Sentence Transformers | Semantic embeddings |
| ChromaDB | Vector database |
| Ollama | Local LLM execution |
| Llama 3.2 (3B) | Answer generation |
| Git & GitHub | Version control |

## System Architecture

```text
       User
        |
        v
    PDF Upload
        |
        v
   FastAPI Backend
        |
        v
   PDF Text Extraction
        |
        v
     Text Chunking
        |
        v
  Embedding Generation
        |
        v
      ChromaDB
   (Vector Storage)
        |
        |
    User Question
        |
        v
  Query Embedding
        |
        v
 Semantic Retrieval
        |
        v
 Relevant Text Chunks
        |
        v
  Ollama (Llama 3.2)
        |
        v
   Generated Answer
        |
        v
 Answer + Source Pages
```

## Project Structure

```text
AI-PDF-Research-Assistant/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── document.py
│   │   │
│   │   ├── services/
│   │   │   ├── pdf_service.py
│   │   │   ├── chunking_service.py
│   │   │   ├── embedding_service.py
│   │   │   ├── vector_store.py
│   │   │   ├── llm_service.py
│   │   │   └── rag_service.py
│   │   │
│   │   ├── __init__.py
│   │   └── main.py
│   │
│   ├── tests/
│   └── requirements.txt
│
├── .gitignore
└── README.md
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/shashank618/AI-PDF-Research-Assistant.git
```

### 2. Navigate to the Project

```bash
cd AI-PDF-Research-Assistant
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r backend/requirements.txt
```

### 5. Install and Run Ollama

Download Ollama from:

https://ollama.com/

Pull the Llama 3.2 model:

```bash
oll