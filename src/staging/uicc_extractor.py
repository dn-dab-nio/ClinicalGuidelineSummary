from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="llama3.2:latest")

def tnm_extract(patient_description):
    prompt = f"""
You are clinical staging assistant.
Extract TNM classification information from the patient description according to tables in sources.
    
Rules:
- If patient's type of cancer is described -> fill Cancer_type
- If patient's age is described -> fill age
- If tumor size or local invasion is described -> fill T with ONLY T feature - look at the greatest dimension in query
- Do not round up limits in tumor size - STAY IN LIMITS
- If lymph nodes are described -> fill N with only N feature
- If distant metastases are described -> fill M with only M feature
- If information in patient description is missing -> write: INSUFFICIENT_INFORMATION
- DO NOT infer
- DO NOT quess
- Output ONLY valid JSON

cancer_type must contain:

"label" – full clinical name exactly as mentioned in query, if not described -> INSUFFICIENT_INFORMATION 
"group" – must be one of the following values ONLY:

- "Differentiated thyroid carcinoma"
- "Medullary thyroid carcinoma"
- "Anaplastic thyroid carcinoma"

JSON format:
    
{{
    "age": 0,
    "T": "",
    "N": "",
    "M": "",
    "cancer_type": 
    {{
        "label": "",
        "group": ""
    }}
}}
    
Patient description:
{patient_description}
"""
    response = llm.invoke(prompt)
    return response

