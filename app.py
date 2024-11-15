import os
from fastapi import FastAPI
import uvicorn

from contextlib import asynccontextmanager
from pdf_question_answering.llm.embeddings import Embeddings
from pdf_question_answering.routers.routes import pdf_router

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

limiter = Limiter(key_func=get_remote_address, default_limits=["2/minute"])


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load embeddings once at application startup
    embeddings = Embeddings().download_hugging_face_embeddings()
    # Add embeddings to app state for easy access
    app.state.embeddings = embeddings

    # Initialize an empty dictionary in the app state for docsearch storage
    app.state.store_data = {}
    yield
    # cleanup logic if needed


version = "v1"
app = FastAPI(
    title="PDF Question Answering System",
    description="A REST API for uploaded pdf to ask question and recieve answer",
    version=version,
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # can alter with time
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Add rate limit exceeded handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(pdf_router, prefix=f"/api/{version}/pdf-qa")

if __name__ == "__main__":
    host = os.environ.get("HOST")
    uvicorn.run(
        "app:app", host=host, reload=(True if host == "localhost" else False), port=8000
    )
