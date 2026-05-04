from langchain_ollama import OllamaLLM
from src.rag.retriever import retrieve_context

llm = OllamaLLM(model="gpt-oss")

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
- If patient's type of cancer is described -> fill Cancer_type
- If patient's age is described -> fill age
- If tumor size (local invasion) is described -> fill T with ONLY T feature - look at the greatest dimension in query
- Do not round up limits in tumor size - STAY IN LIMITS
- If lymph nodes (N) are described -> fill N with only N feature
- If distant metastases (M) are described -> fill M with only M feature
- If name of cancer is NOT described in patient description -> DO NOT guess, fill 'label' with "INSUFFICIENT_INFORMATION"
- If ANY required information in patient description is MISSING -> write: INSUFFICIENT_INFORMATION (except group of cancer)
- DO NOT infer
- DO NOT quess
- DO NOT leave empty keys
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

