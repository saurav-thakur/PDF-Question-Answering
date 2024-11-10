from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings

from pdf_question_answering.constants import *
from pdf_question_answering.logger import logging
from pdf_question_answering.exception import PDFQAException


class PDF:
    def read_pdf_file(self, data):
        loader = PyPDFLoader(data)
        documents = loader.load()
        return documents

    def split_text(self, extracted_data):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
        )
        text_chunks = text_splitter.split_documents(extracted_data)
        return text_chunks
