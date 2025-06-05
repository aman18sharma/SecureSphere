import os
import subprocess
import logging
import httpx


# Set up logger
logger = logging.getLogger(__name__)

def run_ollama_ai(title: str, description: str, severity: str):
    prompt = (
        "You are a cybersecurity expert analyzing software vulnerabilities. "
        "Analyze the following vulnerability and provide remediation advice:\n\n"
        f"Title: {title}\n"
        f"Description: {description}\n"
        f"Severity: {severity}"
    )
    try:
        result = subprocess.run(
            [
                'ollama', 'run', 'llama3',
                f"{prompt}"
            ],
            capture_output=True, text=True, timeout=120
        )
        print("Result>>>", result.stdout.strip())
        raw_output = result.stdout.strip()
        if not raw_output:
            return {"error": "Empty response from Ollama."}
        return raw_output # fallback to plain text
    except Exception as e:
        print("ERROR >> ", e)
        return {"error": str(e)}

def get_ai_assessment(title: str, description: str, severity: str) -> str:
    """
    Get AI assessment from OLLAMA server
    """
    ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    endpoint = f"{ollama_host}/api/chat"

    prompt = (
        "You are a cybersecurity expert analyzing software vulnerabilities. "
        "Analyze the following vulnerability and provide remediation advice:\n\n"
        f"Title: {title}\n"
        f"Description: {description}\n"
        f"Severity: {severity}"
    )

    payload = {
        "model": os.getenv("OLLAMA_MODEL", "llama3"),
        "messages": [
            {"role": "system", "content": "You are a cybersecurity expert."},
            {"role": "user", "content": prompt}
        ],
        "stream": False,
        "options": {"temperature": 0.3}
    }

    try:
        with httpx.AsyncClient(timeout=60.0) as client:
            response = client.post(endpoint, json=payload)
            response.raise_for_status()
            data = response.json()
            return data["message"]["content"].strip()
    except Exception as e:
        logger.error(f"OLLAMA API error: {str(e)}")
        print(e)
        return f"AI assessment failed: {str(e)}"