from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from sqlalchemy import Integer

class VulnerabilityBase(BaseModel):
    title: str
    description: str
    severity: str
    cve_id: Optional[str] = None

    class Config:
        orm_mode = True

class VulnerabilityCreate(VulnerabilityBase):
    pass

class Vulnerability(VulnerabilityBase):
    id: int
    date_reported: datetime
    ai_assessment: Optional[str] = None

    class Config:
        orm_mode = True