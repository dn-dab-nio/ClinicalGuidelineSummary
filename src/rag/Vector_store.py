from langchain_community.vectorstores import FAISS

def create_vector_store(docs, embeddings):
    return FAISS.from_documents(docs, embeddings)

def save_vector_store(vectorstore, path="vectorstore"):
    vectorstore.save_local(path)

def load_vector_store(path="vectorstore"):
    return FAISS.load_local(path)

