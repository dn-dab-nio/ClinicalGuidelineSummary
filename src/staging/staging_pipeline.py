from src.staging.uicc_extractor import tnm_extract
from src.staging.json_parser import parse_str_to_json
from src.staging.uicc_validator import validate_json
from src.staging.uicc_mapper import map_uicc

def run_staging(query):
    answer = tnm_extract(query)

    parsed_answer = parse_str_to_json(answer)
    if parsed_answer is None:
        return "Invalid JSON from LLM!!!"

    is_valid, message = validate_json(parsed_answer)
    if not is_valid:
        return {"error": message}

    final = map_uicc(parsed_answer)
    return final

