"""AI Assessment Module using OpenAI"""

import os
import logging
from typing import Any

from dotenv import load_dotenv
import openai
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Vulnerability
from prompt import prompt_string, response_format_json
import schemas

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def configure_openai() -> None:
    """Configure OpenAI API key from environment."""
    openai.api_key = os.getenv('OPEN_API_KEY')
    if not openai.api_key:
        raise EnvironmentError("OPEN_API_KEY not set in environment variables")


def run_ai_assessment(vuln_id: int, db: Session = Depends(get_db)) -> dict[str, Any]:
    """
    Run an AI-powered assessment for a specific vulnerability.

    Args:
        vuln_id (int): The ID of the vulnerability.
        db (Session): SQLAlchemy DB session (injected via FastAPI).

    Returns:
        dict: Dictionary containing the AI assessment result.

    Raises:
        HTTPException: If vulnerability is not found.
    """
    vuln = db.query(Vulnerability).filter(Vulnerability.id == vuln_id).first()

    if not vuln:
        raise HTTPException(status_code=404, detail="Vulnerability not found")

    try:
        vuln_data = schemas.VulnerabilityBase.from_orm(vuln).json()

        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": f"I want you to always reply in the following JSON format: {response_format_json()}"},
                {"role": "system", "content": prompt_string()},
                {"role": "system", "content": vuln_data},
            ]
        )

        assessment = response.choices[0].message['content'].strip()
        vuln.ai_assessment = assessment
        db.commit()

        logger.info("AI assessment completed successfully.")
        return {"assessment": assessment}

    except openai.OpenAIError as exc:
        logger.error("OpenAI API error: %s", exc)
        raise HTTPException(status_code=500, detail="OpenAI API error occurred.")
    except Exception as exc:
        logger.error("Unexpected error during assessment: %s", exc)
        raise HTTPException(status_code=500, detail="Internal server error.")
