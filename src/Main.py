from src.rag.Vector_store import load_vector_store
from src.rag.Generator import generate_initial_answer, check_completeness, generate_followup_query, generate_final_answer

vectorstore = load_vector_store("vector_db")

query = f"""
Pacjentka 44 lata, brak narażenia na promieniowanie, brak rodzinnej historii raka tarczycy. 
USG: hypoechogeniczna zmiana wielkości 8 mm, o nieregularnych marginesach, podejrzenie 
mikrozwapnień, nie wykryto zmian w obrębie węzłów chłonnych. Wykonano biopsję cienkoigłową zmiany, 
zgodnie z The Bethesda System for Reporting Thyroid Cytopathology przypisano kategorię III (AUS).

Wypisz mi wytyczne kliniczne dla pacjentki.
"""

retrieved_docs = vectorstore.similarity_search(query, k=3)
context = "\n".join([doc.page_content for doc in retrieved_docs])

answer1 = generate_initial_answer(query, context)
print("---PIERWSZA ODPOWIEDŹ---")
print(answer1)

evaluation = check_completeness(answer1)
print("---DRUGA ODPOWIEDŹ---")
print(evaluation)

all_contexts = [context]

if "INCOMPLETE" in evaluation:
    follow_up_query = generate_followup_query(query, all_contexts)
    print("Follow-up query:", follow_up_query)

    new_docs = vectorstore.similarity_search(follow_up_query, k=3)
    new_context = "\n".join([doc.page_content for doc in new_docs])
    all_contexts.append(new_context)

    final_answer = generate_final_answer(query, all_contexts)
else:
    final_answer = answer1

print("---FINAL ANSWER---")
print(final_answer)

