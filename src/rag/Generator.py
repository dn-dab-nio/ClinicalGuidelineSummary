from langchain_ollama import OllamaLLM

def generate_guideline_answer(context, classification_json, organisation):
    prompt = f"""
You are clinical guideline assistant.
Use ONLY the following context from {organisation} guidelines.
If information is missing, say: "INSUFFICIENT INFORMATION".

Context: {context}

Patient classification:
{classification_json}

Provide concise recommendations according to {organisation} guidelines.
Do not include recommendations from other organisations.

Answer must be focused on:
* What recommended - best recommendations
* To consider - recommendations that doctor should consider
* What not recommended - bad options for patient's therapy

Answer MUST contain these 3 requirements.
"""


    response = llm.invoke(prompt)
    return response


def evaluate_answer(answer, base_query, query, context):
    prompt = f"""
Evaluate the following answer.

If it fully answers questions and is based only on the provided context, respond with: COMPLETE.
If important medical information is missing, respond with: INCOMPLETE.

Main question: 
{base_query}

Question generated to fill missing medical information.
{query} 

Other Questions:
-Does gap "to consider" contain informations about therapy that doctor should consider?
-Does gap "What not recommended" contain informations about therapy that doctor should NOT (!) consider?

Context: 
{context}

Answer:
{answer}

RESPOND ONLY 'COMPLETE' OR 'INCOMPLETE'.
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

llm = OllamaLLM(model="ahmgam/medllama3-v20:latest")

