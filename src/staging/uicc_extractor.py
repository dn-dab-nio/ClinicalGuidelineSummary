from langchain_ollama import OllamaLLM
from src.rag.retriever import retrieve_context

llm = OllamaLLM(model="gpt-oss", base_url="http://127.0.0.1:11434")

def tnm_extract(patient_description: str, vectorstore):
    context = retrieve_context(vectorstore, patient_description)
    prompt = f"""
You are clinical staging assistant. Using PROVIDED CONTEXT extract:
 - TNM classification information, 
 - information, if thyroid ultrasound (USG) was performed,
 - information, if biopsy/FNA was performed,
 - information about Bethesda category if mentioned!
 FROM PATIENT DESCRIPTION according to tables in sources and put it in JSON format. 

Context: 
{context}

Patient description:
{patient_description}

Rules:
- If patient's age is described -> fill age, if is not described -> fill age with "INSUFFICIENT_INFORMATION"
- If tumor size (local invasion) is described -> fill T with ONLY T feature - look at the greatest dimension in query
- Do not round up limits in tumor size - STAY IN LIMITS
- If lymph nodes (N) are described -> fill N with only N feature, If is not described -> fill with "INSUFFICIENT_INFORMATION"
- If distant metastases (M) are described -> fill M with only M feature, If is not described -> fill with "INSUFFICIENT_INFORMATION"
- If name of cancer is NOT described in patient description -> DO NOT guess, fill 'label' with "INSUFFICIENT_INFORMATION" and fill 'group' with "Differentiated thyroid carcinoma"
- DO NOT infer
- DO NOT quess
- DO NOT leave empty keys (especially key 'group')!
- DO NOT write tumor size instead of T feature
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
    }},
    "Bethesda_System_Category": "",
    "USG": "",
    "Biopsy": "",
}}
"""
    response = llm.invoke(prompt)
    return response

