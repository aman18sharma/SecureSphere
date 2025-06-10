import os
import json
import pdb
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from database import get_db
from models import Vulnerability
from ai_assessor import generate_ai_assessment
from vulnerabilities import get_by_cve_id_vulnerability
from services.llama import api_ollama_ai, subprocess_ollama_ai

router = APIRouter()

UPLOAD_DIR = "./uploaded_data"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@router.post("/")
async def upload_vulnerabilities(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        print("FILE:", file)
        contents = await file.read()
        vuln_data_raw = json.loads(contents)

        cve_id = vuln_data_raw.get('cveMetadata', {}).get('cveId')
        if not cve_id:
            raise HTTPException(status_code=400, detail="CVE ID not found in uploaded data")

        existing_vuln = get_by_cve_id_vulnerability(cve_id, db)
        if existing_vuln:
            return {
                "message": f"Vulnerability already exists with CVE ID {cve_id}",
                "ids": [str(existing_vuln.id)]
            }

        assessment_str = generate_ai_assessment(vuln_data_raw)
        ollama_str = api_ollama_ai(vuln_data_raw)
        ollama_json = json.loads(ollama_str['response'])
        open_api_json = json.loads(assessment_str)
        print("OLLAMA RESP", ollama_json)
        print("OPEN AI RESP", open_api_json)

        # Save uploaded JSON file for record keeping
        with open(os.path.join(UPLOAD_DIR, f"{(ollama_json.get('cve_id') or open_api_json.get('cve_id'))}.json"), 'w') as f:
            json.dump(vuln_data_raw, f, indent=4)

        vuln = Vulnerability(
            title=(ollama_json.get('title') or open_api_json.get('title')),
            description=(ollama_json.get('description') or open_api_json.get('description')),
            severity=(ollama_json.get('severity') or open_api_json.get('severity')),
            cve_id=(ollama_json.get('cve_id') or open_api_json.get('cve_id')),
            ai_assessment=assessment_str,
            ai_ollama_assessment=ollama_str['response'],
            date_reported=datetime.utcnow()
        )
        db.add(vuln)
        db.commit()

        return {
            "message": "Vulnerability added successfully",
            "ids": [str(vuln.id)]
        }

    except json.JSONDecodeError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid JSON file uploaded")
    except HTTPException:
        # Propagate HTTPExceptions as is
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
