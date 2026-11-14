from app.api.auth import router as auth_router
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.document import router as document_router
from app.database import create_users_table


@asynccontextmanager
async def lifespan(app: FastAPI):

    # Initialize the users database table
    create_users_table()

    yield


app = FastAPI(
    title="AI PDF Research Assistant",
    description="An AI-powered application to research and interact with PDF documents.",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(document_router)
app.include_router(auth_router)
