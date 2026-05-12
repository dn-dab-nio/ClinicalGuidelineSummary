from langchain_ollama import OllamaLLM
from src.validation.json_parser import parse_str_to_json
from src.validation.validator import validate_guideline_answer, GuidelineAnswer


def get_llm():
    return OllamaLLM(
        model="gpt-oss",
        temperature=0.0
    )

def generate_guideline_answer(context: str, classification_json: dict, organisation: str) -> GuidelineAnswer:
    llm = get_llm()
    prompt = f"""
You are clinical guideline assistant.
Use ONLY the following context from {organisation} guidelines.

Context: {context}

Patient classification:
{classification_json}

Provide concise recommendations according to {organisation} guidelines.
Do not include recommendations from other organisations.

Answer MUST be focused on these 3 requirements:
* What recommended - best recommendations
* To consider - recommendations that doctor should consider
* What not recommended - bad options for patient's therapy

Rules:
- Output ONLY valid JSON!
- Every requirement MUST be in special JSON key!
- EVERY KEY IN JSON MUST BE FILLED!
- If there is not information in key - you MUST fill with "INSUFFICIENT INFORMATION"!


Give answer in JSON format: - EVERY KEY IN JSON MUST BE FILLED!
Each category must contain a list of bullet points.
{{
    "Recommended": ["...", "..."],
    "To consider": ["...", "..."],
    "Not recommended": ["...", "..."]
}}
Each bullet point mst be one complete recommendation.
EVERY KEY IN JSON MUST BE FILLED!
"""
    response = llm.invoke(prompt)
    print(f"\nODPOWIEDŹ LLMA: \n{response}")
    json = parse_str_to_json(response)
    print(f"\nPO PARSOWANIU: \n{json}")
    validated_json = validate_guideline_answer(json)
    return validated_json


def evaluate_answer(answer: GuidelineAnswer, base_query: str, query: str, context: str) -> str:
    llm = get_llm()
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

You MUST respond ONLY with a valid JSON object in the following format, without any extra text or markdown:
{{
  "status": "COMPLETE", "INCOMPLETE", or "UNAVAILABLE_IN_SOURCE",
  "missing_medical_info": "Explain briefly what is missing (or null if complete)",
  "suggested_search_term": "Provide a new, broader search query if incomplete (or null)"
}}
"""
    return llm.invoke(prompt)

def generate_followup_query(og_query: str, previous_answer: GuidelineAnswer) -> str:
    llm = get_llm()
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