import json
import re

def parse_str_to_json(answer: str) -> dict:
    cleaned = re.sub(r"```json|```", "", answer).strip()
    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if not match:
        raise ValueError("No JSON object found in LLM response")
    json_str = match.group()
    json_str = re.sub(r",\s*}", "}", json_str)
    json_str = re.sub(r",\s*]", "]", json_str)

    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON parsing failed: {e}\n\nRaw:\n{json_str}") from e

