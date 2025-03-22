import os
import sqlite3
from Rag_model.retriever import Retriever
from Rag_model.prompt import Prompt_Template
from Rag_model import utils
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv

load_dotenv()

 # Google Gemini API Key
# GEMINI_API_KEY = os.getenv("GEMINI_API")


class RAGSystem:
    def __init__(self, pdf_path, api_key):
        self.llm = ChatGoogleGenerativeAI(model="models/gemini-2.0-flash", google_api_key=api_key)
        self.retriever = None
        self.data= {}
        self.pdf_path= pdf_path
        self.api_key= api_key
        self.initialize_system()

    def initialize_system(self):
        """Initialize the retriever and data variables."""
        if "retriever_initialized" not in self.data:
            docs= utils.extract_pdf_to_documents(self.pdf_path)
            chunks= utils.split_text(docs)

            # Load & process documents
            persist_directory = os.getenv("PERSIST_DIRECTORY")
            os.makedirs(persist_directory, exist_ok=True)

            # Initialize retriever
            retriever_obj = Retriever(chunks, persist_directory, self.api_key)
            self.data["retriever"] = retriever_obj.get_retriever()

            self.data["chat_history"] = []
            self.data["conversation_context"] = ""
            self.data["retriever_initialized"] = True

    def get_rag_chain(self):
        """Return the RAG processing chain."""
        prompt_template = Prompt_Template()

        # Retrieve documents from data retriever
        retriever = self.data.get("retriever", None)

        if retriever is None:
            raise ValueError("Retriever not initialized. Call initialize_system() first.")

        # RAG Chain
        rag_chain = {
            "context": retriever,
            "sql_results": RunnablePassthrough(),
            "question": RunnablePassthrough()
        } | prompt_template | self.llm
        return rag_chain
