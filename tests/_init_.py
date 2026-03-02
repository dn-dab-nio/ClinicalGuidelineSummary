# import pytesseract
# from PyPDF2 import PdfReader
# from pdf2image import convert_from_path
#
# #to jest funkcja ta sama co w pdf_loader, ale zniekształciłam ją tylko żeby mi to wykonał dla
# #strony ze schematem w postaci zdjęcia, który jest obrócony o 90 stopni - strona 7
#
# #też sprawdzałam, czy czyta polskie znaki
# def extract_text_from_pdf2(path):
#     reader = PdfReader(path)
#     texts = []
#     images = convert_from_path(
#         path,
#         poppler_path=r"C:\Users\Natalia\Documents\Poppler\Release-25.12.0-0\poppler-25.12.0\Library\bin"
#     )
#
#     for i, page in enumerate(reader.pages):
#         if i == 6:
#             text = page.extract_text()
#             if text and len(text.strip()) > 50: #ignoruje strony prawie puste, z samym naglowkiem albo wlasnie schemat
#                 texts.append(text)
#             else:
#                 print(f"OCR page {i}")
#                 image = images[i]
#                 text = pytesseract.image_to_string(image, lang="osd+eng+pol")
#                 texts.append(text)
#
#     return "\n".join(texts)
#
#
# pdf_path1 = r"C:\Users\Natalia\Desktop\wolontariat\WYTYCZNE\KOM Wytyczne 2022.pdf" #strona 70
# pdf_path2 = r"C:\Users\Natalia\Desktop\ESMO Wytyczne 2019.pdf" #strona 7
#
# text = extract_text_from_pdf2(pdf_path2)
#
# print("----- OCR OUTPUT -----")
# print(text[:1000])

from src.staging.uicc_mapper import map_uicc
from src.staging.uicc_extractor import tnm_extract
from src.rag.Vector_store import load_vector_store
from src.rag.Embeddings import import_embedding_llm

embeddings = import_embedding_llm()
vectorstore = load_vector_store(r"C:\Users\Natalia\Desktop\Projekty_python\ClinicalGuidelineSummary\src\scripts\vector_db", embeddings)

query = f"""
Pacjentka w wieku 56 lat, bez znanej historii nowotworów tarczycy w rodzinie, 
nie zgłasza narażenia na promieniowanie. W USG pojedyncza hypoechogeniczna zmiana o mieszanym 
echu w przedniej części lewego płata tarczycy, wielkości 1.8 x 1 x 2.1 cm, nie wykryto zmian 
w obrębie węzłów chłonnych. Wykonano biopsję cienkoigłową zmiany, zgodnie z The Bethesda 
System for Reporting Thyroid Cytopathology przypisano kategorię V (podejrzenie 
raka pęcherzykowego)
"""

answer = tnm_extract(query)
#answer = map_uicc(query)
print(answer)



