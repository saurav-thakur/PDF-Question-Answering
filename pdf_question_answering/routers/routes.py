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
)
from fastapi.responses import HTMLResponse
from typing import List
from pdf_question_answering.logger import logging
from pdf_question_answering.exception import PDFQAException
from pdf_question_answering.db.schemas import Question
from main import main

pdf_router = APIRouter()


# # Dependency to get embeddings from the app's state
# def get_embeddings(request: Request):
#     return request.app.state.embeddings
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
async def uploadfile(files: list[UploadFile]):
    try:
        for file in files:
            file_path = f"./pdf_data/{file.filename}"
            filepath = Path(file_path)
            print(filepath)
            filedir, filename = os.path.split(filepath)

            if filedir != "":
                os.makedirs(filedir, exist_ok=True)
                logging.info(f"Creating directory: {filedir} for the file {filename}")

            with open(file_path, "wb") as f:
                f.write(file.file.read())

    except Exception as e:
        raise PDFQAException(e, sys)


@pdf_router.post("/ask-question")
async def ask_question(question: Question):
    return question.question


@pdf_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        answer = main(data_folder="./pdf_data", question=data)
        await websocket.send_text(f"Answer: {answer}")
        # await websocket.send_text(f"Message text was: {data}")
