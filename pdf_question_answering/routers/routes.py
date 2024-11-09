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

pdf_router = APIRouter()

# Create tables if they do not exist
models.Base.metadata.create_all(bind=engine)

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
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        answer = main(data_folder="./pdf_data", question=data)
        await websocket.send_text(f"Answer: {answer}")
