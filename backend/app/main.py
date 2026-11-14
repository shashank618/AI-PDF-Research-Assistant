from fastapi import FastAPI
from app.api.document import router as document_router

app = FastAPI(
    
     title="AI PDF Research Assistant",
     description="An AI-powered application to research and interact with PDF documents.",
     version="1.0.0"


)
app.include_router(document_router)

