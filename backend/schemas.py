"""Pydantic schemas for vulnerability models."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class VulnerabilityBase(BaseModel):
    """Base schema for vulnerability input."""
    title: str
    description: str
    severity: str
    cve_id: Optional[str] = None

    class Config:
        from_attributes = True


class VulnerabilityCreate(VulnerabilityBase):
    """Schema for creating a new vulnerability."""
    pass


class Vulnerability(VulnerabilityBase):
    """Schema for returning a full vulnerability object."""
    id: int
    date_reported: datetime
    ai_assessment: Optional[str] = None

    class Config:
        from_attributes = True
