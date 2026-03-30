from src.rag.retriever import retrieve_context
from src.rag.Generator import evaluate_answer, generate_followup_query
from src.rag.query_compiler import build_data_query
from src.rag.Generator import generate_guideline_answer
import time
import psutil
import os


def run_iterative_rag(vectorstore, classification_json: dict, max_iterations: int = 3, k: int = 5, debug: bool = True) -> dict:
    organisations = ["KOM", "NCCN", "ATA", "BTA", "ESMO"]

    base_query = build_data_query(classification_json)
    results = {}
    metrics = {}

    for org in organisations:
        org_start = time.perf_counter()

        query =  "No new followup query"
        all_contexts = []
        answer = None
        evaluation = None

        if debug:
            print(f"\n=== ORGANISATION: {org} ===")

        for i in range(max_iterations):
            iter_start = time.perf_counter()

            try:
                context = retrieve_context(vectorstore, query, k=k, organisation=org)

            except Exception as e:
                print(f"[ERROR][{org}] Retrieval failed: {e}")
                break

            if not context:
                print(f"[WARNING][{org}] Empty context")
                break

            if context not in all_contexts:
                all_contexts.append(context)

            context_together = "\n\n".join(all_contexts)

            try:
                answer = generate_guideline_answer(context_together, classification_json, org)
            except Exception as e:
                print(f"[ERROR][{org}] Generation failed: {e}")
                break

            try:
                evaluation = evaluate_answer(answer, base_query, query, context_together)
            except Exception as e:
                print(f"[ERROR][{org}] Evaluation failed: {e}")
                break

            iter_time = time.perf_counter() - iter_start

            if debug:
                print(f"\n[ITER {i+1}]")
                print(f"Query: {query}")
                print(f"Evaluation: {evaluation}")
                print(f"Iteration time: {iter_time:.2f}s")

            if evaluation and evaluation.strip() == "COMPLETE":
                if debug:
                    print(f"[STOP] Answer complete at iteration {i+1}")
                break

            try:
                query = generate_followup_query(query, answer)
            except Exception as e:

                print(f"[ERROR][{org}] Query refinement failed: {e}")
                break

        org_time = time.perf_counter() - org_start

        results[org] = answer

        metrics[org] = {
            "iterations_used": i + 1,
            "final_evaluation": evaluation,
            "time_sec": round(org_time, 3),
            "contexts_used": len(all_contexts),
        }

    return {
        "answers": results,
        "metrics": metrics
    }

