from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
import os
from dotenv import load_dotenv
from langchain_pinecone import PineconeVectorStore

from pdf_question_answering.constants import *
from pdf_question_answering.logger import logging
from pdf_question_answering.exception import PDFQAException

load_dotenv()


class VectorDB:
    def __init__(self):
        try:
            self.index_name = os.environ.get("PINECONE_INDEX_NAME")
            self.pinecone_api_key = os.environ.get("PINECONE_API_KEY")
            self.pinecone_dimension = DIMENSION
            self.pinecone_metric = METRIC
            self.pinecone_cloud = os.environ.get("PINECONE_CLOUD")
            self.pinecone_region = os.environ.get("PINECONE_REGION")
            if not self.index_name or not self.pinecone_api_key:
                raise PDFQAException(
                    "Missing necessary environment variables for Pinecone configuration."
                )
            logging.info("VectorDB initialized with index name: %s", self.index_name)
        except Exception as e:
            logging.error("Failed to initialize VectorDB: %s", e)
            raise PDFQAException(e)

    def create_vector_database(self):
        try:
            pc = Pinecone(api_key=self.pinecone_api_key)
            pc.create_index(
                name=self.index_name,
                dimension=self.pinecone_dimension,
                metric=self.pinecone_dimension,
                spec=ServerlessSpec(
                    cloud=self.pinecone_cloud, region=self.pinecone_region
                ),
            )
            logging.info("Vector database created with index name: %s", self.index_name)
        except Exception as e:
            logging.error("Failed to create vector database: %s", e)
            raise PDFQAException(e)

    def insert_data_into_vector_db(self, text_chunks, embeddings):
        try:
            docsearch = PineconeVectorStore.from_documents(
                documents=text_chunks,
                index_name=self.index_name,
                embedding=embeddings,
            )
            logging.info(
                "Data inserted into vector database for index: %s", self.index_name
            )
        except Exception as e:
            logging.error("Failed to insert data into vector database: %s", e)
            raise PDFQAException(e)

    def delete_index(self):
        try:
            pc = Pinecone(api_key=self.pinecone_api_key)
            pc.delete_index(self.index_name)
            logging.info("Deleted vector database index: %s", self.index_name)
        except Exception as e:
            logging.error("Failed to delete vector database index: %s", e)
            raise PDFQAException(e)

    def load_existing_index(self, embeddings):
        try:
            docsearch = PineconeVectorStore.from_existing_index(
                index_name=self.index_name,
                embedding=embeddings,
            )
            logging.info("Loaded existing vector database index: %s", self.index_name)
            return docsearch
        except Exception as e:
            logging.error("Failed to load existing vector database index: %s", e)
            raise PDFQAException(e)
