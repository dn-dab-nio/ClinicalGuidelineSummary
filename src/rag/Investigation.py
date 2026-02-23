import pytesseract
from PyPDF2 import PdfReader
from langchain_core.documents import Document
from pdf2image import convert_from_path
from langchain_text_splitters import RecursiveCharacterTextSplitter
#PDF + OCR + CHUNKING

pytesseract.pytesseract.tesseract_cmd = "C:/Users/Natalia/AppData/Local/Programs/Tesseract-OCR/tesseract.exe"
def extract_text_from_pdf(path):
    reader = PdfReader(path)
    texts = []
    images = convert_from_path(
        path,
        poppler_path=r"C:\Users\Natalia\Documents\Poppler\Release-25.12.0-0\poppler-25.12.0\Library\bin"
    )

    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text and len(text.strip()) > 50:
            texts.append(text)
        else:
            print(f"OCR page {i}")
            image = images[i]
            text = pytesseract.image_to_string(image, lang="osd+eng+pol")
            texts.append(text)

    return "\n".join(texts)

def chunk_text(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = splitter.split_text(text)

    for i, chunk in enumerate(chunks):
        if len(chunk) > 2000:
            print(f"UWAGA: Duży chunk {i}, długość: {len(chunk)} znaków.")

    print(f"Liczba chunków: {len(chunks)}")
    return chunks

def pdf_to_documents(paths):
    docs = []
    for path in paths:
        text = extract_text_from_pdf(path)
        chunks = chunk_text(text)
        docs.extend([Document(page_content=chunk) for chunk in chunks])
    return docs

