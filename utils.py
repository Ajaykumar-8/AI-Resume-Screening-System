import pdfplumber
import docx
import re


def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9 ]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text


def extract_pdf(file_path):
    text = ""

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()

            if extracted:
                text += extracted + " "

    return text


def extract_docx(file_path):
    doc = docx.Document(file_path)

    text = ""

    for para in doc.paragraphs:
        text += para.text + " "

    return text


def extract_resume_text(file_path):
    if file_path.endswith(".pdf"):
        return extract_pdf(file_path)

    elif file_path.endswith(".docx"):
        return extract_docx(file_path)

    return ""