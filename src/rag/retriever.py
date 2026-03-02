def retrieve_context(vectorstore, query, k=3):
    retrieved_docs = vectorstore.similarity_search(query, k=k)
    context = "\n".join([doc.page_content for doc in retrieved_docs])
    return context

