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
        self.index_name = INDEX_NAME
        self.pinecone_api_key = os.environ.get("PINECONE_API_KEY")

    def create_vector_database(self):
        pc = Pinecone(api_key=self.pinecone_api_key)
        pc.create_index(
            name=self.index_name,
            dimension=DIMENSION,
            metric=METRIC,
            spec=ServerlessSpec(cloud=CLOUD, region=REGION),
        )

    def insert_data_into_vector_db(self, text_chunks, embeddings):
        docsearch = PineconeVectorStore.from_documents(
            documents=text_chunks,
            index_name=self.index_name,
            embedding=embeddings,
        )

    def delete_index(self):
        pc = Pinecone(api_key=self.pinecone_api_key)
        pc.delete_index(self.index_name)

    def load_existing_index(self, embeddings):
        docsearch = PineconeVectorStore.from_existing_index(
            index_name=self.index_name,
            embedding=embeddings,
        )
        return docsearch
