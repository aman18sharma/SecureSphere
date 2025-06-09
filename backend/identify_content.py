import os
import json
import re

def identify_file_content(file_content):
    print(f"Content of the file:\n")
    print(file_content)
    print("\n")

    # Identify the type of content
    file_type = identify_type(file_content)
    if file_type:
        print(f"The file is identified as: {file_type}")
        return file_type
    else:
        print("The file type could not be determined.")

def identify_type(content):
    # Check for JSON
    if is_json(content):
        return 'json'

    # Check for shell script (basic check for shebang)
    if is_shell(content):
        return 'shell'

    # Check for configuration files (basic check for key-value pairs)
    if is_config(content):
        return 'config'

    # Check for logs (basic check for timestamps)
    if is_log(content):
        return 'logs'

    # Check for code (basic check for programming syntax)
    if is_code(content):
        return 'code'

    # Check for reasoning or threat (basic keyword checks)
    if is_reasoning(content):
        return 'reasoning'

    if is_threat(content):
        return 'threat'

    # Check for OWASP-related content (basic keyword checks)
    if is_owasp(content):
        return 'owasp'

    return None

def is_json(content):
    try:
        json.loads(content)
        return True
    except json.JSONDecodeError:
        return False

def is_shell(content):
    return content.startswith("#!")  # Check for shebang

def is_config(content):
    # Basic check for key-value pairs
    return bool(re.search(r'^\s*\w+\s*=\s*.*$', content, re.MULTILINE))

def is_log(content):
    # Basic check for timestamps in logs (e.g., YYYY-MM-DD or similar)
    return bool(re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', content))

def is_code(content):
    # Basic check for common programming syntax (e.g., function definitions)
    return bool(re.search(r'\bdef\b|\bclass\b|\bimport\b', content))

def is_reasoning(content):
    # Check for keywords commonly associated with reasoning
    keywords = ['because', 'therefore', 'thus', 'hence']
    return any(keyword in content.lower() for keyword in keywords)

def is_threat(content):
    # Check for keywords commonly associated with threats
    keywords = ['vulnerability', 'exploit', 'attack', 'breach']
    return any(keyword in content.lower() for keyword in keywords)

def is_owasp(content):
    # Check for OWASP-related keywords
    keywords = ['OWASP', 'Top Ten', 'vulnerability', 'security']
    return any(keyword in content for keyword in keywords)
  
