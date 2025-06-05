import re
import json

def parse_json_string(input_str):
    """
    Parses a JSON string that may be wrapped in markdown-style ```json ... ``` code fences.

    Args:
        input_str (str): Input string possibly containing JSON wrapped in ```json ... ```.

    Returns:
        dict or list: Parsed JSON object if successful.
        str: Error message if parsing fails.
    """
    try:
        # Remove ```json at the start and ``` at the end (with optional whitespace)
        cleaned = re.sub(r'^```json\s*|\s*```$', '', input_str.strip())
        return json.loads(cleaned)
    except Exception as e:
        return f'Failed to parse JSON: {str(e)}'
