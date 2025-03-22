Hotel Booking Analytics with RAG-Enabled SQL Querying System
### 📌 Overview
This project is an advanced Retrieval-Augmented Generation (RAG) based Hotel Booking Analytics system that enables SQL-driven querying for insightful analysis. It integrates Generative AI with SQL-based data retrieval, allowing users to ask natural language questions and get AI-generated responses based on structured hotel booking data.

### 🚀 Features
Natural Language to SQL: Users can ask queries in English, and the system translates them into SQL.

RAG-Powered Insights: Combines retrieved database information with context-aware generative AI responses.

Flask API Backend: Manages query processing and response generation.

Multiple LLM Support:
✅ Google Gemini Flash (Lightweight & fast, currently used)
✅ Llama 2 (For high-performance computation on GPUs)

SQL Query Execution: Connects to a PostgreSQL/SQLite database and dynamically executes queries.

Vector Database Retrieval: Uses ChromaDB for efficient information retrieval.

Seamless JSON Responses: Ensures AI-generated answers are structured for frontend integration.

Data Visualization & Analytics: Generates key insights using Matplotlib & Seaborn.

# For undertanding better about the api end points and tested examples, check the Test_Documents.pdf in th repository

### 🛠️ Tech Stack
Backend: Flask, LangChain

LLMs:
✅ Gemini Flash (Currently Used)
✅ Llama 2 (For High GPU Compute)

Database: SQLite

Embedding & Retrieval: ChromaDB 

Data Visualization: Matplotlib, Seaborn

Frontend (Planned): React.js

### 📌 Setup Instructions
For Windows Users
1️⃣ Clone the Repository

**`git clone https://github.com/Sayan836/Hotel-Booking-Analytics-with-RAG-Enabled-SQL-Querying-System.git`**
**`cd Hotel-Booking-Analytics-with-RAG-Enabled-SQL-Querying-System`**
2️⃣ Create a Virtual Environment

**`virtualenv env`**
3️⃣ Activate the Virtual Environment

**`.\env\Scripts\activate.ps1`**

### 4️⃣ Install Required Dependencies

**`pip install -r requirements.txt`**
5️⃣ Set Up Environment Variables

Edit the .env file and add:

**`
GEMINI_API_KEY=your_gemini_api_key  # Get this from Google Cloud Console
LLAMA_MODEL_PATH=path_to_llama_weights  # If using Llama 2
DATABASE_URL=sqlite:///database/hotel_bookings.db
`**
⚠️ Make sure the Gemini API key is for text generation only!

6️⃣ Run the Application

**`python .\app.py`**
or
**`python3 .\app.py`**

⚠️ Note: You must have Python 3.10+ installed to run the files.


