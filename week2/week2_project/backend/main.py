from fastapi import FastAPI
from pathlib import Path
from pypdf import PdfReader
from groq import groq


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
    resume_text = read_pdf(Path("E:/AI/week2/week2_project/backend/Khushee_resume.pdf"))
    print(resume_text)
    return{
        "message": "resume parsed"
    }