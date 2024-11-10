import os, sys
from pathlib import Path
from fastapi import (
    FastAPI,
    APIRouter,
    status,
    UploadFile,
    Request,
    WebSocket,
    WebSocketDisconnect,
    Depends,
    HTTPException,
)
from fastapi.responses import HTMLResponse
from typing import List, Annotated
from pdf_question_answering.logger import logging
from pdf_question_answering.exception import PDFQAException
from pdf_question_answering.db.schemas import Question
from main import main
from pdf_question_answering.db import models
from sqlalchemy.orm import Session
from pdf_question_answering.db.database import engine, SessionLocal
from pdf_question_answering.db import models
from pdf_question_answering.db.config import db_dependency
from datetime import datetime

from pdf_question_answering.logger import logging
from pdf_question_answering.utils.read_pdf import PDF
from pdf_question_answering.llm.vector_db import VectorDB
from pdf_question_answering.llm.llm import LLMs
from pdf_question_answering.llm.embeddings import Embeddings

from fastapi import Request, Depends

from slowapi import Limiter
from slowapi.util import get_remote_address

# # Dependency to get embeddings from the app's state
# def get_embeddings(request: Request):
#     return request.app.state.embeddings


pdf_router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

# Create tables if they do not exist
models.Base.metadata.create_all(bind=engine)

# embeddings = None


# @pdf_router.on_event("startup")
# async def startup_event():
#     embeddings = Embeddings().download_hugging_face_embeddings()
embeddings = Embeddings().download_hugging_face_embeddings()
vector_db = VectorDB()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>PDF Question Answering Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("http://localhost:8000/api/v1/pdf-qa/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            // Send the user's question and display it in the chat
            function sendMessage(event) {
                var input = document.getElementById("messageText");
                var messages = document.getElementById('messages');

                // Add user question to the chat
                var question = document.createElement('li');
                question.className = "question";
                question.textContent = "Question: " + input.value;
                messages.appendChild(question);

                // Send the question via WebSocket
                ws.send(input.value);

                // Clear the input field
                input.value = '';
                event.preventDefault();
            }
        </script>
    </body>
</html>
"""


@pdf_router.get("/")
@limiter.limit("2/minute")
async def home(request: Request):
    return {"message": "Hello World"}


@pdf_router.get("/chat")
async def chat_with_pdf():
    return HTMLResponse(html)


@pdf_router.post("/upload-pdf")
@limiter.limit("2/minute")
async def uploadfile(request: Request, files: List[UploadFile], db: db_dependency):
    try:
        for file in files:
            file_path = f"./pdf_data/{file.filename}"
            filepath = Path(file_path)
            filedir, filename = os.path.split(filepath)

            if filedir:
                os.makedirs(filedir, exist_ok=True)
                logging.info(f"Creating directory: {filedir} for the file {filename}")

            with open(file_path, "wb") as f:
                f.write(file.file.read())

            # Store in database
            db_pdf_data = models.PDFData(
                filename=file.filename, upload_date=datetime.now().isoformat()
            )
            db.add(db_pdf_data)
            db.commit()
            db.refresh(db_pdf_data)
            db.commit()

            # Process the uploaded file
            pdf_loader = PDF()
            extracted_data = pdf_loader.read_pdf_file(data=file_path)
            text_chunks = pdf_loader.split_text(extracted_data)

            vector_db.create_vector_database()
            vector_db.insert_data_into_vector_db(
                text_chunks=text_chunks, embeddings=embeddings
            )
            docsearch = vector_db.load_existing_index(embeddings=embeddings)

            # Store text_chunks in the app state for this specific file
            request.app.state.store_data["docsearch"] = docsearch

            logging.info(f"PDF loaded and split into chunks for {file.filename}")

    except Exception as e:
        raise PDFQAException(e, sys)


@pdf_router.post("/ask-question")
async def ask_question(question: Question):
    return {"question": question.question}


@pdf_router.delete("/delete-pinecone-index")
async def delete_pinecone_index():

    try:
        vector_db.delete_index()
        return {"message": "index deleted"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No Index Found"
        )


@pdf_router.websocket("/ws")
@limiter.limit("2/minute")
async def websocket_endpoint(request: Request, websocket: WebSocket, db: db_dependency):
    docsearch = websocket.app.state.store_data["docsearch"]
    llm = LLMs()
    logging.info(f"PDF loaded and splitted")
    logging.info(f"Vector loaded")
    logging.info(f"LLMs Initialized")
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_text()

            answer = llm.generate_answer(docsearch=docsearch, question=data)
            logging.info(f"Answer Generated")

            await websocket.send_text(f"Answer: {answer}")
    except WebSocketDisconnect:
        logging.info("WebSocket disconnected. Performing cleanup...")

    finally:
        # Delete the index when the WebSocket connection is closed

        try:
            vector_db.delete_index()
        except Exception as e:
            logging.info(f"No Index to delete!!")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No Index Found"
            )
