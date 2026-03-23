def build_data_query(data_json: dict) -> str:
    return f"""
Provide evidence-based clinical management recommendations for the following patient with:

- Age: {data_json["age"]}
- Cancer type: {data_json['cancer_type']["label"]}, ({data_json["cancer_type"]["group"]})
- T classification: {data_json["T"]}
- N classification: {data_json["N"]}
- M classification: {data_json["M"]}
- UICC Stage: {data_json["Stage"]}

Use clinical guidelines from sources you have in vectorstore.
Focus on treatment.
"""

