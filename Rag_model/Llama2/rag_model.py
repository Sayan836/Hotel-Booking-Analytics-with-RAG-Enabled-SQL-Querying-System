from langchain_huggingface import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from transformers import AutoConfig, AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, pipeline
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel
from langchain_core.documents import Document
from langchain.chains import create_retrieval_chain # type: ignore
from langchain.chains.combine_documents import create_stuff_documents_chain
from Hotel_Booking_Analytics.Rag_model.Llama2.LLM import RAGModel
from dotenv import load_dotenv
import re
import os
import fitz



# Define the Retriever Class
class Retriever:
    def __init__(self, docs, persist_directory):
        self.embeddings = HuggingFaceEmbeddings()
        
        self.vectorstore = Chroma.from_documents(
            documents=docs,
            embedding=self.embeddings,
            persist_directory=persist_directory,
        )

    def get_retriever(self, search_type="similarity", k=10):
        return self.vectorstore.as_retriever(search_type=search_type, search_kwargs={"k": k})


# Function to Define Prompt Template
def Prompt_Template():
    prompt_template = """
    <|system|>
    You are an advanced content analysis engine specializing in extracting insights and answering queries based on document content and structured data.

    Your task is to provide clear, concise, and relevant responses using the available information. If SQL query results are provided, incorporate them into your answer. If SQL results are missing or empty, rely solely on the extracted document context.

    Context for reference:
    - Extracted PDF Content: {context}
    - SQL Query Results: {sql_results}

    Ensure responses are **direct, well-structured, and optimized for clarity**.

    </s>
    <|user|>
    {input}
    </s>
    <|assistant|>
    """

    prompt = PromptTemplate(
        input_variables=["context", "sql_results", "input"],
        template=prompt_template,
    )
    return prompt


def load_pdf_data(file_path):
    documents = []
    with fitz.open(file_path) as pdf:
        for page_num in range(len(pdf)):
            text = pdf[page_num].get_text("text")
            if text.strip():  # Ignore empty pages
                documents.append(Document(page_content=text, metadata={"page": page_num + 1}))

    return documents


# Function to Initialize the RAG Chain
def initialize_rag_chain(model_id, auth_token, data_path, persist_directory):
    # Load PDF data
    documents = load_pdf_data(data_path)

    # Initialize retriever with SQL results included
    retriever_instance = Retriever(docs=documents, persist_directory=persist_directory)
    retriever = retriever_instance.get_retriever()

    # Initialize LLM
    model_instance = RAGModel(model_id=model_id, auth_token=auth_token)
    llm = model_instance.initialize_pipeline()

    prompt_template = Prompt_Template()
    
    qa_chain = create_stuff_documents_chain(llm=llm, prompt=prompt_template)
    rag_chain = create_retrieval_chain(retriever, qa_chain)
    
    return rag_chain



