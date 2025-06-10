"""Parse Json to String"""
import json
import re

def extract_json_from_text(text: str) -> str:
    """
    Extracts the JSON code block from a string and returns it as a Python dictionary.

    Args:
        text (str): The input text containing JSON in markdown-style code block.

    Returns:
        dict: Parsed JSON data.

    Raises:
        ValueError: If JSON cannot be extracted or parsed.
    """
    try:
        # Match JSON block between triple backticks (```...```)
        match1 = re.search(r"```(?:json)?\n({.*?})\n```", text, re.DOTALL)
        match2 = re.search(r"```\n({.*?})\n```", text, re.DOTALL)

        if not match1 and not match2:
            raise ValueError("JSON block not found in the text.")
        match = match1 or match2
        json_str = match.group(1)
        return json_str

    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format: {e}") from e
    except Exception as e:
        raise ValueError(f"Error extracting JSON: {e}") from e
