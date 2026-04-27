import pytesseract
from PyPDF2 import PdfReader
from langchain_core.documents import Document
from pdf2image import convert_from_path
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

pytesseract.pytesseract.tesseract_cmd = r"C:\Users\natalia.nowak\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

def extract_text_from_pdf(path: str) -> str:
    reader = PdfReader(path)
    texts = []
    images = convert_from_path(
        path,
        poppler_path=r"C:\Users\natalia.nowak\AppData\Local\Programs\Release-25.12.0-0\poppler-25.12.0\Library\bin"
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

def chunk_text(text: str) -> list[str]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = splitter.split_text(text)

    for i, chunk in enumerate(chunks):
        if len(chunk) > 2000:
            print(f"UWAGA: Duży chunk {i}, długość: {len(chunk)} znaków.")

    print(f"Liczba chunków: {len(chunks)}")
    return chunks


def detect_organisation(path: str):
    org_names = ["ATA", "NCCN", "KOM", "ESMO", "BTA"]
    filename = os.path.basename(path).upper()

    for org in org_names:
        if org in filename:
            return org

    return None


def pdf_to_documents(paths: list[str]) -> list[Document]:
    docs = []
    for path in paths:
        org = detect_organisation(path)
        text = extract_text_from_pdf(path)
        chunks = chunk_text(text)
        docs.extend([Document(
            page_content=chunk,
            metadata={
                "organisation": org,
                "source": os.path.basename(path)
            }
        ) for chunk in chunks])
    return docs

