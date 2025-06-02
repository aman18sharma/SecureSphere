import os
import openai
from ai_assessor import generate_ai_assessment
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Vulnerability
from services import llama
from prompt import prompt_string, response_format_json
import schemas


router = APIRouter()

@router.post("/{vuln_id}/assess")
async def run_ai_assessment(vuln_id: int, db: Session = Depends(get_db)):
    vuln = db.query(Vulnerability).filter(Vulnerability.id == vuln_id).first()
    vuln_data = schemas.VulnerabilityBase.from_orm(vuln).json()
    if not vuln:
        raise HTTPException(status_code=404, detail="Vulnerability not found")

    try:
        # Call ChatGPT API
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": f"I want you to always reply in the following JSON format: {response_format_json()}"},
                {"role": "system", "content": prompt_string()},
                {"role": "system", "content": vuln_data},
                # {"role": "user", "content": f"Analyze this vulnerability and provide remediation advice:\n\nTitle: {vuln.title}\nDescription: {vuln.description}\nSeverity: {vuln.severity}"}
            ]
        )

        # Update vulnerability with assessment
        assessment = response.choices[0].message['content'].strip()
        vuln.ai_assessment = assessment
        print("ASSESSMENT >>> ", assessment)
        db.commit()

        return {"assessment": assessment}
    except Exception as e:
        print("Error in AI Assesment >>", e)
# async def run_ai_assessment(vuln_id: int, db: Session = Depends(get_db)):
#     vuln = db.query(Vulnerability).filter(Vulnerability.id == vuln_id).first()
#     vuln_data = schemas.VulnerabilityBase.from_orm(vuln).json()
#     if not vuln:
#         raise HTTPException(status_code=404, detail="Vulnerability not found")

#     assessment = generate_ai_assessment(vuln, {})
#     print("ASSESSMENT >>> ", assessment)
#     # Store assessment
#     vuln.ai_assessment = assessment
#     db.commit()
    # try:
    #     # Call ChatGPT API
    #     response = openai.ChatCompletion.create(
    #         model="gpt-4o",
    #         messages=[
    #             {"role": "system", "content": f"I want you to always reply in the following JSON format: {response_format_json()}"},
    #             {"role": "system", "content": prompt_string()},
    #             {"role": "system", "content": vuln_data},
    #             # {"role": "user", "content": f"Analyze this vulnerability and provide remediation advice:\n\nTitle: {vuln.title}\nDescription: {vuln.description}\nSeverity: {vuln.severity}"}
    #         ]
    #     )

    #     # Update vulnerability with assessment
    #     assessment = response.choices[0].message['content'].strip()
    #     vuln.ai_assessment = assessment
    #     print("ASSESSMENT >>> ", assessment)
    #     db.commit()

    #     return {"assessment": assessment}
    # except Exception as e:
    #     print("Error in AI Assesment >>", e)