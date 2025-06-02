import re
import json

def parse_json_string(input_str):
    try:
        cleaned = re.sub(r'^```json|```$', '', input_str).strip()
        return json.loads(cleaned)
    except Exception as e:
        return f'Failed to parse JSON: {str(e)}'