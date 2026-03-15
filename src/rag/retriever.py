def retrieve_context(vectorstore, query, k=3, organisation=None):

    if organisation:
        retrieved_docs = vectorstore.similarity_search(
            query,
            k=k,
            filter={"organisation": organisation}
        )
    else:
        retrieved_docs = vectorstore.similarity_search(query, k=k)

    context = "\n".join([
        f"[{doc.metadata['source']}]\n{doc.page_content}"
        for doc in retrieved_docs])

    return context

