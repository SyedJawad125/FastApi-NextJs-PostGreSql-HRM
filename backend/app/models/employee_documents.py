from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Text, func
from sqlalchemy.orm import relationship
from app.database import Base
import enum


# Optional Enum for Document Type
class DocumentType(str, enum.Enum):
    RESUME = "resume"
    CERTIFICATE = "certificate"
    ID_PROOF = "id_proof"
    OTHER = "other"



class EmployeeDocument(Base):
    __tablename__ = "employee_documents"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    document_type = Column(Enum(DocumentType), nullable=False)
    document_name = Column(String(100), nullable=False)
    document_path = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    uploaded_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)

    employee = relationship("Employee", back_populates="documents")
