"""AI-powered vulnerability assessment route using OpenAI."""

import os
import logging
import pdb
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from openai import OpenAI
from services.llama import api_ollama_ai
from database import get_db
from models import Vulnerability
from prompt import prompt_string, response_format_json
import schemas

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/{vuln_id}/assess_by_ollama")
async def run_ai_assessment(vuln_id: int, db: Session = Depends(get_db)) -> dict:
    """
    Run an AI assessment on a specific vulnerability using OpenAI's GPT-4o model.

    Args:
        vuln_id (int): The ID of the vulnerability to assess.
        db (Session): SQLAlchemy database session.

    Returns:
        dict: The assessment result from the AI.

    Raises:
        HTTPException: If the vulnerability is not found or an error occurs.
    """
    vuln = db.query(Vulnerability).filter(Vulnerability.id == vuln_id).first()
    if not vuln:
        raise HTTPException(status_code=404, detail="Vulnerability not found")
    try:
        vuln_data = schemas.VulnerabilityBase.model_validate(vuln).model_dump_json()

        content = api_ollama_ai(vuln_data)
        vuln.ai_ollama_assessment = content['response']
        print(['response'])
        db.commit()

        logger.info("AI assessment completed for vulnerability ID %d", vuln_id)
        return {"assessment": content}

    except Exception as exc:
        logger.exception("Error during AI assessment")
        raise HTTPException(status_code=500, detail=f"AI assessment failed: {exc}")

@router.post("/{vuln_id}/assess")
async def run_ai_assessment(vuln_id: int, db: Session = Depends(get_db)) -> dict:
    """
    Run an AI assessment on a specific vulnerability using OpenAI's GPT-4o model.

    Args:
        vuln_id (int): The ID of the vulnerability to assess.
        db (Session): SQLAlchemy database session.

    Returns:
        dict: The assessment result from the AI.

    Raises:
        HTTPException: If the vulnerability is not found or an error occurs.
    """
    vuln = db.query(Vulnerability).filter(Vulnerability.id == vuln_id).first()
    if not vuln:
        raise HTTPException(status_code=404, detail="Vulnerability not found")

    try:
        vuln_data = schemas.VulnerabilityBase.model_validate(vuln).model_dump_json()

        system_content = (
            f"I want you to always reply in the following JSON format: {response_format_json()}\n\n"
            f"{prompt_string()}"
        )

        client = OpenAI(api_key=os.getenv("OPEN_API_KEY"))

        response = client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": vuln_data}
            ]
        )

        content = response.choices[0].message.content.strip()
        vuln.ai_assessment = content
        db.commit()

        logger.info("AI assessment completed for vulnerability ID %d", vuln_id)
        return {"assessment": content}

    except Exception as exc:
        logger.exception("Error during AI assessment")
        raise HTTPException(status_code=500, detail=f"AI assessment failed: {exc}")
