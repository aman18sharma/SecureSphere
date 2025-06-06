"""SQLAlchemy model definition for the Vulnerability table."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime

from database import Base


class Vulnerability(Base):
    """
    ORM model for storing software vulnerability details.

    Attributes:
        id (int): Primary key.
        title (str): Short name/title of the vulnerability.
        description (str): Detailed description of the vulnerability.
        severity (str): Severity level (e.g., Low, Medium, High, Critical).
        cve_id (str): CVE identifier if available.
        date_reported (datetime): Timestamp of when it was reported.
        ai_assessment (str): AI-generated security analysis and suggestions.
    """

    __tablename__ = "vulnerabilities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    severity = Column(String(50), nullable=False)
    cve_id = Column(String(50), nullable=True)
    date_reported = Column(DateTime, default=datetime.utcnow)
    ai_assessment = Column(Text, nullable=True)
    ai_ollama_assessment = Column(Text, nullable=True)
