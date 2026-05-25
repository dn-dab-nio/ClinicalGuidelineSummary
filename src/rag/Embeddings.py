from langchain_ollama import OllamaEmbeddings

def import_embedding_llm():
    return OllamaEmbeddings(model="nomic-embed-text", base_url="http://127.0.0.1:11434")

