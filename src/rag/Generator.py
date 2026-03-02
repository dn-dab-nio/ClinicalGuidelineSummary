from langchain_ollama import OllamaLLM

def generate_answer(query, context):
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


def evaluate_answer(answer):
    prompt = f"""
Evaluate the following answer.

If it fully answers the question and is based only on the provided context, respond with: COMPLETE.
If important medical information is missing, respond with: INCOMPLETE.

Answer:
{answer}
"""
    return llm.invoke(prompt)


def generate_followup_query(og_query, previous_answer):
    prompt = f"""
The original question was:
{og_query}

The current answer is incomplete:
{previous_answer}

Generate ONE focused follow-up search query
that would retrieve the missing medical information.
Only output the query.
"""
    return llm.invoke(prompt)

llm = OllamaLLM(model="llama3.2:latest")

