from src.rag.Vector_store import load_vector_store
from src.rag.Embeddings import import_embedding_llm
from src.rag.rag_engine import run_iterative_rag
from src.staging.staging_pipeline import run_staging
import time
#import psutil
import os


if __name__ == '__main__':
    start = time.perf_counter()
    embeddings = import_embedding_llm()
    vectorstore = load_vector_store(r"C:\Users\Natalia\Desktop\Projekty_python\ClinicalGuidelineSummary\src\scripts\vector_db", embeddings)

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

    quidelines = run_iterative_rag(vectorstore, classification_uicc)

    print("--- THERAPY FOR PATIENT---")
    for klucz, wartosc in quidelines.items():
        print(f"{klucz}: \n {wartosc} \n\n")

    end = time.perf_counter()
    print(f"Total time: {end - start:.4f} sec")

    #process = psutil.Process(os.getpid())
   # print(f"Memory (MB): {process.memory_info().rss / 1024**2:.2f}")
   # print(f"CPU %: {psutil.cpu_percent(interval=1)}")

