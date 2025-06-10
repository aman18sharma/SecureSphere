"""Handling the database operations"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
import schemas
from database import get_db
from models import Vulnerability

router = APIRouter()

@router.get("/", response_model=List[schemas.Vulnerability])
def get_vulnerabilities(db: Session = Depends(get_db)) -> List[schemas.Vulnerability]:
    """Retrieve all vulnerabilities."""
    return db.query(Vulnerability).order_by(
        asc(Vulnerability.severity),
        desc(Vulnerability.date_reported)).all()

@router.get("/{vuln_id}", response_model=schemas.Vulnerability)
def get_vulnerability(vuln_id: int, db: Session = Depends(get_db)) -> schemas.Vulnerability:
    """Retrieve a vulnerability by its ID."""
    vuln = db.query(Vulnerability).filter(Vulnerability.id == vuln_id).first()
    if vuln is None:
        raise HTTPException(status_code=404, detail="Vulnerability not found")
    return vuln

def get_by_cve_id_vulnerability(cve_id: str, db: Session) -> Optional[Vulnerability]:
    """Retrieve a vulnerability by its CVE ID."""
    return db.query(Vulnerability).filter(Vulnerability.cve_id == cve_id).first()
