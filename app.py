from fastapi import FastAPI
import uvicorn

from contextlib import asynccontextmanager
from pdf_question_answering.llm.embeddings import Embeddings
from pdf_question_answering.routers.routes import pdf_router


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

app.include_router(pdf_router, prefix=f"/api/{version}/pdf-qa")

if __name__ == "__main__":
    uvicorn.run("app:app", host="localhost", reload=True)
