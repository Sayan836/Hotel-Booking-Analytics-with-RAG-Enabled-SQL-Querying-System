from flask import Flask, jsonify, render_template, request
from Analytics.Plot_Analytics import PlotAnalytics  # Assuming this contains the modified class
from Analytics.fetch_data import FetchData
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from Rag_model.sql_agent import SQL_Agent
#from Hotel_Booking_Analytics.Rag_model.Llama2.LLM import model
from Rag_model.Gemini_RagSystem import RAGSystem
from langchain_core.runnables import RunnablePassthrough
from Rag_model import utils
import pandas as pd
from Rag_model.sql_agent import SQL_Agent
import os
import matplotlib
from flask_cors import CORS # type: ignore

matplotlib.use('Agg')  # Use non-interactive backend

app = Flask(__name__)
CORS(app)

load_dotenv()

session={"chat_history":[]}

model_id = os.getenv("MODEL_ID") # Change as needed
#model_id2= "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
auth_token = os.getenv("HUGGINGFACE_AUTH_TOKEN")  # Load from environment for security
pdf_path = os.getenv("PDF_PATH")
persist_directory = os.getenv("PERSIST_DIRECTORY")
GEMINI_API_KEY = os.getenv("GEMINI_API")
# Initialize SQL Agent and fetch query results
SQL_instance = SQL_Agent(os.getenv("CSV_PATH"), "database.sqlite",os.getenv("GEMINI_API") )
session["SQL_Agent"]= SQL_instance
print("SQL Agent Initilized sucessfully....")

 #Initialize llama RAG Chain
# rag_chain = initialize_rag_chain(model_id, auth_token, pdf_path, persist_directory)
# session["RAG_Chain"]= rag_chain
# print("Rag Chain initialized succesfully...")

model= RAGSystem(pdf_path, GEMINI_API_KEY)
session["rag_chain"]= model.get_rag_chain()

@app.route("/")
def index():
  global session
  return render_template("index.html")

@app.route('/result_analytics', methods=['POST','GET'])
def result_analytics():
  path="Data/hotel_bookings.csv"
  data_reader= FetchData(path)
  df= data_reader.load()
  analytics = PlotAnalytics(df)
    
  # Generate and encode plots
  plots = analytics.analyze_data()
  return jsonify(plots)

@app.route("/ask", methods=["POST"])
def chat():
    data = request.json
    query = data.get("query", "")

    if not query:
        return jsonify({"error": "Query is required"}), 400

    # Fetch SQL results
    sql_results = session["SQL_Agent"].generate_and_execute_query(query)

    if "Error" in sql_results:
      sql_results= "Sql results not generated"
    else:
      sql_results= str(sql_results)
    
    print(sql_results, type(sql_results))
    
    # Combine user query with SQL results & document retriever context
    payload= f"""
      SQL Query Results: {sql_results}
      User Query: {query}
      Response:
      """
    response_text = session["rag_chain"].invoke(payload)

    #response_text = response.split("<|assistant|>")[-1].strip()

    # Update chat history
    session["chat_history"].append({"User": query, "Bot": response_text.content})

    return jsonify({"query": query, "response": response_text.content})

if __name__ == '__main__':
    app.run(port=8000,debug=True)
