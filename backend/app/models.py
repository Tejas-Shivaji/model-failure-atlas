from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func
from app.database import Base

class Investigation(Base):
    __tablename__ = "investigations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(160), nullable=False)
    dataset_name = Column(String(255), nullable=False)
    summary_json = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
