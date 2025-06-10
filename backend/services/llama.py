"""AI Assessment using Ollama (via subprocess and HTTP API)."""
import time
import json
import subprocess
import logging
import requests
from prompt import prompt_string, response_format_json, ollama_prompt
from .json_to_text import extract_json_from_text

# Set up logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def subprocess_ollama_ai(content):
    """
    Run a local Ollama model via subprocess for AI assessment.

    Args:
        title (str): Vulnerability title.
        description (str): Vulnerability description.
        severity (str): Vulnerability severity.

    Returns:
        str | dict: Raw output from the model or error message.
    """

    full_prompt = (
        f"{ollama_prompt()}\n```json\n{response_format_json()}```\n\n"
        f"{prompt_string()}\n```json\n{content}\n```"
    )

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
    # pylint: disable=broad-exception-caught
    except Exception as exc:
        logger.exception("Unexpected error in Ollama subprocess.")
        return {"error": str(exc)}


def api_ollama_ai(content, model="llama3.2:latest", timeout=600):
    """
        Run a local Ollama model via API for AI assessment.

        Args:
            content
            model
            timeout

        Returns:
            str | dict: Raw output from the model or error message.
    """
    url = "http://localhost:11434/api/generate"
    headers = {
        "Content-Type": "application/json",
    }

    full_prompt = (
        f"{ollama_prompt()}\n```json\n{response_format_json()}```\n\n"
        f"{prompt_string()}\n```json\n{content}\n```"
    )
    data = {
        "model": model,
        "prompt": full_prompt,
        "stream": False  # Set to True if you want streaming response
    }

    try:
        t1 = time.perf_counter()
        response = requests.post(
            url,
            headers=headers,
            data=json.dumps(data),
            timeout=timeout
        )
        response.raise_for_status()  # Raises exception for 4XX/5XX errors

        # Parse the response
        result = response.json()
        resp = extract_json_from_text(result.get("response", ""))
        t2 = time.perf_counter() - t1
        print("Ollma Llama3 time taken %s seconds", t2)
        return {
            "response": resp
        }

    except requests.exceptions.RequestException as e:
        return {
            "error": str(e),
            "status_code": getattr(e.response, 'status_code', None)
        }
