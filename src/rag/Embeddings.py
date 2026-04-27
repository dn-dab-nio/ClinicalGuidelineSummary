from langchain_ollama import OllamaEmbeddings

def import_embedding_llm():
    return OllamaEmbeddings(model="nomic-embed-text")

