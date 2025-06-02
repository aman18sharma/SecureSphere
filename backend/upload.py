from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
import json
from datetime import datetime
import schemas
from database import get_db
from models import Vulnerability
from ai_assessor import generate_ai_assessment

router = APIRouter()

@router.post("/")
async def upload_vulnerabilities(

    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        contents = await file.read()
        vuln_data = json.loads(contents)
        new_vulns = []
        for item in vuln_data:
            # assessment = generate_ai_assessment(1, item)
            # print(assessment)
            vuln = Vulnerability(
                title=item['title'],
                description=item['description'],
                severity=item['severity'],
                cve_id=item.get('cve_id'),
                date_reported=datetime.utcnow()
                # ai_assessment=assessment
            )
            db.add(vuln)
            new_vulns.append(vuln)

        db.commit()
        return {"message": f"Added {len(new_vulns)} vulnerabilities", "ids": [str(v.id) for v in new_vulns]}
    except Exception as e:
        print("EEE", e)
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))