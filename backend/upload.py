from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
import json
from datetime import datetime
from database import get_db
from models import Vulnerability
from vulnerabilities import get_by_cve_id_vulnerability
from ai_assessor import generate_ai_assessment
from services.llama import run_ollama_ai
import os

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
        print("FILE:", file.filename)
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

        vuln_data = {
            'title': vuln_data_raw['containers']['cna']['title'],
            'description': vuln_data_raw['containers']['cna']['descriptions'][0]['value'],
            'cve_id': cve_id
        }

        # assessment_str = generate_ai_assessment(contents)
        ollama_str = run_ollama_ai(contents)
        # assessment_json = json.loads(assessment_str)
        print(ollama_str)

        # Save uploaded JSON file for record keeping
        with open(os.path.join(UPLOAD_DIR, f"{cve_id}.json"), 'w') as f:
            json.dump(vuln_data_raw, f, indent=4)

        vuln = Vulnerability(
            title=vuln_data['title'],
            description=vuln_data['description'],
            severity="High",#assessment_json.get('complex_findings', {}).get('severity', 'Unknown'),
            cve_id=cve_id,
            # ai_assessment=assessment_str,
            ai_ollama_assessment=ollama_str,
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
