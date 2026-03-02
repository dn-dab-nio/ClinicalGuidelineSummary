from src.rag.retriever import retrieve_context
from src.rag.Generator import generate_answer, evaluate_answer, generate_followup_query

def run_iterative_rag(vectorstore, query, max_iterations=3): #na podstawie schematu z raportu
    current_query = query
    all_contexts = []

    for i in range(max_iterations):
        print(f"---iteration {i+1}---")

        #1 - retrieval
        context = retrieve_context(vectorstore, current_query)
        all_contexts.append(context)
        context_together = "\n\n".join(all_contexts)

        #2 - generator LLM
        answer = generate_answer(query, context_together)
        print(f"answer: {answer}")

        #3 - Policy Optimalization - evaluation
        evaluation = evaluate_answer(answer)
        print(f"evaluation: {evaluation}")

        #STOP jesli odpowiedz jest pelna
        if evaluation.strip() == "COMPLETE":
            return answer

        #jesli odpowiedz nie jest jeszcze super - nowe zapytanie dopełniające na temat braków
        current_query = generate_followup_query(query, context_together)
        print(f"New query: {current_query}")

    return answer