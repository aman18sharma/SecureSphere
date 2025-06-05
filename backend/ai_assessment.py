import os
from openai import OpenAI
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Vulnerability
from prompt import prompt_string, response_format_json
import schemas


router = APIRouter()

@router.post("/{vuln_id}/assess")
async def run_ai_assessment(vuln_id: int, db: Session = Depends(get_db)):
    try:
        vuln = db.query(Vulnerability).filter(Vulnerability.id == vuln_id).first()
        vuln_data = schemas.VulnerabilityBase.from_orm(vuln).json()
        client = OpenAI(api_key=os.getenv('OPEN_API_KEY'))  # Create OpenAI client instance
        # Combine system messages for better efficiency
        system_content = (
            f"I want you to always reply in the following JSON format: {response_format_json()}\n\n"
            f"{prompt_string()}"
        )
        response = client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},  # Enforce JSON response
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": str(vuln_data)}  # Properly structured user input
            ]
        )
        # Extract content from response
        content = response.choices[0].message.content.strip()
        # print(content)  # Print the actual content instead of full response
        print("ASSESSMENT >>> ", content)
        db.commit()

        return {"assessment": content}
    except Exception as e:
        print("Error in AI Assesment >>", e)

