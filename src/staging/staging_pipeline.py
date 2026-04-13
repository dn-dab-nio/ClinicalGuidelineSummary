from src.staging.uicc_extractor import tnm_extract
from src.validation.json_parser import parse_str_to_json
from src.validation.validator import validate_json
from src.staging.uicc_mapper import map_uicc


def run_staging(query: str) -> dict | None:
    try:
        answer = tnm_extract(query)
        print(answer)
        parsed_answer = parse_str_to_json(answer)
        parsed_answer = validate_json(parsed_answer)
        final = map_uicc(parsed_answer)
        return final
    except Exception as e:
         raise ValueError(f"[Pipeline Error] Staging failed")


