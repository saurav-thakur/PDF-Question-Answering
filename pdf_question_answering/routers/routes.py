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


# # Dependency to get embeddings from the app's state
# def get_embeddings(request: Request):
#     return request.app.state.embeddings


pdf_router = APIRouter()

# Create tables if they do not exist
models.Base.metadata.create_all(bind=engine)

# embeddings = None


# @pdf_router.on_event("startup")
# async def startup_event():
#     embeddings = Embeddings().download_hugging_face_embeddings()
embeddings = Embeddings().download_hugging_face_embeddings()

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
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@pdf_router.get("/")
async def home():
    return {"message": "Hello World"}


@pdf_router.get("/chat")
async def chat_with_pdf():
    return HTMLResponse(html)


@pdf_router.post("/upload-pdf")
async def uploadfile(files: List[UploadFile], db: db_dependency):
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

    except Exception as e:
        raise PDFQAException(e, sys)


@pdf_router.post("/ask-question")
async def ask_question(question: Question):
    return {"question": question.question}


@pdf_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, db: db_dependency):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        # Get embeddings explicitly from request
        # embeddings = embeddings
        # em

        logging.info(f"Uploaded File")
        uploaded_file = (
            db.query(models.PDFData).order_by(models.PDFData.upload_date.desc()).first()
        )
        logging.info(f"Uploaded File: {uploaded_file}")

        if uploaded_file:
            file_path = f"./pdf_data/{uploaded_file.filename}"
            logging.info(f"Uploaded filename is : {uploaded_file.filename}")
            # answer = main(data_folder=file_path, question=data)
            logging.info(f"Loading PDF")
            pdf_loader = PDF()
            extracted_data = pdf_loader.read_pdf_file(data=file_path)
            text_chunks = pdf_loader.split_text(extracted_data)
            logging.info(f"PDF loaded and splitted")

            vector_db = VectorDB()
            # vector_db.create_vector_database()
            # vector_db.insert_data_into_vector_db(
            #     text_chunks=text_chunks, embeddings=embeddings
            # )
            docsearch = vector_db.load_existing_index(embeddings=embeddings)
            logging.info(f"Vector loaded")

            logging.info(f"LLMs Initialized")
            llm = LLMs()
            answer = llm.generate_answer(docsearch=docsearch, question=data)
            logging.info(f"Answer Generated")

            await websocket.send_text(f"Answer: {answer}")
