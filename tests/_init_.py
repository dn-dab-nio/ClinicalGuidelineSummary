import pytesseract
from PyPDF2 import PdfReader
from pdf2image import convert_from_path

def extract_text_from_pdf2(path):
    reader = PdfReader(path)
    texts = []
    images = convert_from_path(
        path,
        poppler_path=r"C:\Users\Natalia\Documents\Poppler\Release-25.12.0-0\poppler-25.12.0\Library\bin"
    )

    for i, page in enumerate(reader.pages):
        if i == 69:
            text = page.extract_text()
            if text and len(text.strip()) > 50:
                texts.append(text)
            else:
                print(f"OCR page {i}")
                image = images[i]
                text = pytesseract.image_to_string(image, lang="osd+eng+pol")
                texts.append(text)

    return "\n".join(texts)


pdf_path = "data/KOM Wytyczne 2022.pdf"

text = extract_text_from_pdf2(pdf_path)

print("----- OCR OUTPUT -----")
print(text[:1000])