import os
import pandas as pd
from sqlalchemy import create_engine
from langchain.chains import create_sql_query_chain
from langchain_google_genai import GoogleGenerativeAI
from langchain_community.utilities import SQLDatabase
import sqlite3
import re

class SQL_Agent():
    def __init__(self, csv_file, db_file, llm_api_key):
        self.csv_file = csv_file
        self.db_file = db_file
        self.table_name = "booking_data"
        self.llm = GoogleGenerativeAI(model="models/gemini-2.0-flash", google_api_key=llm_api_key)
        
        # Initialize SQLite engine and database
        self.engine = create_engine(f"sqlite:///{self.db_file}")
        self.db = None
        self.chain = None
        self.load_data()
        self.initialize_query_chain()
    
    def load_data(self):
        """Loads CSV data into an SQLite database."""
        df = pd.read_csv(self.csv_file)
        df.to_sql(self.table_name, self.engine, if_exists="replace", index=False)
        print("✅ Data loaded into SQLite database.")
    
    def initialize_query_chain(self):
        """Initializes the SQLDatabase and LLM query chain."""
        self.db = SQLDatabase(self.engine, sample_rows_in_table_info=3)
        self.chain = create_sql_query_chain(self.llm, self.db)
        print("✅ SQL Query Chain Initialized.")
    
    def generate_and_execute_query(self, user_question):
        """Generates an SQL query using LLM and executes it."""
        query_dict = self.chain.invoke({"question": user_question})
        sql_query = query_dict if isinstance(query_dict, str) else query_dict.get("text", "")
        
        # Remove unwanted markdown formatting
        sql_query = re.sub(r"```[\s\S]*?\n", "", sql_query).strip()
        sql_query = re.sub(r"```", "", sql_query).strip()
        
        # Execute query
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        try:
            print("\n🔹 Generated SQL Query:\n", sql_query)
            cursor.execute(sql_query)
            result = cursor.fetchall()
        except Exception as e:
            result = f"⚠️ Error: {str(e)}"
        
        conn.close()
        print("\n✅ Query Output:\n", result)
        return result

# Example Usage
if __name__ == "__main__":
    csv_path = "/content/drive/MyDrive/Projects/Hotel_Booking_Analytics/hotel_bookings.csv"
    database_path = "database.sqlite"
    google_api_key = "your_google_api_key_here"
    
    hotel_analytics = SQL_Agent(csv_path, database_path, google_api_key)
    question = "Show me the month at which the highest bookings have done"
    hotel_analytics.generate_and_execute_query(question)
