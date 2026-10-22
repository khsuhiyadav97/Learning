from fastapi import FastAPI
from pathlib import Path
from pypdf import PdfReader

app=FastAPI()

def read_pdf(file_path : Path):

    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"
            
    return text

@app.get("/")
def home():
    return{
        "message": "New Your App is running"
    }