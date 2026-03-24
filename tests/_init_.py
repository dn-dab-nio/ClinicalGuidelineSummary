from src.rag.retriever import retrieve_context
from src.rag.Generator import evaluate_answer, generate_followup_query
from src.rag.query_compiler import build_data_query
from src.rag.Generator import generate_guideline_answer
from src.rag.Vector_store import load_vector_store
from src.rag.Embeddings import import_embedding_llm
from src.staging.staging_pipeline import run_staging
import time
import psutil
import os


def run_iterative_rag2(vectorstore, classification_json: dict, max_iterations: int = 3, k: int = 5, debug: bool = True) -> dict:
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
                context = retrieve_context(vectorstore, query, k=k, organisation=org)

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
                answer = generate_guideline_answer(context_together, classification_json, org)
            except Exception as e:
                print(f"[ERROR][{org}] Generation failed: {e}")
                break

            # --- EVALUATION ---
            try:
                evaluation = evaluate_answer(answer, query, context_together)
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
                query = generate_followup_query(query, context_together, evaluation)
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


start = time.perf_counter()
embeddings = import_embedding_llm()
vectorstore = load_vector_store(
    r"C:\Users\natalia.nowak\Desktop\ClinicalGuidelineSummary\src\scripts\vector_db", embeddings)

query = f"""
    Pacjentka 57 lata, brak narażenia na promieniowanie, brak rodzinnej historii raka tarczycy.
    USG: hypoechogeniczna zmiana wielkości 2 cm, o nieregularnych marginesach, podejrzenie
    mikrozwapnień, nie wykryto zmian w obrębie węzłów chłonnych. Wykonano biopsję cienkoigłową zmiany,
    zgodnie z The Bethesda System for Reporting Thyroid Cytopathology przypisano kategorię III (AUS).

    Wypisz mi wytyczne kliniczne dla pacjentki.
    """

classification_uicc = run_staging(query)
print("--- CLASSIFICATION UICC/UJCC, 8th edition ---")
print(classification_uicc)

quidelines = run_iterative_rag2(vectorstore, classification_uicc)

print("--- THERAPY FOR PATIENT---")
for klucz, wartosc in quidelines.items():
    print(f"{klucz}: \n {wartosc} \n\n")

end = time.perf_counter()
print(f"Total time: {end - start:.4f} sec")

process = psutil.Process(os.getpid())
print(f"Memory (MB): {process.memory_info().rss / 1024 ** 2:.2f}")
print(f"CPU %: {psutil.cpu_percent(interval=1)}")

# Traceback (most recent call last):
#   File "C:\Users\natalia.nowak\Desktop\ClinicalGuidelineSummary\.venv\Lib\site-packages\langchain_community\vectorstores\faiss.py", line 56, in dependable_faiss_import
#     import faiss
# ModuleNotFoundError: No module named 'faiss'
#
# During handling of the above exception, another exception occurred:
#
# Traceback (most recent call last):
#   File "C:\Users\natalia.nowak\Desktop\ClinicalGuidelineSummary\tests\_init_.py", line 125, in <module>
#     vectorstore = load_vector_store(
#                   ^^^^^^^^^^^^^^^^^^
#   File "C:\Users\natalia.nowak\Desktop\ClinicalGuidelineSummary\src\rag\Vector_store.py", line 10, in load_vector_store
#     return FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)
#            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "C:\Users\natalia.nowak\Desktop\ClinicalGuidelineSummary\.venv\Lib\site-packages\langchain_community\vectorstores\faiss.py", line 1204, in load_local
#     faiss = dependable_faiss_import()
#             ^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "C:\Users\natalia.nowak\Desktop\ClinicalGuidelineSummary\.venv\Lib\site-packages\langchain_community\vectorstores\faiss.py", line 58, in dependable_faiss_import
#     raise ImportError(
# ImportError: Could not import faiss python package. Please install it with `pip install faiss-gpu` (for CUDA supported GPU) or `pip install faiss-cpu` (depending on Python version).
#
