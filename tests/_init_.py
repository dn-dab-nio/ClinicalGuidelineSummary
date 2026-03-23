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
from src.staging.uicc_validator import validate_json

#embeddings = import_embedding_llm()
#vectorstore = load_vector_store(r"C:\Users\Natalia\Desktop\Projekty_python\ClinicalGuidelineSummary\src\scripts\vector_db", embeddings)

query = f"""
Pacjentka w wieku 56 lat, bez znanej historii nowotworów tarczycy w rodzinie, 
nie zgłasza narażenia na promieniowanie. W USG pojedyncza hypoechogeniczna zmiana o mieszanym 
echu w przedniej części lewego płata tarczycy, wielkości 1.8 x 1 x 2.1 cm, nie wykryto zmian 
w obrębie węzłów chłonnych. Wykonano biopsję cienkoigłową zmiany, zgodnie z The Bethesda 
System for Reporting Thyroid Cytopathology przypisano kategorię V (podejrzenie 
raka pęcherzykowego)
"""

#answer = tnm_extract(query)
#answer = map_uicc(query)
#print(answer)

parsed_answer = {'age': 56, 'T': 'T1', 'N': 'N10', 'M': 'M0', 'cancer_type': {'label': 'Podejrzana raka pęcherzykowa', 'group': 'Differentiated thyroid carcinoma'}}
is_valid, message = validate_json(parsed_answer)
if not is_valid:
    print({"error": message})

######
from src.rag.retriever import retrieve_context
from src.rag.Generator import evaluate_answer, generate_followup_query
from src.rag.query_compiler import build_data_query
from src.rag.Generator import generate_guideline_answer
import time
import psutil
import os


def run_iterative_rag(
    vectorstore,
    classification_json: dict,
    max_iterations: int = 3,
    k: int = 5,
    debug: bool = True
) -> dict:

    organisations = ["KOM", "NCCN", "ATA", "BTA", "ESMO"]

    base_query = build_data_query(classification_json)
    results = {}
    metrics = {}

    process = psutil.Process(os.getpid())
    total_start = time.perf_counter()

    for org in organisations:
        org_start = time.perf_counter()

        query = base_query
        all_contexts = []
        answer = None
        evaluation = None

        if debug:
            print(f"\n=== ORGANISATION: {org} ===")

        for i in range(max_iterations):
            iter_start = time.perf_counter()

            # --- RETRIEVAL ---
            try:
                context = retrieve_context(
                    vectorstore,
                    query,
                    k=k,
                    organisation=org
                )
            except Exception as e:
                print(f"[ERROR][{org}] Retrieval failed: {e}")
                break

            if not context:
                print(f"[WARNING][{org}] Empty context")
                break

            # deduplikacja
            if context not in all_contexts:
                all_contexts.append(context)

            context_together = "\n\n".join(all_contexts)

            # --- GENERATION ---
            try:
                answer = generate_guideline_answer(
                    context_together,
                    classification_json,
                    org
                )
            except Exception as e:
                print(f"[ERROR][{org}] Generation failed: {e}")
                break

            # --- EVALUATION ---
            try:
                evaluation = evaluate_answer(
                    answer,
                    query,  # ✅ FIX (nie base_query)
                    context_together
                )
            except Exception as e:
                print(f"[ERROR][{org}] Evaluation failed: {e}")
                break

            iter_time = time.perf_counter() - iter_start

            if debug:
                print(f"\n[ITER {i+1}]")
                print(f"Query: {query}")
                print(f"Evaluation: {evaluation}")
                print(f"Iteration time: {iter_time:.2f}s")

            # --- STOP CONDITION ---
            if evaluation and evaluation.strip() == "COMPLETE":
                if debug:
                    print(f"[STOP] Answer complete at iteration {i+1}")
                break

            # --- QUERY REFINEMENT ---
            try:
                query = generate_followup_query(
                    query,
                    context_together,
                    evaluation  # ✅ FIX: dodany feedback
                )
            except Exception as e:
                print(f"[ERROR][{org}] Query refinement failed: {e}")
                break

        org_time = time.perf_counter() - org_start

        results[org] = answer

        metrics[org] = {
            "iterations_used": i + 1,
            "final_evaluation": evaluation,
            "time_sec": round(org_time, 3),
            "contexts_used": len(all_contexts),
        }

    total_time = time.perf_counter() - total_start

    # --- SYSTEM METRICS ---
    memory_mb = process.memory_info().rss / 1024**2
    cpu_percent = psutil.cpu_percent(interval=0.5)

    metrics["SYSTEM"] = {
        "total_time_sec": round(total_time, 3),
        "memory_mb": round(memory_mb, 2),
        "cpu_percent": cpu_percent
    }

    if debug:
        print("\n=== SYSTEM METRICS ===")
        print(metrics["SYSTEM"])

    return {
        "answers": results,
        "metrics": metrics
    }
