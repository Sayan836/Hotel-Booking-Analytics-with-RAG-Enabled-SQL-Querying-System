from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()



class Retriever:
    def __init__(self, docs, persist_directory, api_key=None, use_gemini_embeddings=True):
        """
        Initialize the retriever with documents and a vector store.
        
        Args:
            docs (list): List of document objects.
            persist_directory (str): Directory for storing Chroma database.
            use_gemini_embeddings (bool): Whether to use Gemini embeddings instead of HuggingFace.
        """
        self.docs = docs
        # Use Gemini embeddings if enabled, else default to HuggingFace
        if use_gemini_embeddings:
            self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)
        else:
            self.embeddings = HuggingFaceEmbeddings()
        # Initialize Chroma vector store
        self.vectorstore = Chroma.from_documents(
            documents=docs,
            embedding=self.embeddings,
            persist_directory=persist_directory
        )

    def get_retriever(self, search_type="similarity", k=3):
        """
        Returns a retriever that searches for similar documents.

        Args:
            search_type (str): The type of search (default: "similarity").
            k (int): Number of relevant documents to retrieve (default: 3).

        Returns:
            A retriever object configured with the vectorstore.
        """
        return self.vectorstore.as_retriever(search_type=search_type, search_kwargs={"k": k})
