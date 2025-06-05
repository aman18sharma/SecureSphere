"""AI Assessment generator using OpenAI GPT-4o."""

import os
import logging
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError
from fastapi import HTTPException

from prompt import response_format_json, prompt_string

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_ai_assessment(vuln) -> str:
    """
    Generate an AI assessment for the given vulnerability.

    Args:
        vuln: A Pydantic or ORM vulnerability object.

    Returns:
        str: The AI-generated assessment content.

    Raises:
        HTTPException: For OpenAI or unexpected errors.
    """
    try:
        client = OpenAI(api_key=os.getenv("OPEN_API_KEY"))

        system_content = (
            f"I want you to always reply in the following JSON format: {response_format_json()}\n\n"
            f"{prompt_string()}"
        )

        response = client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": str(vuln)}
            ]
        )

        return response.choices[0].message.content.strip()

    except OpenAIError as exc:
        logger.error("OpenAI error occurred: %s", exc)
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {exc}") from exc

    except Exception as exc:
        logger.exception("Unexpected error during AI assessment")
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error during AI assessment: {exc}"
        ) from exc
