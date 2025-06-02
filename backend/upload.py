from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
import json
from datetime import datetime
from database import get_db
from models import Vulnerability
from vulnerabilities import get_by_cve_id_vulnerability
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
        cve_id = vuln_data.get('cveMetadata', {}).get('cveId')
        vuln = get_by_cve_id_vulnerability(cve_id, db)
        if not vuln:
            vuln_data = {
                            'title': vuln_data['containers']['cna']['title'],
                            'description': vuln_data['containers']['cna']['descriptions'][0]['value'],
                            'cve_id': cve_id
                        }

            assesment = generate_ai_assessment(vuln_data)
            print('assesment', type(assesment))
            json_resp = json.loads(assesment)
            print("json_resp", type(json_resp))

            with open(f"./uploaded_data/{cve_id}.json", 'w') as file:
                # Step 2: Dump JSON data into a json file
                json.dump([vuln_data], file, indent=4)
            for item in [vuln_data]:
                vuln = Vulnerability(
                    title=item['title'],
                    description=item['description'],
                    severity=json_resp.get('complex_findings', {}).get('Severity'),
                    cve_id=item.get('cve_id'),
                    ai_assessment=assesment,
                    date_reported=datetime.utcnow()
                )
                db.add(vuln)
                new_vulns.append(vuln)
            db.commit()
            print("DB COMMITED")
            return {"message": f"Added {len(new_vulns)} vulnerabilities", "ids": [str(v.id) for v in new_vulns]}
        else:
            print("Vuln Found")
            new_vulns.append(vuln)
            return {"message": f"Vulnerability found with cve id {cve_id}", "ids": [str(v.id) for v in new_vulns]}
    except Exception as e:
        print("EEE", e)
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))