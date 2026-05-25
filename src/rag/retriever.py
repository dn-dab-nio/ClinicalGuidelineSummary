from langchain_core.documents import Document


def retrieve_context(vectorstore, query: str, k:int=3, organisation:str=None) -> list[Document]:

    if organisation:
        retrieved_docs = vectorstore.similarity_search(
            query,
            k=k,
            #filter={"organisation": organisation}
        )
    else:
        retrieved_docs = vectorstore.similarity_search(query, k=k)

    return retrieved_docs


