# GenAIEmailProcessingApp

## Overview
GenAIEmailProcessingApp is a Flask-based web application that processes email files and extracts summaries using a machine learning model.

## Features
- Upload email files in `.eml` or `.txt` or `.pdf` or `.docx` format.
- Extract and summarize the content of the email.
- Receive additional parameters for processing.

## Prerequisites
1. Get Gemini API Key:
   - Sign up at the Gemini API website and obtain your API key.
2. Set environment variable with name `GENAI_API_KEY` in Windows:
3. Create postgresql DB 
4. Set environment variable with name 'EMAIL_PROC_APP_DB' for DB connection string starting with 'postgresql+psycopg'
   

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/GenAIEmailProcessingApp.git
    ```
2. Navigate to the project directory:
    ```bash
    cd GenAIEmailProcessingApp
    py -3 -m venv .venv
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
1. Start the Flask application:
    ```bash

    .venv\Scripts\activate
    flask run
    ```
2. Open your web browser and go to `http://127.0.0.1:5000/`.

## License
This project is licensed under the MIT License.
