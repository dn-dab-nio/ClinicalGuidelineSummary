
# start = time.perf_counter()
# embeddings = import_embedding_llm()
# vectorstore = load_vector_store(
#     r"C:\Users\natalia.nowak\Desktop\ClinicalGuidelineSummary\src\scripts\vector_db", embeddings)
#
# query = f"""
#     Pacjentka 44 lata, brak narażenia na promieniowanie, brak rodzinnej historii raka tarczycy.
#     USG: hypoechogeniczna zmiana wielkości 8 mm, o nieregularnych marginesach, podejrzenie
#     mikrozwapnień, nie wykryto zmian w obrębie węzłów chłonnych. Wykonano biopsję cienkoigłową zmiany,
#     zgodnie z The Bethesda System for Reporting Thyroid Cytopathology przypisano kategorię III (AUS).
#
#     Wypisz mi wytyczne kliniczne dla pacjentki.
#     """
#
# classification_uicc = run_staging(query)
# print("--- CLASSIFICATION UICC/UJCC, 8th edition ---")
# print(classification_uicc)
#
# quidelines = run_iterative_rag2(vectorstore, classification_uicc)
#
# print("--- THERAPY FOR PATIENT---")
# for klucz, wartosc in quidelines.items():
#     print(f"{klucz}: \n {wartosc} \n\n")
#
# end = time.perf_counter()
# min = (end - start) / 60
# print(f"Total time: {end - start:.4f} sec   ==   {min:.4f} min")
#
# process = psutil.Process(os.getpid())
# print(f"Memory (MB): {process.memory_info().rss / 1024 ** 2:.2f}")
# print(f"CPU (%): {psutil.cpu_percent(interval=1)}")


ziomek = {"wyniki": {"kot": 'kot', "pies": 'pis'}, "mmm": {"kot": {"dlugosc": 2, "siersc": 5}, "pies": {"dlugosc": 3, "siersc": 6}}}

lol = ziomek["wyniki"]["pies"]

for org in ziomek["wyniki"]:
    result = ziomek["wyniki"][org]
    metrics = ziomek["mmm"][org]

    print(f"--- {org} ---")
    print(f"{result}")
    for m in metrics:
        print(f"{m}: {metrics[m]}")

