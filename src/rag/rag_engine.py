from src.rag.retriever import retrieve_context
from src.rag.Generator import evaluate_answer, generate_followup_query
from src.rag.query_compiler import build_data_query
from src.rag.Generator import generate_guideline_answer


def run_iterative_rag(vectorstore, classification_json: dict, max_iterations:int=3) -> dict:

    organisations = ["KOM", "NCCN", "ATA", "BTA", "ESMO"]

    base_query = build_data_query(classification_json)
    results = {}

    for org in organisations:
        all_contexts = []
        query = base_query
        answer = None
        for i in range(max_iterations):
            # 1 - retrieval
            context = retrieve_context(vectorstore, query, k=5, organisation=org)
            all_contexts.append(context)
            context_together = "\n\n".join(all_contexts)

            # 2 - generator LLM
            answer = generate_guideline_answer(context_together, classification_json, org)

            # 3 - Policy Optimalization - evaluation
            evaluation = evaluate_answer(answer, base_query, context_together)

            # STOP jesli odpowiedz jest pelna
            if evaluation.strip() == "COMPLETE":
                results[org] = answer
                break
            else:
                query = generate_followup_query(query, context_together)

        results[org] = answer

    return results

