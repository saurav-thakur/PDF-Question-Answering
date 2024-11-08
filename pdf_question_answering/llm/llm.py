import os

# from langchain_openai import OpenAI
from langchain_groq import ChatGroq
from dotenv import load_dotenv

from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

from pdf_question_answering.constants import SYSTEM_PROMPT, LLM_MODEL
from pdf_question_answering.logger import logging
from pdf_question_answering.exception import PDFQAException

load_dotenv()


class LLMs:
    def __init__(self, retriver) -> None:
        self.system_prompt = SYSTEM_PROMPT
        self.llm_model = ChatGroq(
            groq_api_key=os.environ.get("GROQ_API_KEY"), model=LLM_MODEL
        )
        self.prompt = ChatPromptTemplate.from_messages(
            [("system", self.system_prompt), ("human", "{input}")]
        )
        self.retriver = retriver

    def generate_answer(self, question):
        question_answer_chain = create_stuff_documents_chain(
            self.llm_model, self.prompt
        )
        rag_chain = create_retrieval_chain(self.retriver, question_answer_chain)
        response = rag_chain.invoke({"input": f"{question}"})
        return response["answer"]
