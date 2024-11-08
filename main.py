import sys
from pdf_question_answering.llm.llm_service import (
    PDFService,
    VectorDBService,
    PDFQuestionAnsweringService,
)
from pdf_question_answering.utils.read_pdf import PDF
from pdf_question_answering.llm.embeddings import Embeddings
from pdf_question_answering.llm.vector_db import VectorDB
from pdf_question_answering.llm.llm import LLMs
from pdf_question_answering.logger import logging
from pdf_question_answering.exception import PDFQAException


def main(data_folder, question):
    try:
        logging.info("Initializing PDF, embedding, vector DB, and LLM services.")
        pdf_service = PDFService(pdf=PDF())
        embedding_service = Embeddings()
        vector_db_service = VectorDBService(vector_db=VectorDB())
        llm_service = LLMs()

        qa_service = PDFQuestionAnsweringService(
            pdf_service=pdf_service,
            embedding_service=embedding_service,
            vector_db_service=vector_db_service,
            llm_service=llm_service,
        )
        logging.info("All services initialized successfully.")
        answer = qa_service.answer_question_from_pdf(
            data_folder=data_folder, question=question
        )
        logging.info("Question answered successfully.")
        return answer

    except Exception as e:
        raise PDFQAException(e, sys)


if __name__ == "__main__":
    data = "./pdf_data"
    question = "what is adversarial machine learning?"
    answer = main(data_folder=data, question=question)
    print(answer)
