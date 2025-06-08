import requests
import json

def query_ollama(full_prompt, model="llama3.2:latest", timeout=120):
    url = "http://localhost:11434/api/generate"
    headers = {
        "Content-Type": "application/json",
    }
    data = {
        "model": model,
        "prompt": full_prompt,
        "stream": False  # Set to True if you want streaming response
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            data=json.dumps(data),
            timeout=timeout
        )
        response.raise_for_status()  # Raises exception for 4XX/5XX errors

        # Parse the response
        result = response.json()
        return {
            "response": result.get("response", ""),
            "status_code": response.status_code,
            "details": result
        }

    except requests.exceptions.RequestException as e:
        return {
            "error": str(e),
            "status_code": getattr(e.response, 'status_code', None)
        }