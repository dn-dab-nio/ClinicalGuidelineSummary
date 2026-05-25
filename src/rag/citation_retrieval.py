def attach_citations(vectorstore, recommendations, organisation):
    results = []

    for rec in recommendations:
        docs = vectorstore.similarity_search(
            rec,
            k=1,
            filter={"organisation": organisation})

        if docs:
            best_doc = docs[0]

            results.append({
                "recommendation": rec,
                "source": best_doc.metadata.get("source"),
                "page": best_doc.metadata.get("page")
            })

        else:
            results.append({
                "recommendation": rec,
                "source": "UNKNOWN",
                "page": "UNKNOWN"
            })

    return results

