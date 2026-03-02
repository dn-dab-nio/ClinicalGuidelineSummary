from src.rag.Vector_store import load_vector_store
from src.rag.Embeddings import import_embedding_llm
from src.rag.rag_engine import run_iterative_rag

embeddings = import_embedding_llm()
vectorstore = load_vector_store(r"C:\Users\Natalia\Desktop\Projekty_python\ClinicalGuidelineSummary\src\scripts\vector_db", embeddings)

query = f"""
Pacjentka 44 lata, brak narażenia na promieniowanie, brak rodzinnej historii raka tarczycy.
USG: hypoechogeniczna zmiana wielkości 8 mm, o nieregularnych marginesach, podejrzenie
mikrozwapnień, nie wykryto zmian w obrębie węzłów chłonnych. Wykonano biopsję cienkoigłową zmiany,
zgodnie z The Bethesda System for Reporting Thyroid Cytopathology przypisano kategorię III (AUS).

Wypisz mi wytyczne kliniczne dla pacjentki.
"""

answer = run_iterative_rag(vectorstore, query)

print("---FINAL ANSWER---")
print(answer)

