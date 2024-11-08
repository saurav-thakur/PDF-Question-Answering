import os, sys
from pathlib import Path
from fastapi import FastAPI, APIRouter, status, UploadFile
from typing import List
from pdf_question_answering.logger import logging
from pdf_question_answering.exception import PDFQAException

pdf_router = APIRouter()


@pdf_router.get("/")
async def home():
    return {"message": "Hello World"}


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
