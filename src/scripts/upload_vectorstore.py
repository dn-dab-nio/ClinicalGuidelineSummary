from src.rag.Investigation import pdf_to_documents
from src.rag.Embeddings import import_embedding_llm
from src.rag.Vector_store import create_vector_store, save_vector_store
import os

data_folder = "data"
pdf_files = [os.path.join(data_folder, f) for f in os.listdir(data_folder)]
docs = pdf_to_documents(pdf_files)

embeddings = import_embedding_llm()

vectorstore = create_vector_store(docs, embeddings)
save_vector_store(vectorstore, "vector_db")

