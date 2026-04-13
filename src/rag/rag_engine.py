from src.rag.retriever import retrieve_context
from src.rag.Generator import evaluate_answer, generate_followup_query, generate_guideline_answer
from src.rag.query_compiler import build_data_query
import time
import json


def run_iterative_rag(vectorstore, classification_json: dict, max_iterations: int = 3, k: int = 5,
                      debug: bool = True) -> dict:
    organisations = ["KOM", "NCCN", "ATA", "BTA", "ESMO"]

    base_query = build_data_query(classification_json)
    results = {}
    metrics = {}

    for org in organisations:
        org_start = time.perf_counter()

        current_query = base_query
        all_contexts = []
        answer = None

        eval_status = "UNKNOWN"
        eval_full_response = ""

        completed_iterations = 0

        if debug:
            print(f"\n=== ORGANISATION: {org} ===")

        for i in range(max_iterations):
            iter_start = time.perf_counter()

            try:
                context = retrieve_context(vectorstore, current_query, k=k, organisation=org)
            except Exception as e:
                print(f"[ERROR][{org}] Retrieval failed: {e}")
                break

            if not context:
                print(f"[WARNING][{org}] Empty context. Breaking loop.")
                break

            if not isinstance(context, str):
                try:
                    context = "\n".join([doc.page_content for doc in context])
                except AttributeError:
                    context = str(context)

            if context not in all_contexts:
                all_contexts.append(context)

            context_together = "\n\n".join(all_contexts)

            try:
                answer = generate_guideline_answer(context_together, classification_json, org)
            except Exception as e:
                print(f"[ERROR][{org}] Generation failed: {e}")
                break

            try:
                eval_raw = evaluate_answer(answer, base_query, current_query, context_together)
                eval_full_response = eval_raw  # Zapisujemy do metryk

                eval_clean = eval_raw.replace('```json', '').replace('```', '').strip()
                eval_dict = json.loads(eval_clean)
                eval_status = eval_dict.get("status", "UNKNOWN").upper()
                suggested_query = eval_dict.get("suggested_search_term", "")

            except json.JSONDecodeError:
                print(f"[WARNING][{org}] Evaluator did not return valid JSON. Falling back to string matching.")
                eval_clean_str = eval_raw.strip().upper()
                if "UNAVAILABLE_IN_SOURCE" in eval_clean_str:
                    eval_status = "UNAVAILABLE_IN_SOURCE"
                elif "INCOMPLETE" in eval_clean_str:
                    eval_status = "INCOMPLETE"
                elif "COMPLETE" in eval_clean_str:
                    eval_status = "COMPLETE"
                suggested_query = ""
            except Exception as e:
                print(f"[ERROR][{org}] Evaluation failed: {e}")
                break

            completed_iterations += 1
            iter_time = time.perf_counter() - iter_start

            if debug:
                print(f"\n[ITER {completed_iterations}]")
                print(f"Query used: {current_query}")
                print(f"Status: {eval_status}")
                print(f"Iteration time: {iter_time:.2f}s")

            # NOWY, INTELIGENTNY WARUNEK STOPU
            if eval_status == "COMPLETE":
                if debug:
                    print(f"[STOP] Answer complete at iteration {completed_iterations}")
                break
            elif eval_status == "UNAVAILABLE_IN_SOURCE":
                if debug:
                    print(f"[STOP] Dead-end. Information not available in {org} guidelines.")
                break

            if i == max_iterations - 1:
                break

            # USTAWIENIE NOWEGO ZAPYTANIA (QUERY RELAXATION)
            try:
                if suggested_query:
                    current_query = suggested_query
                    if debug: print(f"[RELAXATION] Evaluator suggested new query: {current_query}")
                else:
                    current_query = generate_followup_query(current_query, answer)
            except Exception as e:
                print(f"[ERROR][{org}] Query refinement failed: {e}")
                break

        org_time = time.perf_counter() - org_start
        results[org] = answer

        metrics[org] = {
            "iterations_used": completed_iterations,
            "final_status": eval_status,
            "time_sec": round(org_time, 3),
            "contexts_used": len(all_contexts),
            "eval_raw": eval_full_response
        }

    return {
        "answers": results,
        "metrics": metrics
    }