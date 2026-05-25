from src.staging.uicc_extractor import tnm_extract
from src.rag.Vector_store import load_vector_store
from src.rag.Embeddings import import_embedding_llm
#from staging.staging_pipeline import run_staging
from src.rag.rag_engine import run_iterative_rag

query = f"""
     Pacjentka 44 lata, brak narażenia na promieniowanie, brak rodzinnej historii raka tarczycy.
     USG: hypoechogeniczna zmiana wielkości 8 mm, o nieregularnych marginesach, podejrzenie
     mikrozwapnień, nie wykryto zmian w obrębie węzłów chłonnych. Wykonano biopsję cienkoigłową zmiany,
     zgodnie z The Bethesda System for Reporting Thyroid Cytopathology przypisano kategorię III (AUS).

     Wypisz mi wytyczne kliniczne dla pacjentki.
     """
embeddings = import_embedding_llm()
vectorstore = load_vector_store(embeddings)
classification = { #DO TESTU
            "age": 45,
            "T": "T2",
            "N": "N1",
            "M": "M0",
            "cancer_type": {
                "label": "Papillary Thyroid Carcinoma",
                "group": "Differentiated thyroid carcinoma"
            },
            "Stage": "Stage II",
            "Bethesda_System_Category": "III (AUS)",
            "USG": "Performed; hypoechogenic nodule 8 mm, irregular margins, suspected microcalcifications, no lymph node involvement",
            "Biopsy": "Performed; fine‑needle aspiration"
        }


quidelines = run_iterative_rag(vectorstore, classification, debug=False)

print("\n--- THERAPY FOR PATIENT--- \n")

for org in quidelines["answers"]:
     result = quidelines["answers"][org]
     metrics = quidelines["metrics"][org]

     print(f"\n \n--- {org} ---")

     print("\n Recommended: \n")
     for item in result.recommended:
         print(f"- {item} \n")

     print("\n To consider: \n")
     for item in result.to_consider:
         print(f"- {item} \n")

     print("\n Not recommended: \n")
     for item in result.not_recommended:
         print(f"- {item} \n")

#answer = run_staging(query, vectorstore)
#print(answer)

#
# from src.validation.validator import validate_guideline_answer
# exmpl = {
#     "Recommended": ["a", "b"],
#     "To consider": ["c", "d", ""],
#     "Not recommended": ["e", "   f    "]
# }
#
# tt = validate_guideline_answer(exmpl)
# print(tt)

# (.venv) PS C:\Users\natalia.nowak\Desktop\ClinicalGuidelineSummary> streamlit run app.py
# Traceback (most recent call last):
#   File "<frozen runpy>", line 198, in _run_module_as_main
#   File "<frozen runpy>", line 88, in _run_code
#   File "C:\Users\natalia.nowak\Desktop\ClinicalGuidelineSummary\.venv\Scripts\streamlit.exe\__main__.py", line 7, in <module>
#   File "C:\Users\natalia.nowak\Desktop\ClinicalGuidelineSummary\.venv\Lib\site-packages\click\core.py", line 1485, in __call__
#     return self.main(*args, **kwargs)
#            ^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "C:\Users\natalia.nowak\Desktop\ClinicalGuidelineSummary\.venv\Lib\site-packages\click\core.py", line 1406, in main
#     rv = self.invoke(ctx)
#          ^^^^^^^^^^^^^^^^
#   File "C:\Users\natalia.nowak\Desktop\ClinicalGuidelineSummary\.venv\Lib\site-packages\click\core.py", line 1873, in invoke
#     return _process_result(sub_ctx.command.invoke(sub_ctx))
#                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "C:\Users\natalia.nowak\Desktop\ClinicalGuidelineSummary\.venv\Lib\site-packages\click\core.py", line 1269, in invoke
#     return ctx.invoke(self.callback, **ctx.params)
#            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "C:\Users\natalia.nowak\Desktop\ClinicalGuidelineSummary\.venv\Lib\site-packages\click\core.py", line 824, in invoke
#     return callback(*args, **kwargs)
#            ^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "C:\Users\natalia.nowak\Desktop\ClinicalGuidelineSummary\.venv\Lib\site-packages\streamlit\web\cli.py", line 238, in main_run
#     _main_run(target, args, flag_options=kwargs)
#   File "C:\Users\natalia.nowak\Desktop\ClinicalGuidelineSummary\.venv\Lib\site-packages\streamlit\web\cli.py", line 274, in _main_run
#     bootstrap.run(file, is_hello, args, flag_options)
#   File "C:\Users\natalia.nowak\Desktop\ClinicalGuidelineSummary\.venv\Lib\site-packages\streamlit\web\bootstrap.py", line 352, in run
#     asyncio.run(run_server())
#   File "C:\Users\natalia.nowak\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 195, in run
#     return runner.run(main)
#            ^^^^^^^^^^^^^^^^
#   File "C:\Users\natalia.nowak\AppData\Local\Programs\Python\Python312\Lib\asyncio\runners.py", line 118, in run
#     return self._loop.run_until_complete(task)
#            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "C:\Users\natalia.nowak\AppData\Local\Programs\Python\Python312\Lib\asyncio\base_events.py", line 691, in run_until_complete
#     return future.result()
#            ^^^^^^^^^^^^^^^
#   File "C:\Users\natalia.nowak\Desktop\ClinicalGuidelineSummary\.venv\Lib\site-packages\streamlit\web\bootstrap.py", line 340, in run_server
#     await server.start()
#   File "C:\Users\natalia.nowak\Desktop\ClinicalGuidelineSummary\.venv\Lib\site-packages\streamlit\web\server\server.py", line 270, in start
#     start_listening(app)
#   File "C:\Users\natalia.nowak\Desktop\ClinicalGuidelineSummary\.venv\Lib\site-packages\streamlit\web\server\server.py", line 130, in start_listening
#     start_listening_tcp_socket(http_server)
#   File "C:\Users\natalia.nowak\Desktop\ClinicalGuidelineSummary\.venv\Lib\site-packages\streamlit\web\server\server.py", line 197, in start_listening_tcp_socket
#     http_server.listen(port, address)
#   File "C:\Users\natalia.nowak\Desktop\ClinicalGuidelineSummary\.venv\Lib\site-packages\tornado\tcpserver.py", line 183, in listen
#     sockets = bind_sockets(
#               ^^^^^^^^^^^^^
#   File "C:\Users\natalia.nowak\Desktop\ClinicalGuidelineSummary\.venv\Lib\site-packages\tornado\netutil.py", line 162, in bind_sockets
#     sock.bind(sockaddr)
# PermissionError: [WinError 10013] Została podjęta próba uzyskania dostępu do gniazda w sposób zabroniony przez
# przypisane do niego uprawnienia dostępu

