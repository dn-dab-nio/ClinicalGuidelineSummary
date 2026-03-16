import json
import re

def parse_str_to_json(answer: str) -> dict:
    raw_text = re.sub(r"```json|```", "", answer).strip()

    try:
        return json.loads(raw_text)
    except json.decoder.JSONDecodeError:
        raise ValueError("Error: Can not parse json !")
