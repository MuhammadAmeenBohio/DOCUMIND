import os
import requests
import mimetypes
import fitz  # PyMuPDF for PDF extraction
import docx
from bs4 import BeautifulSoup

def extract_text_from_pdf(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def extract_text_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.get_text()
    return "Failed to fetch content."

def analyze_input(user_input):
    if user_input.startswith("http://") or user_input.startswith("https://"):
        return "url"
    elif os.path.exists(user_input):
        mime_type, _ = mimetypes.guess_type(user_input)
        if mime_type:
            if "pdf" in mime_type:
                return "pdf"
            elif "officedocument.wordprocessingml.document" in mime_type:
                return "docx"
            elif "text/plain" in mime_type:
                return "txt"
    return "unknown"

def process_input(user_input):
    input_type = analyze_input(user_input)
    
    if input_type == "pdf":
        text = extract_text_from_pdf(user_input)
    elif input_type == "docx":
        text = extract_text_from_docx(user_input)
    elif input_type == "txt":
        text = extract_text_from_txt(user_input)
    elif input_type == "url":
        text = extract_text_from_url(user_input)
    else:
        text = "Unsupported file type or invalid input."
    
    print("Extracted Text:\n", text)
    return text

# Example usage
if __name__ == "__main__":
    user_input = input("Enter file path or URL: ")
    process_input(user_input)