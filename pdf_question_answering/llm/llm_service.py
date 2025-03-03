import sys
import logging
from pdf_question_answering.llm.llm import LLMs
from pdf_question_answering.utils.read_pdf import PDF
from pdf_question_answering.llm.embeddings import Embeddings
from pdf_question_answering.llm.vector_db import VectorDB
from pdf_question_answering.exception import PDFQAException
from pdf_question_answering.logger import logging
from pdf_question_answering.constants import *


# PDF Service
class PDFService:
    def __init__(self, pdf: PDF):
        self.pdf = pdf

    def extract_text_chunks(self, pdf_data_folder):
        try:
            extracted_data = self.pdf.read_pdf_file(pdf_data_folder)
            text_chunks = self.pdf.split_text(extracted_data=extracted_data)
            logging.info("Extracted text chunks from PDF")
            return text_chunks
        except Exception as e:
            logging.error(f"Failed to extract text chunks: {e}")
            raise PDFQAException(e, sys)


# Vector DB Service
class VectorDBService:
    def __init__(self, vector_db: VectorDB):
        self.vector_db = vector_db

    def setup_vector_db(self, text_chunks, embeddings):
        try:
            # self.vector_db.create_vector_database()
            # self.vector_db.insert_data_into_vector_db(text_chunks, embeddings)
            docsearch = self.vector_db.load_existing_index(embeddings=embeddings)
            logging.info("Vector database created and populated")
            return docsearch
        except Exception as e:
            logging.error(f"Failed to set up vector DB: {e}")
            raise PDFQAException(e, sys)


# Main Service Coordinator
class PDFQuestionAnsweringService:
    def __init__(
        self,
        pdf_service: PDFService,
        embedding_service: Embeddings,
        vector_db_service: VectorDBService,
        llm_service: LLMs,
    ):
        self.pdf_service = pdf_service
        self.embedding_service = embedding_service
        self.vector_db_service = vector_db_service
        self.llm_service = llm_service

    def answer_question_from_pdf(self, data_folder, question):
        try:
            text_chunks = self.pdf_service.extract_text_chunks(data_folder)
            embeddings = self.embedding_service.download_hugging_face_embeddings()
            docsearch = self.vector_db_service.setup_vector_db(text_chunks, embeddings)
            answer = self.llm_service.generate_answer(docsearch, question)
            logging.info("Question answered successfully")
            return answer
        except Exception as e:
            logging.info(f"Failed to answer question: {e}")
            raise PDFQAException(e, sys)
