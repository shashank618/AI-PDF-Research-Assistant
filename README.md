# 📚 AI-Powered PDF Research Assistant

An AI-powered application that enables users to upload PDF documents, ask questions, and receive context-aware answers using **Retrieval-Augmented Generation (RAG)**.

Built with FastAPI, LangChain, Hugging Face embeddings, ChromaDB, Ollama and Streamlit, this application makes researching lengthy documents easier through semantic search and AI-powered question answering.

---

## 🚀 Project Overview

The AI-Powered PDF Research Assistant is designed to simplify document research and information retrieval.

Users can register, log in, upload PDF documents, and ask questions about their uploaded content.

The application processes documents through a RAG pipeline:

1. Extracts text and page numbers from PDF documents.
2. Splits extracted text into smaller chunks.
3. Generates semantic embeddings using Hugging Face Sentence Transformers.
4. Stores embeddings and document metadata in ChromaDB.
5. Converts user questions into embeddings.
6. Retrieves relevant document chunks using semantic similarity search.
7. Passes retrieved context to a local Large Language Model (LLM).
8. Generates answers based on the retrieved document content.
9. Returns answers along with source page references.

The application also implements JWT-based authentication and document ownership verification to protect user documents.

---

## ✨ Key Features

### 1. PDF Processing
- Upload PDF documents through the Streamlit interface.
- Extract text and page numbers using PyMuPDF.
- Validate PDF files and file size.
- Split extracted text into manageable chunks.

### 2. Retrieval-Augmented Generation (RAG)
- Generate semantic embeddings using Hugging Face.
- Store document embeddings in ChromaDB.
- Perform semantic similarity search.
- Retrieve relevant document chunks.
- Generate context-aware answers using Ollama and Llama 3.2.

### 3. AI-Powered Question Answering
- Ask natural-language questions about uploaded documents.
- Retrieve relevant information from document content.
- Generate answers using retrieved context.
- Display source page references.
- Handle questions when relevant information is unavailable in the document.

### 4. Authentication and Security
- User registration and login.
- Password hashing using Argon2.
- JWT-based authentication.
- Protected document endpoints.
- Document ownership verification.
- SQLite database for user and document records.

### 5. User Interface
- Interactive Streamlit frontend.
- User registration and login interface.
- PDF upload functionality.
- AI-powered question-answering interface.
- Display of generated answers and source pages.
- Custom Ivory, Pale Sage, Muted Olive and Deep Walnut theme.

### 6. Validation and Error Handling
- PDF extension validation.
- File size validation (10 MB maximum).
- PDF file signature validation.
- Question input validation.
- HTTP exception handling.
- Invalid document and authentication handling.

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| FastAPI | REST API development |
| Streamlit | Frontend development |
| LangChain | Text splitting |
| PyMuPDF | PDF text extraction |
| Hugging Face | Embedding generation |
| Sentence Transformers | Semantic embeddings |
| ChromaDB | Vector database |
| Ollama | Local LLM execution |
| Llama 3.2 (3B) | AI answer generation |
| SQLite | User and document database |
| PyJWT | JWT authentication |
| Argon2 | Password hashing |
| Pydantic | Data validation |
| Git & GitHub | Version control |

---

## 🏗️ System Architecture

### Document Upload and Processing Flow

```text
              User
               |
               v
         Streamlit UI
               |
               v
          PDF Upload
               |
               v
        FastAPI Backend
               |
               v
       PDF Text Extraction
           (PyMuPDF)
               |
               v
          Text Chunking
          (LangChain)
               |
               v
       Embedding Generation
       (Hugging Face Model)
               |
               v
           ChromaDB
        (Vector Storage)
```

### Question Answering Flow

```text
          User Question
               |
               v
        FastAPI Backend
               |
               v
        Query Embedding
               |
               v
        Semantic Search
           (ChromaDB)
               |
               v
       Relevant Text Chunks
               |
               v
       Context Construction
               |
               v
       Ollama (Llama 3.2)
               |
               v
        Generated Answer
               |
               v
       Answer + Source Pages
               |
               v
          Streamlit UI
```

### Authentication Flow

```text
             User
              |
              v
        Register / Login
              |
              v
        FastAPI Backend
              |
              v
       SQLite User Database
              |
              v
       Password Verification
           (Argon2)
              |
              v
        JWT Token Generation
              |
              v
        Authenticated User
              |
              v
       Protected API Endpoints
              |
              v
       Document Ownership Check
```

---

## 📁 Project Structure

```text
AI-PDF-research-Assitant/
│
├── .streamlit/
│   └── config.toml
│
├── backend/
│   │
│   ├── app/
│   │   ├── api/
│   │   │   ├── auth.py
│   │   │   └── document.py
│   │   │
│   │   ├── services/
│   │   │   ├── pdf_service.py
│   │   │   ├── chunking_service.py
│   │   │   ├── embedding_service.py
│   │   │   ├── vector_store.py
│   │   │   ├── llm_service.py
│   │   │   ├── rag_service.py
│   │   │   ├── security.py
│   │   │   ├── auth_service.py
│   │   │   ├── jwt_service.py
│   │   │   ├── auth_dependency.py
│   │   │   └── document_service.py
│   │   │
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── database.py
│   │   └── schemas.py
│   │
│   ├── tests/
│   │   ├── test_chunking.py
│   │   ├── test_vector_store.py
│   │   ├── test_llm.py
│   │   ├── test_rag.py
│   │   └── test_security.py
│   │
│   └── requirements.txt
│
├── frontend/
│   └── app.py
│
├── .env
├── .gitignore
└── README.md
```

**Note:** Runtime files such as the SQLite database, uploaded PDFs, ChromaDB storage and virtual environment are excluded from Git.

---

## ⚙️ Installation and Setup

### Prerequisites

Install the following before running the application:

- Python 3.10 or later (a compatible Python environment).
- Git.
- Ollama.
- Llama 3.2 model.

### 1. Clone the Repository

```bash
git clone https://github.com/shashank618/AI-PDF-Research-Assistant.git
```

### 2. Navigate to the Project Directory

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

### 4. Install Backend Dependencies

```bash
python -m pip install -r backend/requirements.txt
```

Install frontend dependencies:

```bash
python -m pip install streamlit requests
```

### 5. Install and Configure Ollama

Download Ollama:

https://ollama.com/

Pull the Llama 3.2 model:

```bash
ollama pull llama3.2:3b
```

Make sure Ollama is running locally before using the question-answering functionality.

### 6. Configure Environment Variables

Create a `.env` file in the project root.

Add the following configuration:

```env
JWT_SECRET_KEY=your_secure_random_secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Generate your own strong secret key. Never upload your `.env` file to GitHub.

### 7. Run the FastAPI Backend

Open a terminal and navigate to the backend directory:

```powershell
cd backend
```

Start the FastAPI server:

```powershell
python -m uvicorn app.main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

### 8. Run the Streamlit Frontend

Open a second terminal in the project root and activate the virtual environment if necessary.

Run:

```powershell
python -m streamlit run frontend/app.py
```

Frontend URL:

```text
http://localhost:8501
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Authenticate user and generate JWT |
| POST | `/documents/upload` | Upload and process a PDF |
| POST | `/documents/{document_id}/ask` | Ask questions about an uploaded PDF |

Protected document endpoints require a valid JWT bearer token.

---

## 🔐 Security Implementation

The application includes several authentication and security mechanisms:

- **Password Hashing:** Argon2 is used to hash passwords before storing them.
- **JWT Authentication:** JSON Web Tokens are generated after successful login.
- **Protected Routes:** Authentication dependencies protect document endpoints.
- **Document Ownership:** Users can access only documents associated with their account.
- **Input Validation:** Pydantic validates user inputs and question requests.
- **Environment Variables:** Sensitive JWT configuration is maintained outside the source code.

---

## 🧪 Testing

The project includes test modules for important application components:

- Text chunking.
- Vector storage.
- LLM integration.
- RAG functionality.
- Password hashing and verification.

The application has also been manually tested for:

- User registration and login.
- JWT-protected API access.
- PDF upload and processing.
- Semantic question answering.
- Source page references.
- Invalid PDF handling.
- File size validation.
- Document ownership verification.

---

## 🎯 Learning Outcomes

Through this project, I gained practical experience with:

- Building REST APIs using FastAPI.
- Implementing Retrieval-Augmented Generation.
- Understanding embeddings and vector databases.
- Working with Hugging Face Sentence Transformers.
- Integrating local LLMs using Ollama.
- Implementing JWT authentication and password hashing.
- Managing relational and vector databases.
- Building interactive applications using Streamlit.
- Organizing backend code using modular services and API routers.
- Using Git and GitHub for version control.

---

## 🔮 Future Improvements

Potential enhancements include:

- Support for multiple document formats.
- Document management and deletion interface.
- Conversation history.
- Streaming AI responses.
- Improved automated test coverage.
- Docker-based deployment.
- Cloud deployment and production monitoring.

---

## 👨‍💻 Author

**Shashank Choudhary**

Computer Science Graduate | Python Backend & Generative AI Enthusiast

**GitHub:** https://github.com/shashank618

---

## ⭐ Acknowledgements

- FastAPI
- LangChain
- Hugging Face
- ChromaDB
- Ollama
- Streamlit
- PyMuPDF

If you find this project useful, feel free to explore the repository and give it a star!
