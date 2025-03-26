import os
import json
import sqlite3
from google import genai

from .document_extractor import read_data_from_file
from .db_util import db, RequestType  # Import the necessary modules
from .db_util import load_request_types_from_db  # Import the function to load request types from DB

def get_genai_client():
    api_key = os.environ.get("GENAI_API_KEY") or os.getenv("GENAI_API_KEY")
    print(f"Retrieved API key: {api_key}")  # Debug print statement
    if api_key is None:
        raise ValueError("API key is not set. Please set the GENAI_API_KEY environment variable.")
    
    client = genai.Client(api_key=api_key)
    print("GenAI client initialized.")
    return client

def summarize_eml_file(uploaded_file_path):
    print("Starting to summarize the email file.")
    content = read_data_from_file(uploaded_file_path)
    print("Email content extracted.")

    request_types = load_request_types_from_db()  # Load request types from DB
    client = get_genai_client()
    
    response = client.models.generate_content(
        model="gemini-2.0-flash", 
        contents=f"(summarize as 'summary', classify based on the following request types {request_types} as list of 'requestClassification' & its confidence score as 'confidenceScore', extract key fields as 'keyFields') group by message & return it in json format. {content}"
    )
    print("Received response from GenAI.")
    return response.text