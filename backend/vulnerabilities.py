from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import schemas
from database import get_db
from models import Vulnerability

router = APIRouter()

@router.get("/", response_model=List[schemas.Vulnerability])
def get_vulnerabilities(db: Session = Depends(get_db)):
    return db.query(Vulnerability).all()

@router.get("/{vuln_id}", response_model=schemas.Vulnerability)
def get_vulnerability(vuln_id: int, db: Session = Depends(get_db)):

    vuln = db.query(Vulnerability).filter(Vulnerability.id == vuln_id).first()
    if not vuln:
        raise HTTPException(status_code=404, detail="Vulnerability not found")
    return vuln

def get_by_cve_id_vulnerability(cve_id: int, db: Session = Depends(get_db)):

    vuln = db.query(Vulnerability).filter(Vulnerability.cve_id == cve_id).first()
    if not vuln:
        raise HTTPException(status_code=404, detail="Vulnerability not found")
    return vuln