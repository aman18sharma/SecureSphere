"""AI Assessment using Ollama (via subprocess and HTTP API)."""

import os
import subprocess
import logging
import httpx
from prompt import prompt_string

# Set up logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_ollama_ai(vuln_data):
    """
    Run a local Ollama model via subprocess for AI assessment.

    Args:
        title (str): Vulnerability title.
        description (str): Vulnerability description.
        severity (str): Vulnerability severity.

    Returns:
        str | dict: Raw output from the model or error message.
    """
    print("TYPE >>>> ", type(vuln_data))
    prompt = (
        "You are a cybersecurity expert analyzing software vulnerabilities. "
        "Analyze the following vulnerability and provide remediation advice:\n\n"
        f"{vuln_data.encode('utf-8')}"
    )

    full_prompt = f"{prompt_string}\n\n{vuln_data}"

    try:
        result = subprocess.run(
            ['ollama', 'run', 'llama3.2'],
            input=full_prompt,
            capture_output=True,
            text=True,
            timeout=120,
            check=True
        )
        output = result.stdout.strip()
        if not output:
            logger.warning("Empty response from Ollama subprocess.")
            return {"error": "Empty response from Ollama."}

        logger.info("Ollama subprocess assessment successful. %s", output)
        return output

    except subprocess.TimeoutExpired as exc:
        logger.error("Ollama subprocess timed out: %s", exc)
        return {"error": "Ollama subprocess timed out."}
    except subprocess.CalledProcessError as exc:
        logger.error("Ollama subprocess failed: %s", exc)
        return {"error": f"Ollama subprocess error: {exc}"}
    except Exception as exc:
        logger.exception("Unexpected error in Ollama subprocess.")
        return {"error": str(exc)}


def get_ai_assessment(title: str, description: str, severity: str) -> str:
    """
    Get AI assessment from Ollama's HTTP API.

    Args:
        title (str): Vulnerability title.
        description (str): Vulnerability description.
        severity (str): Vulnerability severity.

    Returns:
        str: Assessment string or error message.
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
        response = httpx.post(endpoint, json=payload, timeout=60.0)
        response.raise_for_status()
        data = response.json()
        return data["message"]["content"].strip()

    except httpx.HTTPStatusError as exc:
        logger.error("HTTP error from Ollama: %s", exc)
        return f"HTTP error from Ollama: {exc}"
    except httpx.RequestError as exc:
        logger.error("Request failed: %s", exc)
        return f"Request failed: {exc}"
    except KeyError:
        logger.error("Unexpected response format from Ollama.")
        return "Unexpected response format from Ollama."
    except Exception as exc:
        logger.exception("Unexpected error in get_ai_assessment.")
        return f"AI assessment failed: {exc}"
