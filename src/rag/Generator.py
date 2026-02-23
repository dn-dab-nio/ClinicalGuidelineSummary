from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="llama3.2:latest")


def generate_initial_answer(query, context):
    prompt = f"""
You are a medical assistant.
Answer ONLY based on the provided context.
If information is missing, say: "INSUFFICIENT INFORMATION".

Context:
{context}

Question:
{query}

Answer:
"""
    return llm.invoke(prompt)


def check_completeness(answer):
    prompt = f"""
Evaluate the following answer.

If it fully answers the question and is based only on the provided context, respond with: COMPLETE.
If important medical information is missing, respond with: INCOMPLETE.

Answer:
{answer}
"""
    return llm.invoke(prompt)


def generate_followup_query(query, answer):
    prompt = f"""
The original question was:
{query}

The current answer is incomplete:
{answer}

Generate ONE focused follow-up search query
that would retrieve the missing medical information.
Only output the query.
"""
    return llm.invoke(prompt)


def generate_final_answer(query, contexts):
    combined_context = "\n\n".join(contexts)

    prompt = f"""
You are a clinical guideline assistant.

Answer ONLY using the information in the context below.
Do NOT add external knowledge.

Context:
{combined_context}

Question:
{query}

Final Answer:
"""
    return llm.invoke(prompt)
