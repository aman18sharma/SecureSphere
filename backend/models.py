from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from database import Base

class Vulnerability(Base):
    __tablename__ = "vulnerabilities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    severity = Column(String(50), nullable=False)
    cve_id = Column(String(50))
    date_reported = Column(DateTime, default=datetime.utcnow)
    ai_assessment = Column(Text)