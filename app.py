from fastapi import FastAPI
import uvicorn
from pdf_question_answering.routers.routes import pdf_router


version = "v1"
app = FastAPI()
app.include_router(pdf_router, prefix=f"/api/{version}/pdf-qa")

if __name__ == "__main__":
    uvicorn.run("app:app", host="localhost", reload=True)
