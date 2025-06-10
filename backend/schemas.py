"""Pydantic schemas for vulnerability models."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

# pylint: disable=too-few-public-methods
class VulnerabilityBase(BaseModel):
    """Base schema for vulnerability input."""
    title: str
    description: str
    severity: str
    cve_id: Optional[str] = None

    class Config:
        """
            Configuration class for the Pydantic model.

            Enables attribute-style access for ORM objects by setting `from_attributes` to True.
            This allows Pydantic to populate the model from ORM instances like SQLAlchemy models.
        """
        from_attributes = True

class Vulnerability(VulnerabilityBase):
    """Schema for returning a full vulnerability object."""
    id: int
    date_reported: datetime
    ai_assessment: Optional[str] = None
    ai_ollama_assessment: Optional[str] = None

    class Config:
        """
            Configuration class for the Pydantic model.

            Enables attribute-style access for ORM objects by setting `from_attributes` to True.
            This allows Pydantic to populate the model from ORM instances like SQLAlchemy models.
        """
        from_attributes = True
