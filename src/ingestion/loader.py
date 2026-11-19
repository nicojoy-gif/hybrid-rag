
from pypdf import PdfReader
from docx import Document

from src.processing.cleaner import clean_text
from src.processing.chunker import chunk_text


def load_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def load_pdf(file_path):
    reader = PdfReader(file_path)

    content = ""

    for page in reader.pages:
        content += page.extract_text() or ""

    return content


def load_docx(file_path):
    reader = Document(file_path)

    content = ""

    for paragraph in reader.paragraphs:
        content += paragraph.text + "\n"

    return content


def load_document(file_path):
    extension = file_path.suffix.lower()

    if extension == ".pdf":
        content = load_pdf(file_path)

    elif extension == ".docx":
        content = load_docx(file_path)

    elif extension == ".txt":
        content = load_txt(file_path)

    else:
        raise ValueError("File type not supported")

    return clean_text(content)


def load_and_chunk_document(file_path):
    cleaned_text = load_document(file_path)

    return chunk_text(
        cleaned_text,
        chunk_size=150,
        overlap=50
    )
