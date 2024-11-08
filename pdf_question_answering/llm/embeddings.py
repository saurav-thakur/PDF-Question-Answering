from langchain.embeddings import HuggingFaceEmbeddings

from pdf_question_answering.constants import *
from pdf_question_answering.logger import logging
from pdf_question_answering.exception import PDFQAException


class Embeddings:
    def __init__(self):
        self.embedding_model_name = EMBEDDING_MODEL_NAME

    def download_hugging_face_embeddings(self):
        embeddings = HuggingFaceEmbeddings(model_name=self.embedding_model_name)
        return embeddings
