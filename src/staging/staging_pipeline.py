from src.staging.uicc_extractor import tnm_extract
from src.staging.json_parser import parse_str_to_json
from src.staging.uicc_validator import validate_json
from src.staging.uicc_mapper import map_uicc

def run_staging(query: str) -> dict:
    answer = tnm_extract(query)
    parsed_answer = parse_str_to_json(answer)
    parsed_answer = validate_json(parsed_answer)
    final = map_uicc(parsed_answer)
    return final

