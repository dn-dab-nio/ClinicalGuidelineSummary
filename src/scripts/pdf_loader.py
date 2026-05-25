import os
import pytesseract
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Users\natalia.nowak\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
)


def extract_pages_from_pdf(path: str) -> list[dict]:
    reader = PdfReader(path)
    images = convert_from_path(
        path,
        poppler_path=r"C:\Users\natalia.nowak\AppData\Local\Programs\Release-25.12.0-0\poppler-25.12.0\Library\bin"
    )

    pages = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text()

        if not text or len(text.strip()) < 50:
            print(f"OCR page {i + 1}")
            image = images[i]

            text = pytesseract.image_to_string(
                image,
                lang="osd+eng+pol"
            )

        pages.append({
            "page": i + 1,
            "text": text
        })

    return pages

def chunk_text(text: str) -> list[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    chunks = splitter.split_text(text)
    print(f"Liczba chunków: {len(chunks)}")

    return chunks


def detect_organisation(path: str):
    org_names = ["ATA", "NCCN", "KOM", "ESMO", "BTA"]
    filename = os.path.basename(path).upper()

    for org in org_names:
        if org in filename:
            return org

    return "UNKNOWN"


def pdf_to_documents(paths: list[str]) -> list[Document]:
    docs = []

    for path in paths:
        print(f"\nProcessing: {os.path.basename(path)}")
        organisation = detect_organisation(path)
        pages = extract_pages_from_pdf(path)

        for page_data in pages:
            page_number = page_data["page"]
            text = page_data["text"]

            chunks = chunk_text(text)
            for chunk_id, chunk in enumerate(chunks):

                doc = Document(
                    page_content=chunk,

                    metadata={
                        "organisation": organisation,
                        "source": os.path.basename(path),
                        "page": page_number,
                        "chunk_id": chunk_id
                    }
                )
                docs.append(doc)

    return docs
